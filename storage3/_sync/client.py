from __future__ import annotations
from ..utils import SyncClient, __version__
from .bucket import SyncStorageBucketAPI
from .file_api import SyncBucketProxy

__all__ = [
    "SyncStorageClient",
]


class SyncStorageClient(SyncStorageBucketAPI):
    """Manage storage buckets and files."""

    def __init__(self, url: str, key: str, headers: dict[str, str] = None) -> None:
        super().__init__(
            url,
            {
                "User-Agent": f"supabase-py/storage3 v{__version__}",
                **self._get_auth_headers(key),
                **(headers or {}),
            },
            SyncClient(),
        )

    def from_(self, id: str) -> SyncBucketProxy:
        """Run a storage file operation.

        Parameters
        ----------
        id
            The unique identifier of the bucket
        """
        return SyncBucketProxy(id, self.url, self.headers, self._client)

    @staticmethod
    def _get_auth_headers(key: str) -> dict[str, str]:
        """Helper method to get auth headers."""
        # What's the corresponding method to get the token
        return {
            "apiKey": key,
            "Authorization": f"Bearer {key}",
        }
