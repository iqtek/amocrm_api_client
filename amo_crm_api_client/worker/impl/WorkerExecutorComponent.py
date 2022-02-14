from asyncio import PriorityQueue, AbstractEventLoop, CancelledError, QueueEmpty
from typing import (
    Coroutine,
    Optional,
    Callable,
    TypeVar,
    Any,
)
from amo_crm_api_client.logger import get_logger, ILogger
from amo_crm_api_client.make_amocrm_request import ExceedRequestLimitException
from amo_crm_api_client.rate_limiter import IRateLimiter
from amo_crm_api_client.repeater import IRepeaterDecorator
from .WorkerTask import WorkerTask
from ..core import IWorkerExecutorComponent, IWorkerTask, TaskPriority


__all__ = [
    "WorkerExecutorComponent",
]


T = TypeVar('T')


class WorkerExecutorComponent(IWorkerExecutorComponent):

    __slots__ = (
        "__logger",
        "__rate_limiter",
        "__event_loop",
        "__queue",
        "__background_task",
        "__is_run",
    )

    def __init__(
        self,
        queue: Optional[PriorityQueue] = None,
        logger: Optional[ILogger] = None,
        rate_limiter: Optional[IRateLimiter] = None,
        repeater: Optional[IRepeaterDecorator] = None,
        event_loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        self.__logger = logger or get_logger()
        self.__rate_limiter = rate_limiter
        self.__repeater = repeater
        self.__event_loop = event_loop or get_event_loop()
        self.__queue = queue or PriorityQueue(loop=self.__event_loop)
        self.__background_task: Optional[Task] = None
        self.__is_run: bool = False

    async def __queue_put(self, task: IWorkerTask, priority: TaskPriority = None) -> None:
        if not priority:
            priority = TaskPriority.Low
        await self.__queue.put(
            (priority.value, task)
        )
        await self.__logger.debug(
            "WorkerExecutor: "
            f"An element={task} with priority={priority.value} "
            f"has been added to the queue."
        )

    async def __queue_get(self) -> IWorkerTask:
        data = await self.__queue.get()
        return data[1]

    def __queue_get_nowait(self) -> IWorkerTask:
        data = self.__queue.get_nowait()
        return data[1]

    async def __task_execute(self, task: IWorkerTask) -> None:
        task = task.execute
        if self.__rate_limiter:
            task = self.__rate_limiter(task)
        if self.__repeater:
            task = self.__repeater(task)

        await task()

    async def __background_work(self) -> None:
        try:
            while True:
                amo_crm_request_task = await self.__queue_get()
                try:
                    await self.__task_execute(amo_crm_request_task)
                except Exception as e:
                    await self.__logger.error(f'Execute task error, {e}')
                self.__queue.task_done()

        except CancelledError:
            try:
                while amo_crm_request_task := self.__queue_get_nowait():
                    try:
                        await self.__task_execute(amo_crm_request_task)
                    except Exception as e:
                        await self.__logger.error(
                            f"Worker: error of calling {amo_crm_request_task},{e}"
                        )
                        self.__queue.task_done()
                    self.__queue.task_done()
            except QueueEmpty:
                await self.__logger.debug("Remaining queue items processed.")

    async def __call__(
        self,
        task: Callable[[], Coroutine[Any, Any, T]],
        priority: Optional[TaskPriority] = None,
        ttl: Optional[float] = None,
    ) -> T:
        if not self.__is_run:
            raise RuntimeError(
                "Worker component is not initialize."
            )
        task = WorkerTask(
            callback=task,
            ttl=ttl,
            thrown_exceptions=(
                ExceedRequestLimitException,
            )
        )
        await self.__queue_put(task, priority=priority)
        return await task()

    async def initialize(self) -> None:
        self.__background_task = self.__event_loop.create_task(
            self.__background_work()
        )
        self.__is_run = True

    async def deinitialize(self) -> None:
        self.__is_run = False
        if self.__background_task is not None:
            self.__background_task.cancel()
