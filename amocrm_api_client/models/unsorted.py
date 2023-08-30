import typing as t

from pydantic import BaseModel, Field

from .lead import CreateLead


__all__ = [
    "UnsortedCall",
    "UnsortedCallMetadata",
    "Embedded",
]


class Embedded(BaseModel):
    leads: t.List[CreateLead]


class UnsortedCallMetadata(BaseModel):
    uniq: str
    from_: str
    phone: str
    called_at: int
    duration: int
    link: t.Optional[str] = None
    service_code: str
    is_call_event_needed: bool


class UnsortedCall(BaseModel):
    source_uid: str
    source_name: str
    pipeline_id: int
    created_at: int
    metadata: UnsortedCallMetadata
    embedded: t.Optional[Embedded] = Field(None, alias='_embedded')
