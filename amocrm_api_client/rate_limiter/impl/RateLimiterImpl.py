from asyncio import sleep
from functools import wraps
from time import time

from typing import Any
from typing import Callable
from typing import Collection
from typing import Type
from typing import TypeVar

from .RateLimiterConfig import RateLimiterConfig
from ..core import IRateLimiterDecorator


__all__ = [
    "RateLimiterImpl",
]


class RateLimiterImpl(IRateLimiterDecorator):

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
        trigger_exceptions: Collection[Type[Exception]],
    ) -> None:
        self.__config = config
        self.__trigger_exceptions = trigger_exceptions

        self.__request_counter = 0
        self.__last_interval_start = 0

        # Time of last exceeded number of requests.
        self.__over_speed_timestamp: float = 0

    def __call__(self, wrappee: Callable) -> Callable:
        @wraps(wrappee)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:

            curr_time = time()

            interval_length = self.__config.interval_length
            max_request_count = self.__config.max_request_count

            forced_delay = self.__over_speed_timestamp + \
                self.__config.forced_delay - curr_time

            if forced_delay > 0:
                await sleep(forced_delay)

            self.__interval_start = curr_time // interval_length
            if self.__interval_start == self.__last_interval_start:
                self.__request_counter += 1
            else:
                self.__last_interval_start = self.__interval_start
                self.__request_counter = 1

            if self.__request_counter >= max_request_count:
                delay = curr_time % interval_length + 1
                await sleep(delay)

            try:
                return await wrappee(*args, **kwargs)
            except self.__trigger_exceptions as e:
                self.__over_speed_timestamp = time()
                raise e

        return wrapper
