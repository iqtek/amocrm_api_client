from typing import Generic
from typing import List
from typing import TypeVar

from pydantic import Field
from pydantic.generics import GenericModel


__all__ = [
    "Page",
]


T = TypeVar("T")


class Page(GenericModel, Generic[T]):
    page: int = Field(..., alias='_page')
    total_items: int = Field(..., alias='_total_items')
    page_count: int = Field(..., alias='_page_count')
    embedded: List[T] = Field(..., alias='_embedded')
