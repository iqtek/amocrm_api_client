from asyncio import AbstractEventLoop
from asyncio import Task
from asyncio import get_event_loop
from asyncio import CancelledError
from asyncio import PriorityQueue
from asyncio import QueueEmpty
from logging import Logger
from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Optional
from typing import TypeVar

from amocrm_api_client.logger import logger as amocrm_api_client_logger
from amocrm_api_client.make_amocrm_request import ExceedRequestLimitException
from amocrm_api_client.rate_limiter import IRateLimiterDecorator
from amocrm_api_client.repeater import IRepeaterDecorator

from .TaskWrapper import TaskWrapper
from ..core import IExecutorComponent
from ..core import ITaskWrapper
from ..core import TaskPriority


__all__ = [
    "ExecutorComponent",
]


T = TypeVar('T')


class ExecutorComponent(IExecutorComponent):

    __slots__ = (
        "__rate_limiter",
        "__repeater",
        "__queue",
        "__event_loop",
        "__background_task",
        "__logger",
    )

    def __init__(
        self,
        rate_limiter: IRateLimiterDecorator,
        repeater: IRepeaterDecorator,
        queue: Optional[PriorityQueue] = None,
        event_loop: Optional[AbstractEventLoop] = None,
        logger: Optional[Logger] = None,
    ) -> None:
        self.__rate_limiter = rate_limiter
        self.__repeater = repeater
        self.__queue = queue
        self.__event_loop = event_loop
        self.__logger = logger or amocrm_api_client_logger
        self.__background_task: Optional[Task] = None

    async def __task_execute(self, task: ITaskWrapper) -> None:
        task = task.execute
        if self.__rate_limiter:
            task = self.__rate_limiter(task)
        if self.__repeater:
            task = self.__repeater(task)

        await task()

    async def __background_executor(self) -> None:
        try:
            while True:
                amocrm_request_task = await self.__queue.get()
                try:
                    await self.__task_execute(amocrm_request_task)
                except Exception as e:
                    self.__logger.error(f"Execute task error: {e!r}.")
                    self.__queue.task_done()
                self.__queue.task_done()

        except CancelledError:
            try:
                while amo_crm_request_task := self.__queue.get_nowait():
                    try:
                        await self.__task_execute(amo_crm_request_task)
                    except Exception as e:
                        self.__logger.error(f"Execute task error: {e!r}.")
                        self.__queue.task_done()
                    self.__queue.task_done()
            except QueueEmpty:
                self.__logger.info("Remaining queue items processed.")

    async def __call__(
        self,
        task: Callable[[], Coroutine[Any, Any, T]],
        priority: TaskPriority = TaskPriority.Low,
        ttl: Optional[float] = None,
    ) -> T:
        if self.__background_task is None:
            raise RuntimeError(
                "Executor component is not initialize."
            )

        task = TaskWrapper(
            callback=task,
            thrown_exceptions=(ExceedRequestLimitException,),
            priority=priority.value,
            ttl=ttl,
        )
        await self.__queue.put(task)
        self.__logger.debug(
            "Executor component: "
            f"A task: `{task}` with priority: `{priority.value}` "
            f"has been added to the queue."
        )
        return await task()

    async def initialize(self) -> None:
        if self.__event_loop is None:
            self.__event_loop = get_event_loop()

        if self.__queue is None:
            self.__queue = PriorityQueue()

        self.__background_task = self.__event_loop.create_task(
            self.__background_executor()
        )

    async def deinitialize(self) -> None:
        if self.__background_task is not None:
            self.__background_task.cancel()
