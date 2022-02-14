from typing import List
from pydantic import BaseModel, Field


__all__ = [
    "UsersPage",
    "User",
]


class User(BaseModel):
    id: int
    name: str
    email: str


class Embedded(BaseModel):
    users: List[User]


class UsersPage(BaseModel):
    total_items: int = Field(..., alias='_total_items')
    page: int = Field(..., alias='_page')
    page_count: int = Field(..., alias='_page_count')
    embedded: Embedded = Field(..., alias='_embedded')

