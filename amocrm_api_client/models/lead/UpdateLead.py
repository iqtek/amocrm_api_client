import typing as t

from pydantic import BaseModel
from pydantic import Field

from .BaseLead import BaseLead
from ..tag import Tag


class UpdateEmbedded(BaseModel):
    tags: t.Optional[t.List[Tag]] = None


class UpdateLead(BaseLead):
    id: int
    embedded: t.Optional[UpdateEmbedded] = Field(None, alias='_embedded')
