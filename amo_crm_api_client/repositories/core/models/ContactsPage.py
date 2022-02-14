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
from .Contact import Contact


__all__ = [
    "ContactsPage",
]


class Embedded(BaseModel):
    contacts: List[Contact]


class ContactsPage(BaseModel):
    page: int = Field(..., alias='_page')
    embedded: Embedded = Field(..., alias='_embedded')
