import typing as t

from pydantic import Field
from pydantic.generics import GenericModel


__all__ = [
    "Page",
]


T = t.TypeVar("T")


class Page(GenericModel, t.Generic[T]):
    page: int = Field(..., alias='_page')
    total_items: t.Optional[int] = Field(None, alias='_total_items')
    page_count: t.Optional[int] = Field(None, alias='_page_count')
    embedded: t.List[T] = Field(..., alias='_embedded')
