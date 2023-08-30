import typing as t

from pydantic import BaseModel, Field


__all__ = [
    "Pipeline",
    "PipelineStatus",
]


class PipelineStatus(BaseModel):
    id: int
    name: str
    sort: int
    is_editable: bool
    pipeline_id: int
    color: str
    type: int
    account_id: int



class Embedded(BaseModel):
    statuses: t.List[PipelineStatus]


class Pipeline(BaseModel):
    id: int
    name: str
    sort: int
    is_main: bool
    is_unsorted_on: bool
    is_archive: bool
    account_id: int
    embedded: Embedded = Field(..., alias='_embedded')
