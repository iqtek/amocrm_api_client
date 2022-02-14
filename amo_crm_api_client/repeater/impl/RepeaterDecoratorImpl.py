import asyncio
from functools import wraps
from typing import Any, Callable, Tuple, Type, TypeVar

from amo_crm_api_client.logger import ILogger
from .RepeaterConfigModel import RepeaterConfigModel
from ..core import IRepeaterDecorator


__all__ = [
    "RepeaterDecoratorImpl",
]


T = TypeVar("T", bound=Exception)


class RepeaterDecoratorImpl(IRepeaterDecorator):

    def __init__(
        self,
        config: RepeaterConfigModel,
        logger: ILogger,
        trigger_exceptions: Tuple[Type[T]],
    ) -> None:
        self.__config = config
        self.__logger = logger
        self.__trigger_exceptions = trigger_exceptions

    def __call__(self, wrappee: Callable) -> Callable:

        @wraps(wrappee)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:

            for i in range(self.__config.tries):
                delay = self.__config.delay + self.__config.backoff * i
                if self.__config.max_delay and delay > self.__config.max_delay:
                    delay = self.__config.max_delay

                await self.__logger.debug(
                    f"Repeater: delay={delay}."
                )
                await asyncio.sleep(delay)

                try:
                    await self.__logger.debug(
                        f"Repeater: attempting to complete a task {wrappee} #{i+1}."
                    )
                    return await wrappee(*args, **kwargs)
                except self.__trigger_exceptions as e:
                    await self.__logger.debug(
                        f"Repeater: exception caught: {e!r}."
                        f"The task will be repeated."
                    )

                    if i + 1 == self.__config.tries:
                        await self.__logger.debug(
                            f"Repeater: exception caught: {e!r}. "
                            f"Attempts exhausted."
                        )
                        raise e
                    continue
                except Exception as e:
                    await self.__logger.debug(
                        f"Repeater: critical exception caught: {e!r}"
                    )
                    raise e

        return wrapper
