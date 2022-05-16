from __future__ import annotations

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
        headers: dict[str, str],
    ) -> None:
        headers = {
            "User-Agent": f"supabase-py/storage3 v{__version__}",
            **headers,
        }
        self.session = self._create_session(url, headers)
        super().__init__(self.session)

    def _create_session(
        self,
        base_url: str,
        headers: dict[str, str],
    ) -> AsyncClient:
        return AsyncClient(
            base_url=base_url,
            headers=headers,
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
