from __future__ import annotations

from typing import Any, Optional

from httpx import HTTPError, Response

from ..types import RequestMethod
from ..utils import StorageException, SyncClient
from .file_api import SyncBucket

__all__ = ["SyncStorageBucketAPI"]


class SyncStorageBucketAPI:
    """This class abstracts access to the endpoint to the Get, List, Empty, and Delete operations on a bucket"""

    def __init__(self, url: str, headers: dict[str, str], session: SyncClient) -> None:
        self.url = url
        self.headers = headers
        self._client = session

    def _request(
        self,
        method: RequestMethod,
        url: str,
        json: Optional[dict[Any, Any]] = None,
    ) -> Response:
        response = self._client.request(method, url, headers=self.headers, json=json)
        try:
            response.raise_for_status()
        except HTTPError:
            raise StorageException(response.json())

        return response

    def list_buckets(self) -> list[SyncBucket]:
        """Retrieves the details of all storage buckets within an existing product."""
        # if the request doesn't error, it is assured to return a list
        res = self._request("GET", f"{self.url}/bucket")
        return [
            SyncBucket(
                **bucket, _url=self.url, _headers=self.headers, _client=self._client
            )
            for bucket in res.json()
        ]

    def get_bucket(self, id: str) -> SyncBucket:
        """Retrieves the details of an existing storage bucket.

        Parameters
        ----------
        id
            The unique identifier of the bucket you would like to retrieve.
        """
        res = self._request("GET", f"{self.url}/bucket/{id}")
        json = res.json()
        return SyncBucket(
            **json, _url=self.url, _headers=self.headers, _client=self._client
        )

    def create_bucket(
        self, id: str, name: Optional[str] = None, public: bool = False
    ) -> dict[str, str]:
        """Creates a new storage bucket.

        Parameters
        ----------
        id
            A unique identifier for the bucket you are creating.
        name
            A name for the bucket you are creating. If not passed, the id is used as the name as well.
        public
            Whether the bucket you are creating should be publicly accessible. Defaults to False.
        """
        res = self._request(
            "POST",
            f"{self.url}/bucket",
            json={"id": id, "name": name or id, "public": public},
        )
        return res.json()

    def empty_bucket(self, id: str) -> dict[str, str]:
        """Removes all objects inside a single bucket.

        Parameters
        ----------
        id
            The unique identifier of the bucket you would like to empty.
        """
        res = self._request("POST", f"{self.url}/bucket/{id}/empty", json={})
        return res.json()

    def delete_bucket(self, id: str) -> dict[str, str]:
        """Deletes an existing bucket. Note that you cannot delete buckets with existing objects inside. You must first
        `empty()` the bucket.

        Parameters
        ----------
        id
            The unique identifier of the bucket you would like to delete.
        """
        res = self._request("DELETE", f"{self.url}/bucket/{id}", json={})
        return res.json()
