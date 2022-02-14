from typing import (
    Coroutine,
    Callable,
    Optional,
    TypeVar,
    Any,
)
from amo_crm_api_client.component import IComponent
from .TaskPriority import TaskPriority


__all__ = [
    "IWorkerExecutorComponent",
]


T = TypeVar('T')


class IWorkerExecutorComponent(IComponent):

    async def __call__(
        self,
        task: Callable[[], Coroutine[Any, Any, T]],
        priority: Optional[TaskPriority] = None,
        ttl: Optional[float] = None,
    ) -> T:
        raise NotImplementedError()

    async def initialize(self) -> None:
        raise NotImplementedError()

    async def deinitialize(self) -> None:
        raise NotImplementedError()
