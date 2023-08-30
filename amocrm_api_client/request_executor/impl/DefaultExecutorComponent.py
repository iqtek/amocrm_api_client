import asyncio
from logging import Logger
import typing as t

from amocrm_api_client.utils import amocrm_api_client_logger
from amocrm_api_client.make_amocrm_request import ExceedRequestLimitException

from ..core import ExecutorComponent

from .TaskWrapper import TaskWrapper


__all__ = ["DefaultExecutorComponent"]


T = t.TypeVar('T')


class DefaultExecutorComponent(ExecutorComponent):

    __slots__ = (
        "__task_decorator",
        "__logger",
        "__queue",
        "__background_task",
    )

    def __init__(
        self,
        task_decorator: t.Optional[t.Callable] = None,
        task_thrown_exceptions: t.Optional[t.Callable] = None,
        logger: t.Optional[Logger] = None,
    ) -> None:
        self.__task_decorator = task_decorator or (lambda x: x)
        self.__logger = logger or amocrm_api_client_logger
        self.__queue: asyncio.PriorityQueue[TaskWrapper] = asyncio.PriorityQueue()
        self.__background_task: t.Optional[asyncio.Task] = None

    async def __execute_task(self, task_wrapper: TaskWrapper) -> None:
        try:
            await self.__task_decorator(task_wrapper.execute)()
        except Exception as exc:
            self.__logger.error(f"Execute task error.", exc_info=exc)

    async def __background_executor(self) -> None:
        try:
            while True:
                task_wrapper = await self.__queue.get()
                await self.__execute_task(task_wrapper)
                self.__queue.task_done()
        except asyncio.CancelledError:
            try:
                while task_wrapper := self.__queue.get_nowait():
                    await self.__execute_task(task_wrapper)
                    self.__queue.task_done()
            except asyncio.QueueEmpty:
                self.__logger.info("Remaining queue items processed.")

    async def __call__(
        self,
        task: t.Callable[[], t.Coroutine[t.Any, t.Any, T]],
        priority: int = 0,
        ttl: t.Optional[float] = None,
    ) -> T:
        if self.__background_task is None:
            raise RuntimeError("Executor component is not initialized.")

        task = TaskWrapper(
            callback=task,
            thrown_exceptions=(ExceedRequestLimitException,),
            priority=priority,
            ttl=ttl,
        )
        await self.__queue.put(task)
        return await task.result()

    async def initialize(self) -> None:
        self.__background_task = asyncio.create_task(self.__background_executor())

    async def deinitialize(self) -> None:
        if self.__background_task is not None:
            self.__background_task.cancel()