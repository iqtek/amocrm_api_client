from typing import Callable


__all__ = [
    "IRateLimiterDecorator",
]


class IRateLimiterDecorator:

    __slots__ = ()

    def __call__(self, wrappee: Callable) -> Callable:
        raise NotImplementedError()
