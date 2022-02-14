import asyncio
from asyncio import sleep
from functools import wraps
from time import time
from typing import Any, Callable, Tuple, TypeVar, Type

from amo_crm_api_client.logger import ILogger
from .RateLimiterConfig import RateLimiterConfig
from ..core import IRateLimiter


__all__ = [
    "SimpleRateLimiter",
]


T = TypeVar("T", bound=Exception)


class SimpleRateLimiter(IRateLimiter):

    def __init__(
        self,
        config: RateLimiterConfig,
        trigger_exceptions: Tuple[Type[T]],
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__logger = logger
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
                await self.__logger.debug(
                    f"RateLimiter: forced delay={forced_delay}."
                )
                await asyncio.sleep(forced_delay)

            self.__interval_start = curr_time // interval_length
            if self.__interval_start == self.__last_interval_start:
                self.__request_counter += 1
            else:
                self.__last_interval_start = self.__interval_start
                self.__request_counter = 1

            if self.__request_counter >= max_request_count:
                delay = curr_time % interval_length + 1
                await self.__logger.debug(
                    f"RateLimiter: delay={delay}."
                )
                await sleep(delay)

            try:
                return await wrappee(*args, **kwargs)
            except trigger_exceptions as e:
                self.__over_speed_timestamp = time()
                await self.__logger.debug(
                    f"RateLimiter: over speed detected "
                    f"timestamp={self.__over_speed_timestamp}."
                )
                f"RateLimiter: exception caught: {e}."
                raise e

        return wrapper
