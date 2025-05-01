from __future__ import annotations

from typing import Optional

from storage3.constants import DEFAULT_TIMEOUT

from ..utils import AsyncClient
from ..version import __version__
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
        timeout: int = DEFAULT_TIMEOUT,
        verify: bool = True,
        proxy: Optional[str] = None,
        http_client: Optional[AsyncClient] = None,
    ) -> None:
        headers = {
            "User-Agent": f"supabase-py/storage3 v{__version__}",
            **headers,
        }
        self.session = self._create_session(
            url, headers, timeout, verify, proxy, http_client
        )
        super().__init__(self.session)

    def _create_session(
        self,
        base_url: str,
        headers: dict[str, str],
        timeout: int,
        verify: bool = True,
        proxy: Optional[str] = None,
        http_client: Optional[AsyncClient] = None,
    ) -> AsyncClient:
        if http_client is not None:
            http_client.base_url = base_url
            http_client.headers = headers
            return http_client

        return AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
            proxy=proxy,
            verify=bool(verify),
            follow_redirects=True,
            http2=True,
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
