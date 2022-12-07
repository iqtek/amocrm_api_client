from typing import Generic
from typing import List
from typing import TypeVar
from typing import Optional
from pydantic import Field
from pydantic.generics import GenericModel


__all__ = [
    "Page",
]


T = TypeVar("T")


class Page(GenericModel, Generic[T]):
    page: int = Field(..., alias='_page')
    total_items: Optional[int] = Field(None, alias='_total_items')
    page_count: Optional[int] = Field(None, alias='_page_count')
    embedded: List[T] = Field(..., alias='_embedded')
