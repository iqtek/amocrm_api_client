from typing import Collection
from typing import Generic
from typing import Optional
from typing import TypeVar
from typing import Union

from amocrm_api_client.models import Page


__all__ = [
    "IPaginable",
]


T = TypeVar('T')


class IPaginable(Generic[T]):

    __slots__ = ()

    async def get_page(
        self,
        _with: Optional[Collection[str]] = None,
        page: int = 1,
        limit: int = 250,
        query: Optional[Union[str, int]] = None,
    ) -> Page[T]:
        raise NotImplementedError()
