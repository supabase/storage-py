import os
from base64 import b64encode
from datetime import datetime

from .types import FileInfo, UploadMetadata
from .utils import StorageException, SyncClient

__all__ = ["ResumableUpload"]


class FileStore:
    """This class serves as storage of files to be sent in the resumable upload workflow"""

    def __init__(self):
        self.storage = {}

    def mark_file(self, file_info: FileInfo):
        """Store file metadata in a in-memory storage"""
        self.storage[file_info["name"]] = file_info

    def get_file_info(self, filename):
        return self.storage[filename]

    def update_file_headers(self, filename, key, value):
        file = self.get_file_info(filename)
        file["headers"][key] = value

    def get_file_headers(self, filename):
        return self.get_file_info(filename)["headers"]

    def get_file_storage_link(self, filename):
        return self.get_file_info(filename)["headers"]["link"]

    def open_file(self, filename: str, offset: int):
        """Open file in the specified offset
        Parameters
        ----------
        filename
            local file
        offset
            set current the file-pointer
        """
        file = open(filename, "rb")
        file.seek(offset)
        return file

    def close_file(self, filename):
        filename.close()

    def remove_file(self, filename: str):
        del self.storage[filename]

    def get_link(self, filename: str):
        return self.storage[filename]["link"]


class ResumableUpload:
    def __init__(self, session: SyncClient) -> None:
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

    def create_unique_link(
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
            info["headers"][upload_mode] = size
            info["length"] = size

        metadata = UploadMetadata(bucketName=bucketname, objectName=file)

        info["headers"]["Upload-Metadata"] = self._encode(metadata)
        response = self._client.post(self.url, headers=info["headers"])

        if response.status_code != 201:
            raise StorageException(response.content)

        expiration_time = datetime.strptime(
            response.headers["upload-expires"], self.expiration_time_format
        )
        info["expiration_time"] = expiration_time.timestamp()

        info["link"] = response.headers["location"]
        del info["headers"][upload_mode]
        self._filestore.mark_file(info)

    def resumable_offset(self, link, headers) -> str:
        """Get the current offset to be used
        Parameters
        ----------
        link
            Target url
        headers
            Metadata headers sent to the server
        """
        response = self._client.head(link, headers=headers)
        return response.headers["upload-offset"]

    def upload(
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
        chunk_size = 1048576 * int(mb_size)  # 1024 * 1024 * mb_size
        size = None
        self._filestore.update_file_headers(
            target_file, "Content-Type", "application/offset+octet-stream"
        )
        storage_link = link if upload_defer else self._filestore.get_link(target_file)

        if upload_defer:
            size = str(os.stat(filename).st_size)
            self._filestore.update_file_headers(target_file, "Upload-Length", size)

        while True:
            headers = self._filestore.get_file_headers(target_file)
            offset = self.resumable_offset(storage_link, headers)
            file = self._filestore.open_file(filename, offset=int(offset))
            self._filestore.update_file_headers(target_file, "Upload-Offset", offset)

            chunk = file.read(chunk_size)
            headers = self._filestore.get_file_headers(target_file)
            response = self._client.patch(storage_link, headers=headers, data=chunk)

            if response.status_code not in {201, 204}:
                raise StorageException(response.content)

            if "tus-complete" in response.headers:
                self._filestore.close_file(file)
                self._filestore.remove_file(target_file)
                break
