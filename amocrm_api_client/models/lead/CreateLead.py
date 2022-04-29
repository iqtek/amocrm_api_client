from typing import Optional
from typing import Sequence

from pydantic import BaseModel
from pydantic import Field

from .BaseLead import BaseLead


__all__ = [
    "CreateLead",

]


class Tag(BaseModel):
    id: int


class Contact(BaseModel):
    id: int
    is_main: bool


class Company(BaseModel):
    id: int


class Source(BaseModel):
    external_id: int
    type: str


class CreateEmbedded(BaseModel):
    tags: Optional[Sequence[Tag]] = None
    contacts: Optional[Sequence[Contact]] = None
    companies: Optional[Sequence[Company]] = None
    source: Optional[Source] = None


class CreateLead(BaseLead):
    embedded: Optional[CreateEmbedded] = Field(None, alias='_embedded')
