import typing as t

from amocrm_api_client.models import Page


__all__ = ["Paginable"]


T = t.TypeVar('T')


class Paginable(t.Generic[T]):

    __slots__ = ()

    async def get_page(
        self,
        _with: t.Optional[t.Collection[str]] = None,
        page: int = 1,
        limit: int = 250,
        query: t.Optional[t.Union[str, int]] = None,
    ) -> Page[T]:
        raise NotImplementedError()
