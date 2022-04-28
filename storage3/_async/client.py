from __future__ import annotations

from ..utils import AsyncClient, __version__
from .bucket import AsyncStorageBucketAPI
from .file_api import AsyncBucketProxy

__all__ = [
    "AsyncStorageClient",
]


class AsyncStorageClient(AsyncStorageBucketAPI):
    """Manage storage buckets and files."""

    def __init__(self, url: str, key: str, headers: dict[str, str] = None) -> None:
        super().__init__(
            url,
            {
                "User-Agent": f"supabase-py/storage3 v{__version__}",
                **self._get_auth_headers(key),
                **(headers or {}),
            },
            AsyncClient(),
        )

    def from_(self, id: str) -> AsyncBucketProxy:
        """Run a storage file operation.

        Parameters
        ----------
        id
            The unique identifier of the bucket
        """
        return AsyncBucketProxy(id, self.url, self.headers, self._client)

    @staticmethod
    def _get_auth_headers(key: str) -> dict[str, str]:
        """Helper method to get auth headers."""
        # What's the corresponding method to get the token
        return {
            "apiKey": key,
            "Authorization": f"Bearer {key}",
        }
