import typing as t


__all__ = ["ExecutorComponent"]


T = t.TypeVar('T')


class ExecutorComponent:

    __slots__ = ()

    async def initialize(self) -> None:
        raise NotImplementedError()

    async def __call__(
        self,
        task: t.Callable[[], t.Coroutine[t.Any, t.Any, T]],
        priority: int = 0,
        ttl: t.Optional[float] = None,
    ) -> T:
        raise NotImplementedError()

    async def deinitialize(self) -> None:
        raise NotImplementedError()
