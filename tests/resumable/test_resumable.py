import os


def test_sync_client(sync_client, file, test_bucket):
    client = sync_client

    """Check file was created during configuration phase"""
    assert file is not None

    """Verify test_bucket is not an empty string"""
    assert len(test_bucket.strip()) > 0

    client.resumable.create_unique_link(bucketname=test_bucket, filename=file.name)
    link = client.resumable.get_link(file.name)

    """Verify the link was generated as expected"""
    assert len(link) > 0

    """Check the file is not empty"""
    assert os.stat(file.name).st_size > 0

    """Verify if the file was loaded correctly"""
    client.resumable.upload(file.name)
    bucket = client.get_bucket(test_bucket)
    file_loaded = list(filter(lambda e: e["name"] == file.name, bucket.list()))
    assert len(file_loaded) == 1

    bucket.remove(file.name)


def test_deferred_sync_client(sync_client, file, test_bucket):

    client = sync_client

    """Check file was created during configuration phase"""
    assert file is not None

    """Verify test_bucket is not an empty string"""
    assert len(test_bucket.strip()) > 0

    client.resumable.create_unique_link(bucketname=test_bucket, objectname=file.name)
    link = client.resumable.get_link(file.name)

    """Verify the link was generated as expected"""
    assert len(link) > 0

    """Check the file is not empty"""
    assert os.stat(file.name).st_size > 0

    """Verify if the file was loaded correctly"""
    client.resumable.upload(
        file.name, mb_size=10, upload_defer=True, link=link, objectname=file.name
    )
    bucket = client.get_bucket(test_bucket)
    file_loaded = list(filter(lambda e: e["name"] == file.name, bucket.list()))
    assert len(file_loaded) == 1

    bucket.remove(file.name)


async def test_async_client(async_client, file, test_bucket):
    client = async_client

    """Check file was created during configuration phase"""
    assert file is not None

    """Verify test_bucket is not an empty string"""
    assert len(test_bucket.strip()) > 0

    await client.resumable.create_unique_link(
        bucketname=test_bucket, filename=file.name
    )
    link = client.resumable.get_link(file.name)

    """Verify the link was generated as expected"""
    assert len(link) > 0

    """Check the file is not empty"""
    assert os.stat(file.name).st_size > 0

    """Verify if the file was loaded correctly"""
    await client.resumable.upload(file.name)
    bucket = await client.get_bucket(test_bucket)
    file_loaded = list(filter(lambda e: e["name"] == file.name, await bucket.list()))
    assert len(file_loaded) == 1

    await bucket.remove(file.name)


async def test_deferred_async_client(async_client, file, test_bucket):

    client = async_client

    """Check file was created during configuration phase"""
    assert file is not None

    """Verify test_bucket is not an empty string"""
    assert len(test_bucket.strip()) > 0

    await client.resumable.create_unique_link(
        bucketname=test_bucket, objectname=file.name
    )
    link = client.resumable.get_link(file.name)

    """Verify the link was generated as expected"""
    assert len(link) > 0

    """Check the file is not empty"""
    assert os.stat(file.name).st_size > 0

    """Verify if the file was loaded correctly"""
    await client.resumable.upload(
        file.name, mb_size=10, upload_defer=True, link=link, objectname=file.name
    )
    bucket = await client.get_bucket(test_bucket)
    file_loaded = list(filter(lambda e: e["name"] == file.name, await bucket.list()))
    assert len(file_loaded) == 1

    await bucket.remove(file.name)
