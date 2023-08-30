import typing as t

from pydantic import BaseModel, Field

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
    tags: t.Optional[t.List[Tag]] = None
    contacts: t.Optional[t.List[Contact]] = None
    companies: t.Optional[t.List[Company]] = None
    source: t.Optional[Source] = None


class CreateLead(BaseLead):
    embedded: t.Optional[CreateEmbedded] = Field(None, alias='_embedded')
