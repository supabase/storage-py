import os
from base64 import b64encode
from datetime import datetime

from ..types import FileInfo, UploadMetadata
from ..utils import AsyncClient, FileStore, StorageException


__all__ = ("AsyncResumableUpload", )


class AsyncResumableUpload:
    def __init__(self, session: AsyncClient) -> None:
        self._client = session
        self.url = f"{self._client.base_url}upload/resumable"
        self.expiration_time_format = "%a, %d %b %Y %X %Z"
        self._filestore = FileStore()

    def _encode(self, metadata: UploadMetadata) -> str:
        """Generate base64 encoding for Upload-Metadata header
        Parameters
        ----------
        metadata
            Bucket and object pair representing the resulting file in the storage
        """
        res = [
            f"{k} {b64encode(bytes(v, 'utf-8')).decode()}" for k, v in metadata.items()
        ]
        return ",".join(res)

    def file_exists(self, filename) -> bool:
        """Verify if the file exists in the storage
        Parameters
        ----------
        filename
            This could be the local filename or objectname in the storage
        """
        return filename in self._filestore.storage

    def get_link(self, objectname) -> str:
        """Get the link associated with objectname in the bucket
        Parameters
        ----------
        objectname
            This could be the local filename or objectname in the storage
        """
        if not self.file_exists(objectname):
            raise StorageException(f"There is no entry for {objectname} in FileStore")
        return self._filestore.get_link(objectname)

    async def create_unique_link(
        self, bucketname=None, objectname=None, filename=None
    ) -> None:
        """Create unique link according to bucketname and objectname
        Parameters
        ----------
        bucketname
            Storage bucket
        objectname
            Filename in the bucket
        filename
            Local file
        """
        if bucketname is None:
            raise StorageException("bucketname cannot be empty")

        if objectname is None and filename is None:
            raise StorageException("Must specify objectname or filename")

        file = None
        upload_mode = None

        if filename:
            _, file = os.path.split(filename)
        else:
            file = objectname

        info = FileInfo(
            name=file, link="", length="", headers={"Tus-Resumable": "1.0.0"}
        )

        if not filename:
            upload_mode = "Upload-Defer-Length"
            info["headers"][upload_mode] = "1"
        else:
            upload_mode = "Upload-Length"
            size = str(os.stat(filename).st_size)

            if int(size) == 0:
                raise StorageException(
                    f"Cannot create a link for an empty file: {file}"
                )

            info["headers"][upload_mode] = size
            info["length"] = size

        metadata = UploadMetadata(bucketName=bucketname, objectName=file)

        info["headers"]["Upload-Metadata"] = self._encode(metadata)
        response = await self._client.post(self.url, headers=info["headers"])

        if response.status_code != 201:
            raise StorageException(response.content)

        expiration_time = datetime.strptime(
            response.headers["upload-expires"], self.expiration_time_format
        )
        info["expiration_time"] = expiration_time.timestamp()

        info["link"] = response.headers["location"]
        del info["headers"][upload_mode]
        self._filestore.mark_file(info)

    async def resumable_offset(self, link, headers) -> str:
        """Get the current offset to be used
        Parameters
        ----------
        link
            Target url
        headers
            Metadata headers sent to the server
        """
        response = await self._client.head(link, headers=headers)
        return response.headers["upload-offset"]

    async def upload(
        self, filename, upload_defer=False, link=None, objectname=None, mb_size=1
    ) -> None:
        """Send file's content in chunks to the target url
        Parameters
        ----------
        filename
            Local file
        upload_defer
            Requires link and objectname to be True to retrieve file info in the FileStore
        link
            Target url
        objectname
            Name of the file in the bucket
        mb_size
            Amount of megabytes to be sent in each iteration
        """
        if upload_defer:
            if link is None or objectname is None:
                raise StorageException(
                    "Upload-Defer mode requires a link and objectname"
                )

        target_file = objectname if upload_defer else os.path.split(filename)[1]
        chunk_size = 1048576 * int(abs(mb_size))  # 1024 * 1024 * mb_size
        size = None
        self._filestore.update_file_headers(
            target_file, "Content-Type", "application/offset+octet-stream"
        )
        storage_link = link if upload_defer else self._filestore.get_link(target_file)

        if upload_defer:
            size = str(os.stat(filename).st_size)

            if int(size) == 0:
                raise StorageException(f"Cannot upload an empty file: {filename}")

            self._filestore.update_file_headers(target_file, "Upload-Length", size)

        while True:
            headers = self._filestore.get_file_headers(target_file)
            offset = await self.resumable_offset(storage_link, headers)
            file = self._filestore.open_file(filename, offset=int(offset))
            self._filestore.update_file_headers(target_file, "Upload-Offset", offset)

            chunk = file.read(chunk_size)
            headers = self._filestore.get_file_headers(target_file)
            response = await self._client.patch(
                storage_link, headers=headers, data=chunk
            )
            if response.status_code not in {201, 204}:
                raise StorageException(response.content)

            if "tus-complete" in response.headers:
                self._filestore.close_file(file)
                self._filestore.remove_file(target_file)
                break
