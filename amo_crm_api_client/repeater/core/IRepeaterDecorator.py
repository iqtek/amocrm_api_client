from typing import Callable


__all__ = [
    "IRepeaterDecorator",
]


class IRepeaterDecorator:

    def __call__(self, wrappee: Callable) -> Callable:
        raise NotImplementedError()
