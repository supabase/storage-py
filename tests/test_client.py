from typing import Dict

import pytest
from httpx import Timeout

from storage3 import AsyncStorageClient, SyncStorageClient, create_client
from storage3.constants import DEFAULT_TIMEOUT


@pytest.fixture
def valid_url() -> str:
    return "https://example.com/storage/v1"


@pytest.fixture
def valid_headers() -> Dict[str, str]:
    return {"Authorization": "Bearer test_token", "apikey": "test_api_key"}


def test_create_async_client(valid_url, valid_headers):
    client = create_client(url=valid_url, headers=valid_headers, is_async=True)

    assert isinstance(client, AsyncStorageClient)
    assert all(
        client._client.headers[key] == value for key, value in valid_headers.items()
    )
    assert client._client.timeout == Timeout(DEFAULT_TIMEOUT)


def test_create_sync_client(valid_url, valid_headers):
    client = create_client(url=valid_url, headers=valid_headers, is_async=False)

    assert isinstance(client, SyncStorageClient)
    assert all(
        client._client.headers[key] == value for key, value in valid_headers.items()
    )
    assert client._client.timeout == Timeout(DEFAULT_TIMEOUT)


def test_custom_timeout(valid_url, valid_headers):
    custom_timeout = 30

    async_client = create_client(
        url=valid_url, headers=valid_headers, is_async=True, timeout=custom_timeout
    )
    assert async_client._client.timeout == Timeout(custom_timeout)

    sync_client = create_client(
        url=valid_url, headers=valid_headers, is_async=False, timeout=custom_timeout
    )
    assert sync_client._client.timeout == Timeout(custom_timeout)


def test_type_hints():
    from typing import Union, get_type_hints

    hints = get_type_hints(create_client)

    assert hints["url"] == str
    assert hints["headers"] == dict[str, str]
    assert hints["is_async"] == bool
    assert hints["timeout"] == int
    assert hints["return"] == Union[AsyncStorageClient, SyncStorageClient]
