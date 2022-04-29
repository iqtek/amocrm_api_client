__all__ = [
    'IComponent',
]


class IComponent:

    __slots__ = ()

    async def initialize(self) -> None:
        raise NotImplementedError()

    async def deinitialize(self) -> None:
        raise NotImplementedError()
