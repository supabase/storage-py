from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Union, cast

from httpx import HTTPError, Response

from ..constants import DEFAULT_FILE_OPTIONS, DEFAULT_SEARCH_OPTIONS
from ..types import BaseBucket, ListBucketFilesOptions, RequestMethod
from ..utils import StorageException, SyncClient

__all__ = ["SyncBucket"]


class SyncBucketActionsMixin:
    """Functions needed to access the file API."""

    id: str
    _client: SyncClient

    def _request(
        self,
        method: RequestMethod,
        url: str,
        headers: Optional[dict[str, Any]] = None,
        json: Optional[dict[Any, Any]] = None,
        files: Optional[Any] = None,
    ) -> Response:
        response = self._client.request(
            method,
            url,
            headers=headers or {},
            json=json,
            files=files,
        )
        try:
            response.raise_for_status()
        except HTTPError:
            raise StorageException(
                {**response.json(), "statusCode": response.status_code}
            )

        return response

    def create_signed_url(self, path: str, expires_in: int) -> dict[str, str]:
        """
        Parameters
        ----------
        path
            file path to be downloaded, including the current file name.
        expires_in
            number of seconds until the signed URL expires.
        """
        path = self._get_final_path(path)
        response = self._request(
            "POST",
            f"/object/sign/{path}",
            json={"expiresIn": str(expires_in)},
        )
        data = response.json()
        data[
            "signedURL"
        ] = f"{self._client.base_url}{cast(str, data['signedURL']).lstrip('/')}"
        return data

    def get_public_url(self, path: str) -> str:
        """
        Parameters
        ----------
        path
            file path, including the path and file name. For example `folder/image.png`.
        """
        _path = self._get_final_path(path)
        return f"{self._client.base_url}object/public/{_path}"

    def move(self, from_path: str, to_path: str) -> dict[str, str]:
        """
        Moves an existing file, optionally renaming it at the same time.

        Parameters
        ----------
        from_path
            The original file path, including the current file name. For example `folder/image.png`.
        to_path
            The new file path, including the new file name. For example `folder/image-copy.png`.
        """
        res = self._request(
            "POST",
            "/object/move",
            json={
                "bucketId": self.id,
                "sourceKey": from_path,
                "destinationKey": to_path,
            },
        )
        return res.json()

    def remove(self, paths: list) -> dict[str, str]:
        """
        Deletes files within the same bucket

        Parameters
        ----------
        paths
            An array or list of files to be deletes, including the path and file name. For example [`folder/image.png`].
        """
        response = self._request(
            "DELETE",
            f"/object/{self.id}",
            json={"prefixes": paths},
        )
        return response.json()

    def list(
        self,
        path: Optional[str] = None,
        options: Optional[ListBucketFilesOptions] = None,
    ) -> list[dict[str, str]]:
        """
        Lists all the files within a bucket.

        Parameters
        ----------
        path
            The folder path.
        options
            Search options, including `limit`, `offset`, and `sortBy`.
        """
        extra_options = options or {}
        extra_headers = {"Content-Type": "application/json"}
        body = {**DEFAULT_SEARCH_OPTIONS, **extra_options, "prefix": path or ""}
        response = self._request(
            "POST",
            f"/object/list/{self.id}",
            json=body,
            headers=extra_headers,
        )
        return response.json()

    def download(self, path: str) -> bytes:
        """
        Downloads a file.

        Parameters
        ----------
        path
            The file path to be downloaded, including the path and file name. For example `folder/image.png`.
        """
        _path = self._get_final_path(path)
        response = self._request(
            "GET",
            f"/object/{_path}",
        )
        return response.content

    def upload(
        self, path: str, file: Union[str, Path], file_options: Optional[dict] = None
    ) -> Response:
        """
        Uploads a file to an existing bucket.

        Parameters
        ----------
        path
            The relative file path including the bucket ID. Should be of the format `bucket/folder/subfolder/filename.png`.
            The bucket must already exist before attempting to upload.
        file
            The File object to be stored in the bucket. or a async generator of chunks
        file_options
            HTTP headers. For example `cache-control`
        """
        if file_options is None:
            file_options = {}
        headers = {**self._client.headers, **DEFAULT_FILE_OPTIONS, **file_options}
        filename = path.rsplit("/", maxsplit=1)[-1]
        files = {"file": (filename, open(file, "rb"), headers.pop("content-type"))}
        _path = self._get_final_path(path)

        return self._request(
            "POST",
            f"/object/{_path}",
            files=files,
            headers=headers,
        )

    def _get_final_path(self, path: str) -> str:
        return f"{self.id}/{path}"


# this class is returned by methods that fetch buckets, for example StorageBucketAPI.get_bucket
# adding this mixin on the BaseBucket means that those bucket objects can also be used to
# run methods like `upload` and `download`
@dataclass(repr=False)
class SyncBucket(BaseBucket, SyncBucketActionsMixin):
    """Represents a storage bucket."""

    _client: SyncClient = field(repr=False)


@dataclass
class SyncBucketProxy(SyncBucketActionsMixin):
    """A bucket proxy, this contains the minimum required fields to query the File API."""

    id: str
    _client: SyncClient = field(repr=False)
