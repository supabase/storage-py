from __future__ import annotations

from typing import Union

from httpx import Timeout

from ..utils import AsyncClient, __version__
from .bucket import AsyncStorageBucketAPI
from .file_api import AsyncBucketProxy

__all__ = [
    "AsyncStorageClient",
]


class AsyncStorageClient(AsyncStorageBucketAPI):
    """Manage storage buckets and files."""

    def __init__(
        self,
        url: str,
        key: str,
        headers: dict[str, str] = None,
        timeout: Union[int, float, Timeout] = 5,
    ) -> None:
        headers = {
            "User-Agent": f"supabase-py/storage3 v{__version__}",
            **self._get_auth_headers(key),
            **(headers or {}),
        }
        self.session = self.create_session(url, headers, timeout)
        super().__init__(self.session)

    def create_session(
        self,
        base_url: str,
        headers: dict[str, str],
        timeout: Union[int, float, Timeout],
    ) -> AsyncClient:
        return AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
        )

    async def __aenter__(self) -> AsyncStorageClient:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self.session.aclose()

    def from_(self, id: str) -> AsyncBucketProxy:
        """Run a storage file operation.

        Parameters
        ----------
        id
            The unique identifier of the bucket
        """
        return AsyncBucketProxy(id, self._client)

    @staticmethod
    def _get_auth_headers(key: str) -> dict[str, str]:
        """Helper method to get auth headers."""
        # What's the corresponding method to get the token
        return {
            "apiKey": key,
            "Authorization": f"Bearer {key}",
        }
