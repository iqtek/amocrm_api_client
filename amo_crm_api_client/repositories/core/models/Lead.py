from datetime import (
    datetime
)
from typing import (
    Optional,
    List,
)
from pydantic import (
    BaseModel,
    Field,
)
from .Tag import Tag


__all__ = [
    "Lead",
]


class Contact(BaseModel):
    id: int


class Company(BaseModel):
    id: int


class Embedded(BaseModel):
    tags: Optional[List[Tag]]
    contacts: Optional[List[Contact]]
    companies: Optional[List[Company]]


class Lead(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    pipeline_id: int
    closed_at: Optional[datetime] = None
    responsible_user_id: int
    status_id: int
    name: str
    tags: Optional[List[Tag]] = None
    embedded: Embedded = Field(..., alias='_embedded')
