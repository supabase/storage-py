from ..utils import SyncClient
from .bucket import SyncStorageBucketAPI
from .file_api import SyncBucketProxy

__all__ = [
    "SyncStorageClient",
]


class SyncStorageClient(SyncStorageBucketAPI):

    """Manage storage buckets and files."""

    def __init__(self, url: str, headers: dict[str, str]) -> None:

        super().__init__(url, headers, SyncClient())

    def from_(self, id: str) -> SyncBucketProxy:

        """Run a storage file operation.



        Parameters

        ----------

        id

            The unique identifier of the bucket

        """

        return SyncBucketProxy(id, self.url, self.headers, self._client)
