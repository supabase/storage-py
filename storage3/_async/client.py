from ..utils import AsyncClient, __version__
from .bucket import AsyncStorageBucketAPI
from .file_api import AsyncBucketProxy

__all__ = [
    "AsyncStorageClient",
]


class AsyncStorageClient(AsyncStorageBucketAPI):
    """Manage storage buckets and files."""

    def __init__(self, url: str, headers: dict[str, str]) -> None:
        super().__init__(
            url,
            {"User-Agent": f"supabase-py/storage3 v{__version__}", **headers},
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
