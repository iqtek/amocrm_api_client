from asyncio import sleep
from functools import wraps
from typing import Any
from typing import Callable
from typing import Collection
from typing import Type

from .RepeaterConfigModel import RepeaterConfigModel
from ..core import IRepeaterDecorator


__all__ = [
    "RepeaterDecoratorImpl",
]


class RepeaterDecoratorImpl(IRepeaterDecorator):

    def __init__(
        self,
        config: RepeaterConfigModel,
        trigger_exceptions: Collection[Type[Exception]],
    ) -> None:
        self.__config = config
        self.__trigger_exceptions = trigger_exceptions

    def __call__(self, wrappee: Callable) -> Callable:

        @wraps(wrappee)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:

            for i in range(self.__config.tries):

                try:
                    return await wrappee(*args, **kwargs)
                except self.__trigger_exceptions as e:
                    if i + 1 == self.__config.tries:
                        raise e

                delay = self.__config.delay + self.__config.backoff * i

                if self.__config.max_delay is not None and delay > self.__config.max_delay:
                    delay = self.__config.max_delay

                await sleep(delay)

        return wrapper
