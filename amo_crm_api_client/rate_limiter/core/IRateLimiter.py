from typing import Callable


__all__ = [
    "IRateLimiter",
]


class IRateLimiter:

    def __call__(self, wrappee: Callable) -> Callable:
        raise NotImplementedError()
