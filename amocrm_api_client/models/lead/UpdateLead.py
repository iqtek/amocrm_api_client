from typing import Optional
from typing import Sequence

from pydantic import BaseModel
from pydantic import Field

from .BaseLead import BaseLead
from ..Tag import Tag


class UpdateEmbedded(BaseModel):
    tags: Optional[Sequence[Tag]] = None


class UpdateLead(BaseLead):
    id: int
    embedded: Optional[UpdateEmbedded] = Field(None, alias='_embedded')
