from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from ..lead import CreateLead


__all__ = [
    "UnsortedCall",
    "UnsortedCallMetadata",
    "Embedded",
]


class Embedded(BaseModel):
    leads: List[CreateLead]


class UnsortedCallMetadata(BaseModel):
    uniq: str
    from_: str
    phone: str
    called_at: int
    duration: int
    link: Optional[str] = None
    service_code: str
    is_call_event_needed: bool


class UnsortedCall(BaseModel):
    source_uid: str
    source_name: str
    pipeline_id: int
    created_at: int
    metadata: UnsortedCallMetadata
    embedded: Optional[Embedded] = Field(None, alias='_embedded')
