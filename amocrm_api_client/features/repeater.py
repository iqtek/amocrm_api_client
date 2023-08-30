import asyncio
import functools as ft
import typing as t

import pydantic


__all__ = [
    "RepeaterConfig",
    "RepeaterDecorator"
]


T = t.TypeVar('T', bound=t.Callable[[], t.Awaitable])


class RepeaterConfig(pydantic.BaseModel):
    tries: pydantic.PositiveInt = 5
    min_delay: pydantic.NonNegativeFloat = 0.4
    max_delay: pydantic.NonNegativeFloat = 15.0
    factor: pydantic.NonNegativeFloat = 2


class RepeaterDecorator:

    __slots__ = (
        "__config",
        "__trigger_exceptions",
    )

    def __init__(
        self,
        config: RepeaterConfig,
        trigger_exceptions: t.Collection[t.Type[BaseException]],
    ) -> None:
        self.__config = config
        self.__trigger_exceptions = trigger_exceptions

    def __call__(self, func: T) -> T:
        @ft.wraps(func)
        async def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            for i in range(self.__config.tries):
                try:
                    return await func(*args, **kwargs)
                except self.__trigger_exceptions as e:
                    if i + 1 == self.__config.tries:
                        raise e

                delay = min(self.__config.min_delay * self.__config.factor ** i, self.__config.max_delay)
                await asyncio.sleep(delay)

        return wrapper
