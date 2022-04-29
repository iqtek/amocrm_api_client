from pydantic import BaseModel


__all__ = [
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
