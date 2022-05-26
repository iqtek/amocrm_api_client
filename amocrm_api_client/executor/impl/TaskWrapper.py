from asyncio import Future
from time import time
from typing import Any
from typing import Callable
from typing import Collection
from typing import Coroutine
from typing import Optional
from typing import Type
from typing import TypeVar

from ..core import ITaskWrapper
from ..core import TimeoutException


__all__ = [
    "TaskWrapper"
]


T = TypeVar("T")


class TaskWrapper(ITaskWrapper):

    __slots__ = (
        "__callback",
        "__thrown_exceptions",
        "__priority",
        "__ttl",
        "__timestamp",
        "__future",
    )

    def __init__(
        self,
        callback: Callable[[], Coroutine[Any, Any, T]],
        priority: int,
        thrown_exceptions: Optional[Collection[Type[Exception]]] = None,
        ttl: Optional[float] = None,
    ) -> None:
        self.__callback = callback
        self.__priority = priority

        self.__ttl = ttl
        self.__timestamp: Optional[float] = None
        if ttl is not None:
            self.__timestamp = time.time()

        self.__future = Future()
        self.__thrown_exceptions = thrown_exceptions or ()

    @property
    def priority(self) -> int:
        return self.__priority

    def __is_fit(self) -> bool:
        if self.__ttl is None:
            return True

        curr_time = time()
        if curr_time <= self.__timestamp + self.__ttl:
            return True

        return False

    async def execute(self) -> None:
        if not self.__is_fit():
            self.__future.set_exception(TimeoutException())
            return

        try:
            result = await self.__callback()
            self.__future.set_result(result)
        except self.__thrown_exceptions as e:
            raise e
        except Exception as e:
            self.__future.set_exception(e)

    async def __call__(self) -> T:
        return await self.__future

    def __gt__(self, other: 'TaskWrapper'):
        return self.priority > other.priority

    def __lt__(self, other: 'TaskWrapper'):
        return self.priority < other.priority

    def __eq__(self, other: 'TaskWrapper'):
        return self.priority == other.priority
