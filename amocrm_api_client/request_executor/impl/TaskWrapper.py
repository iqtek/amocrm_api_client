import asyncio
from time import time
import typing as t

from ..core import TtlExpiredException


__all__ = ["TaskWrapper"]


T = t.TypeVar("T")


class TaskWrapper(t.Generic[T]):

    __slots__ = (
        "__callback",
        "__priority",
        "__thrown_exceptions",
        "__ttl",
        "__timestamp",
        "__result",
    )

    def __init__(
        self,
        callback: t.Callable[[], t.Coroutine[t.Any, t.Any, T]],
        priority: int,
        thrown_exceptions: t.Optional[t.Collection[t.Type[Exception]]] = None,
        ttl: t.Optional[float] = None,
    ) -> None:
        self.__callback = callback
        self.__priority = priority
        self.__thrown_exceptions = thrown_exceptions or ()

        self.__ttl: t.Optional[float] = ttl
        self.__timestamp: Optional[float] = None

        if ttl is not None:
            self.__timestamp = time()

        self.__result = asyncio.Future()

    async def execute(self) -> None:
        if self.__ttl is not None and time() <= self.__timestamp + self.__ttl:
            self.__result.set_exception(TtlExpiredException())
            return

        try:
            result = await self.__callback()
            self.__result.set_result(result)
        except self.__thrown_exceptions as exc:
            raise exc
        except Exception as exc:
            self.__result.set_exception(exc)

    async def result(self) -> T:
        return await self.__result

    def __gt__(self, other: 'TaskWrapper'):
        return self.priority > other.priority

    def __lt__(self, other: 'TaskWrapper'):
        return self.priority < other.priority

    def __eq__(self, other: 'TaskWrapper'):
        return self.priority == other.priority
