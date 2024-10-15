from __future__ import annotations

import os

import pytest

from storage3 import AsyncStorageClient, SyncStorageClient


@pytest.fixture
def file() -> str:
    file_name = "test_image.svg"
    file_content = (
        b'<svg width="109" height="113" viewBox="0 0 109 113" fill="none" xmlns="http://www.w3.org/2000/svg"> '
        b'<path d="M63.7076 110.284C60.8481 113.885 55.0502 111.912 54.9813 107.314L53.9738 40.0627L99.1935 '
        b'40.0627C107.384 40.0627 111.952 49.5228 106.859 55.9374L63.7076 110.284Z" fill="url(#paint0_linear)"/> '
        b'<path d="M63.7076 110.284C60.8481 113.885 55.0502 111.912 54.9813 107.314L53.9738 40.0627L99.1935 '
        b'40.0627C107.384 40.0627 111.952 49.5228 106.859 55.9374L63.7076 110.284Z" fill="url(#paint1_linear)" '
        b'fill-opacity="0.2"/> <path d="M45.317 2.07103C48.1765 -1.53037 53.9745 0.442937 54.0434 5.041L54.4849 '
        b'72.2922H9.83113C1.64038 72.2922 -2.92775 62.8321 2.1655 56.4175L45.317 2.07103Z" fill="#3ECF8E"/> <defs>'
        b'<linearGradient id="paint0_linear" x1="53.9738" y1="54.974" x2="94.1635" y2="71.8295"'
        b'gradientUnits="userSpaceOnUse"> <stop stop-color="#249361"/> <stop offset="1" stop-color="#3ECF8E"/> '
        b'</linearGradient> <linearGradient id="paint1_linear" x1="36.1558" y1="30.578" x2="54.4844" y2="65.0806" '
        b'gradientUnits="userSpaceOnUse"> <stop/> <stop offset="1" stop-opacity="0"/> </linearGradient> </defs> </svg>'
    )

    with open(file_name, "wb") as f:
        f.write(file_content)

    return f


@pytest.fixture
def test_bucket() -> str:
    return os.getenv("TEST_BUCKET")


@pytest.fixture
def configure_client():
    url = f'{os.getenv("SUPABASE_URL")}/storage/v1'
    key = os.getenv("SUPABASE_KEY")
    return (url, key)


@pytest.fixture
def sync_client(configure_client) -> SyncStorageClient:
    url, key = configure_client
    client = SyncStorageClient(url, {"apiKey": key, "Authorization": f"Bearer {key}"})
    return client


@pytest.fixture
def async_client(configure_client) -> AsyncStorageClient:
    url, key = configure_client
    client = AsyncStorageClient(url, {"apiKey": key, "Authorization": f"Bearer {key}"})
    return client
