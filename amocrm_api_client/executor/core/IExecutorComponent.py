from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Optional
from typing import TypeVar

from amocrm_api_client.component import IComponent

from .TaskPriority import TaskPriority


__all__ = [
    "IExecutorComponent",
]


T = TypeVar('T')


class IExecutorComponent(IComponent):

    __slots__ = ()

    async def __call__(
        self,
        task: Callable[[], Coroutine[Any, Any, T]],
        priority: Optional[TaskPriority] = TaskPriority.Low,
        ttl: Optional[float] = None,
    ) -> T:
        raise NotImplementedError()

    async def initialize(self) -> None:
        raise NotImplementedError()

    async def deinitialize(self) -> None:
        raise NotImplementedError()
