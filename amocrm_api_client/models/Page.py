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
    embedded: List[T] = Field(..., alias='_embedded')
