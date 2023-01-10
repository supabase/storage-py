from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

import dateutil.parser
from typing_extensions import Literal, TypedDict

RequestMethod = Literal["GET", "POST", "DELETE", "PUT", "HEAD"]


@dataclass
class BaseBucket:
    """Represents a file storage bucket."""

    id: str
    name: str
    owner: str
    public: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        # created_at and updated_at are returned by the API as ISO timestamps
        # so we convert them to datetime objects
        self.created_at = dateutil.parser.isoparse(self.created_at)  # type: ignore
        self.updated_at = dateutil.parser.isoparse(self.updated_at)  # type: ignore


# used in bucket.list method's option parameter
class _sortByType(TypedDict):
    column: str
    order: Literal["asc", "desc"]


class ListBucketFilesOptions(TypedDict):
    limit: int
    offset: int
    sortBy: _sortByType


class TransformOptions(TypedDict):
    height: Optional[float]
    width: Optional[float]
    resize: Optional[Union[Literal["cover"], Literal["contain"], Literal["fill"]]]


class CreateSignedURLOptions(TypedDict):
    download: Optional[Union[str, bool]]
    transform: Optional[TransformOptions]
