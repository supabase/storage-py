from __future__ import annotations

from typing import Literal, Union, overload

from storage3._async import AsyncStorageClient
from storage3._sync import SyncStorageClient

__version__ = "0.1.1"
__all__ = ["create_client", "StorageException"]


@overload
def create_client(
    url: str, headers: dict[str, str], *, is_async: Literal[True]
) -> AsyncStorageClient:
    ...


@overload
def create_client(
    url: str, headers: dict[str, str], *, is_async: Literal[False]
) -> SyncStorageClient:
    ...


def create_client(
    url: str, headers: dict[str, str], *, is_async: bool
) -> Union[AsyncStorageClient, SyncStorageClient]:
    if is_async:
        return AsyncStorageClient(url, headers)
    else:
        return SyncStorageClient(url, headers)


class StorageException(Exception):
    """Error raised when an operation on the storage API fails."""
