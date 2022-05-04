from typing import Any


__all__ = [
    "ITaskWrapper"
]


class ITaskWrapper:

    __slots__ = ()

    async def execute(self) -> None:
        raise NotImplementedError()

    async def __call__(self) -> Any:
        raise NotImplementedError()
