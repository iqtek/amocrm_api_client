from pydantic import BaseModel
from pydantic import Field

from typing import List

from .PipelineStatus import PipelineStatus


__all__ = [
    "Pipeline",
]


class Embedded(BaseModel):
    statuses: List[PipelineStatus]


class Pipeline(BaseModel):

    id: int
    name: str
    sort: int
    is_main: bool
    is_unsorted_on: bool
    is_archive: bool
    account_id: int
    embedded: Embedded = Field(..., alias='_embedded')
