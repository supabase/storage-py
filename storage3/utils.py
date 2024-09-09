from httpx import AsyncClient as AsyncClient  # noqa: F401
from httpx import Client as BaseClient

from .types import FileInfo


class SyncClient(BaseClient):
    def aclose(self) -> None:
        self.close()


class StorageException(Exception):
    """Error raised when an operation on the storage API fails."""


class FileStore:
    """This class serves as storage of files to be sent in the resumable upload workflow"""

    def __init__(self):
        self.storage = {}

    def mark_file(self, file_info: FileInfo):
        """Store file metadata in a in-memory storage"""
        self.storage[file_info["name"]] = file_info

    def get_file_info(self, filename):
        return self.storage[filename]

    def update_file_headers(self, filename, key, value):
        file = self.get_file_info(filename)
        file["headers"][key] = value

    def get_file_headers(self, filename):
        return self.get_file_info(filename)["headers"]

    def get_file_storage_link(self, filename):
        return self.get_file_info(filename)["headers"]["link"]

    def open_file(self, filename: str, offset: int):
        """Open file in the specified offset
        Parameters
        ----------
        filename
            local file
        offset
            set current the file-pointer
        """
        file = open(filename, "rb")
        file.seek(int(offset))
        return file

    def close_file(self, filename):
        filename.close()

    def remove_file(self, filename: str):
        del self.storage[filename]

    def get_link(self, filename: str):
        return self.storage[filename]["link"]
