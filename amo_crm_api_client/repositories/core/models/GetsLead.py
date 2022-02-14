from datetime import datetime
from typing import (
    Optional,
    List,
)
from pydantic import (
    BaseModel,
    Field,
)

__all__ = [
    "GetsLead",
]


class Contact(BaseModel):
    id: int


class Company(BaseModel):
    id: int


class AmoLead(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None
    responsible_user_id: int
    name: str


class Embedded(BaseModel):
    leads: List[AmoLead]


class GetsLead(BaseModel):
    page: int = Field(..., alias='_page')
    embedded: Embedded = Field(..., alias='_embedded')
