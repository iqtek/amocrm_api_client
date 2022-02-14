import time
from asyncio import Future
from typing import (
    Coroutine,
    Optional,
    Callable,
    TypeVar,
    Tuple,
    Type,
    Any,
)
from ..core import (
    TimeoutException,
    IWorkerTask,
)


__all__ = [
    "WorkerTask"
]


T = TypeVar("T")


class WorkerTask(IWorkerTask):

    __slots__ = (
        "__callback",
        "__ttl",
        "__timestamp",
        "__future",
    )

    def __init__(
        self,
        callback: Callable[[], Coroutine[Any, Any, T]],
        ttl: Optional[float] = None,
        thrown_exceptions: Optional[Tuple[Type[BaseException]]] = None,
    ) -> None:
        self.__callback = callback
        self.__timestamp: Optional[float] = None
        if ttl is not None:
            self.__timestamp = time.time()
            self.__ttl = ttl
        else:
            self.__ttl = None
        self.__future = Future()
        self.__thrown_exceptions = thrown_exceptions

    def __is_fit(self) -> bool:
        if self.__ttl is None:
            return True

        curr_time = time.time()
        if curr_time <= self.__timestamp + self.__ttl:
            return True
        return False

    async def execute(self) -> None:
        if not self.__is_fit():
            self.__future.set_exception(TimeoutException())
        try:
            task = self.__callback()
            result = await task
            self.__future.set_result(result)
        except self.__thrown_exceptions as e:
            raise e
        except Exception as e:
            self.__future.set_exception(e)

    async def __call__(self) -> T:
        return await self.__future

    def __le__(self, other):
        return False

    def __eq__(self, other):
        return True
