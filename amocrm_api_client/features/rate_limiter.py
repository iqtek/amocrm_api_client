import asyncio
import functools as ft
from time import time
import typing as t

import pydantic


__all__ = [
    "RateLimiterConfig",
    "RateLimiterDecorator",
]


T = t.TypeVar('T', bound=t.Callable[[], t.Awaitable])


class RateLimiterConfig(pydantic.BaseModel):
    period: pydantic.PositiveFloat = 1
    max_request_count: pydantic.PositiveInt = 7  # Maximum requests per period.
    forced_delay: pydantic.PositiveInt = 1


class RateLimiterDecorator:

    __slots__ = (
        "__config",
        "__trigger_exceptions",
        "__request_counter",
        "__last_interval_start",
        "__last_interval_start",
        "__over_speed_timestamp",
        "__interval_start",
    )

    def __init__(
        self,
        config: RateLimiterConfig,
        trigger_exceptions: t.Collection[t.Type[BaseException]],
    ) -> None:
        self.__config = config
        self.__trigger_exceptions = trigger_exceptions

        self.__request_counter = 0
        self.__last_interval_start = 0

        # Time of last exceeded number of requests.
        self.__over_speed_timestamp: float = 0

    def __call__(self, wrappee: T) -> T:
        @ft.wraps(wrappee)
        async def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            curr_time = time()

            forced_delay = self.__over_speed_timestamp + \
                self.__config.forced_delay - curr_time

            if forced_delay > 0:
                await asyncio.sleep(forced_delay)

            self.__interval_start = curr_time // self.__config.period
            if self.__interval_start == self.__last_interval_start:
                self.__request_counter += 1
            else:
                self.__last_interval_start = self.__interval_start
                self.__request_counter = 1

            if self.__request_counter >= self.__config.max_request_count:
                delay = interval_length - curr_time % self.__config.period
                await asyncio.sleep(delay)

            try:
                return await wrappee(*args, **kwargs)
            except self.__trigger_exceptions as exc:
                self.__over_speed_timestamp = time()
                raise exc

        return wrapper
