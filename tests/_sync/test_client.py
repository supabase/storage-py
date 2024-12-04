from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import uuid4

import pytest

from storage3 import SyncStorageClient
from storage3.utils import StorageException

from .. import SyncBucketProxy
from ..utils import SyncClient as HttpxClient
from ..utils import SyncFinalizerFactory

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Callable


# Global variable to track the ids from the buckets created in the tests run
temp_test_buckets_ids = []


@pytest.fixture(scope="module")
def uuid_factory() -> Callable[[], str]:
    def method() -> str:
        """Generate a 8 digits long UUID"""
        return uuid4().hex[:8]

    return method


@pytest.fixture(scope="module", autouse=True)
def delete_left_buckets(
    request: pytest.FixtureRequest,
    storage: SyncStorageClient,
):
    """Ensures no test buckets are left when a test that created a bucket fails"""

    def afinalizer():
        for bucket_id in temp_test_buckets_ids:
            try:
                storage.empty_bucket(bucket_id)
                storage.delete_bucket(bucket_id)
            except StorageException as e:
                # Ignore 404 responses since they mean the bucket was already deleted
                response = e.args[0]
                if response["statusCode"] != 404:
                    raise e
                continue

    request.addfinalizer(SyncFinalizerFactory(afinalizer).finalizer)


def bucket_factory(
    storage: SyncStorageClient, uuid_factory: Callable[[], str], public: bool
) -> str:
    """Creates a test bucket which will be used in the whole storage tests run and deleted at the end"""


@pytest.fixture(scope="module")
def bucket(storage: SyncStorageClient, uuid_factory: Callable[[], str]) -> str:
    """Creates a test bucket which will be used in the whole storage tests run and deleted at the end"""
    bucket_id = uuid_factory()

    # Store bucket_id in global list
    global temp_test_buckets_ids
    temp_test_buckets_ids.append(bucket_id)

    storage.create_bucket(id=bucket_id)

    yield bucket_id

    storage.empty_bucket(bucket_id)
    storage.delete_bucket(bucket_id)

    temp_test_buckets_ids.remove(bucket_id)


@pytest.fixture(scope="module")
def public_bucket(storage: SyncStorageClient, uuid_factory: Callable[[], str]) -> str:
    """Creates a test public bucket which will be used in the whole storage tests run and deleted at the end"""
    bucket_id = uuid_factory()

    # Store bucket_id in global list
    global temp_test_buckets_ids
    temp_test_buckets_ids.append(bucket_id)

    storage.create_bucket(id=bucket_id, options={"public": True})

    yield bucket_id

    storage.empty_bucket(bucket_id)
    storage.delete_bucket(bucket_id)

    temp_test_buckets_ids.remove(bucket_id)


@pytest.fixture(scope="module")
def storage_file_client(storage: SyncStorageClient, bucket: str) -> SyncBucketProxy:
    """Creates the storage file client for the whole storage tests run"""
    yield storage.from_(bucket)


@pytest.fixture(scope="module")
def storage_file_client_public(
    storage: SyncStorageClient, public_bucket: str
) -> SyncBucketProxy:
    """Creates the storage file client for the whole storage tests run"""
    yield storage.from_(public_bucket)


@dataclass
class FileForTesting:
    name: str
    local_path: str
    bucket_folder: str
    bucket_path: str
    mime_type: str
    file_content: bytes


@pytest.fixture
def file(tmp_path: Path, uuid_factory: Callable[[], str]) -> FileForTesting:
    """Creates a different test file (same content but different path) for each test"""
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
    bucket_folder = uuid_factory()
    bucket_path = f"{bucket_folder}/{file_name}"
    file_path = tmp_path / file_name
    with open(file_path, "wb") as f:
        f.write(file_content)

    return FileForTesting(
        name=file_name,
        local_path=str(file_path),
        bucket_folder=bucket_folder,
        bucket_path=bucket_path,
        mime_type="image/svg+xml",
        file_content=file_content,
    )


@pytest.fixture
def two_files(tmp_path: Path, uuid_factory: Callable[[], str]) -> list[FileForTesting]:
    """Creates multiple test files (different content, same bucket/folder path, different file names)"""
    file_name_1 = "test_image_1.svg"
    file_name_2 = "test_image_2.svg"
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
    file_content_2 = (
        b'<svg width="119" height="123" viewBox="0 0 119 123" fill="none" xmlns="http://www.w3.org/2000/svg"> '
        b'<path d="M63.7076 110.284C60.8481 113.885 55.0502 111.912 54.9813 107.314L53.9738 40.0627L99.1935 '
        b'40.0627C107.384 40.0627 111.952 49.5228 106.859 55.9374L63.7076 110.284Z" fill="url(#paint0_linear)"/> '
        b'<path d="M63.7076 110.284C60.8481 113.885 55.0502 111.912 54.9813 107.314L53.9738 40.0627L99.1935 '
        b'40.0627C107.384 40.0627 111.952 49.5228 106.859 55.9374L63.7076 110.284Z" fill="url(#paint1_linear)" '
        b'fill-opacity="0.2"/> <path d="M45.317 2.07103C48.1765 -1.53037 53.9745 0.442937 54.0434 5.041L54.4849 '
        b'72.2922H9.83113C1.64038 72.2922 -2.92775 62.8321 2.1655 56.4175L45.317 2.07103Z" fill="#3FDF8E"/> <defs>'
        b'<linearGradient id="paint0_linear" x1="53.9738" y1="54.974" x2="94.1635" y2="71.8295"'
        b'gradientUnits="userSpaceOnUse"> <stop stop-color="#249361"/> <stop offset="1" stop-color="#3FDF8E"/> '
        b'</linearGradient> <linearGradient id="paint1_linear" x1="36.1558" y1="30.578" x2="54.4844" y2="65.0806" '
        b'gradientUnits="userSpaceOnUse"> <stop/> <stop offset="1" stop-opacity="0"/> </linearGradient> </defs> </svg>'
    )
    bucket_folder = uuid_factory()
    bucket_path_1 = f"{bucket_folder}/{file_name_1}"
    bucket_path_2 = f"{bucket_folder}/{file_name_2}"
    file_path_1 = tmp_path / file_name_1
    file_path_2 = tmp_path / file_name_2
    with open(file_path_1, "wb") as f:
        f.write(file_content)
    with open(file_path_2, "wb") as f:
        f.write(file_content_2)

    return [
        FileForTesting(
            name=file_name_1,
            local_path=str(file_path_1),
            bucket_folder=bucket_folder,
            bucket_path=bucket_path_1,
            mime_type="image/svg+xml",
            file_content=file_content,
        ),
        FileForTesting(
            name=file_name_2,
            local_path=str(file_path_2),
            bucket_folder=bucket_folder,
            bucket_path=bucket_path_2,
            mime_type="image/svg+xml",
            file_content=file_content_2,
        ),
    ]


@pytest.fixture
def multi_file(tmp_path: Path, uuid_factory: Callable[[], str]) -> list[FileForTesting]:
    """Creates multiple test files (same content, same bucket/folder path, different file names)"""
    file_name_1 = "test_image_1.svg"
    file_name_2 = "test_image_2.svg"
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
    bucket_folder = uuid_factory()
    bucket_path_1 = f"{bucket_folder}/{file_name_1}"
    bucket_path_2 = f"{bucket_folder}/{file_name_2}"
    file_path_1 = tmp_path / file_name_1
    file_path_2 = tmp_path / file_name_2
    with open(file_path_1, "wb") as f:
        f.write(file_content)
    with open(file_path_2, "wb") as f:
        f.write(file_content)

    return [
        FileForTesting(
            name=file_name_1,
            local_path=str(file_path_1),
            bucket_folder=bucket_folder,
            bucket_path=bucket_path_1,
            mime_type="image/svg+xml",
            file_content=file_content,
        ),
        FileForTesting(
            name=file_name_2,
            local_path=str(file_path_2),
            bucket_folder=bucket_folder,
            bucket_path=bucket_path_2,
            mime_type="image/svg+xml",
            file_content=file_content,
        ),
    ]


# TODO: Test create_bucket, delete_bucket, empty_bucket, list_buckets, fileAPI.list before upload test


def test_client_upload(
    storage_file_client: SyncBucketProxy, file: FileForTesting
) -> None:
    """Ensure we can upload files to a bucket"""
    storage_file_client.upload(
        file.bucket_path, file.local_path, {"content-type": file.mime_type}
    )

    image = storage_file_client.download(file.bucket_path)
    files = storage_file_client.list(file.bucket_folder)
    image_info = next((f for f in files if f.get("name") == file.name), None)

    assert image == file.file_content
    assert image_info.get("metadata", {}).get("mimetype") == file.mime_type


def test_client_update(
    storage_file_client: SyncBucketProxy,
    two_files: list[FileForTesting],
) -> None:
    """Ensure we can upload files to a bucket"""
    storage_file_client.upload(
        two_files[0].bucket_path,
        two_files[0].local_path,
        {"content-type": two_files[0].mime_type},
    )

    storage_file_client.update(
        two_files[0].bucket_path,
        two_files[1].local_path,
        {"content-type": two_files[1].mime_type},
    )

    image = storage_file_client.download(two_files[0].bucket_path)
    file_list = storage_file_client.list(two_files[0].bucket_folder)
    image_info = next(
        (f for f in file_list if f.get("name") == two_files[0].name), None
    )

    assert image == two_files[1].file_content
    assert image_info.get("metadata", {}).get("mimetype") == two_files[1].mime_type


@pytest.mark.parametrize(
    "path", ["foobar.txt", "example/nested.jpg", "/leading/slash.png"]
)
def test_client_create_signed_upload_url(
    storage_file_client: SyncBucketProxy, path: str
) -> None:
    """Ensure we can create signed URLs to upload files to a bucket"""
    data = storage_file_client.create_signed_upload_url(path)
    assert data["path"] == path
    assert data["token"]
    expected_url = f"{storage_file_client._client.base_url}/object/upload/sign/{storage_file_client.id}/{path.lstrip('/')}"
    assert data["signed_url"].startswith(expected_url)


def test_client_upload_to_signed_url(
    storage_file_client: SyncBucketProxy, file: FileForTesting
) -> None:
    """Ensure we can upload to a signed URL"""
    data = storage_file_client.create_signed_upload_url(file.bucket_path)
    assert data["path"]
    storage_file_client.upload_to_signed_url(
        data["path"], data["token"], file.file_content, {"content-type": file.mime_type}
    )
    image = storage_file_client.download(file.bucket_path)
    files = storage_file_client.list(file.bucket_folder)
    image_info = next((f for f in files if f.get("name") == file.name), None)

    assert image == file.file_content
    assert image_info.get("metadata", {}).get("mimetype") == file.mime_type


def test_client_create_signed_url(
    storage_file_client: SyncBucketProxy, file: FileForTesting
) -> None:
    """Ensure we can create a signed url for a file in a bucket"""
    storage_file_client.upload(
        file.bucket_path, file.local_path, {"content-type": file.mime_type}
    )

    signed_url = (storage_file_client.create_signed_url(file.bucket_path, 10))[
        "signedURL"
    ]

    with HttpxClient() as client:
        response = client.get(signed_url)
    response.raise_for_status()

    assert response.content == file.file_content


def test_client_create_signed_urls(
    storage_file_client: SyncBucketProxy, multi_file: list[FileForTesting]
) -> None:
    """Ensure we can create signed urls for files in a bucket"""
    paths = []
    for file in multi_file:
        paths.append(file.bucket_path)
        storage_file_client.upload(
            file.bucket_path, file.local_path, {"content-type": file.mime_type}
        )

    signed_urls = storage_file_client.create_signed_urls(paths, 10)

    with HttpxClient() as client:
        for url in signed_urls:
            response = client.get(url["signedURL"])
            response.raise_for_status()
            assert response.content == multi_file[0].file_content


def test_client_get_public_url(
    storage_file_client_public: SyncBucketProxy, file: FileForTesting
) -> None:
    """Ensure we can get the public url of a file in a bucket"""
    storage_file_client_public.upload(
        file.bucket_path, file.local_path, {"content-type": file.mime_type}
    )

    public_url = storage_file_client_public.get_public_url(file.bucket_path)

    with HttpxClient(timeout=None) as client:
        response = client.get(public_url)
    response.raise_for_status()

    assert response.content == file.file_content


def test_client_info(
    storage_file_client_public: SyncBucketProxy, file: FileForTesting
) -> None:
    """Ensure we can get the public url of a file in a bucket"""
    storage_file_client_public.upload(
        file.bucket_path, file.local_path, {"content-type": file.mime_type}
    )

    info = storage_file_client_public.info(file.bucket_path)
    assert 'metadata' in info.keys()
    assert info['name'] == file.bucket_path
    assert info['content_type'] == file.mime_type


def test_client_exists(
    storage_file_client_public: SyncBucketProxy, file: FileForTesting
) -> None:
    """Ensure we can get the public url of a file in a bucket"""
    storage_file_client_public.upload(
        file.bucket_path, file.local_path, {"content-type": file.mime_type}
    )

    exists = storage_file_client_public.exists(file.bucket_path)

    assert exists
