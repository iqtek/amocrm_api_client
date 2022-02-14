from ..core import IKeyFactory


__all__ = [
    "RateLimiterKeyFactory",
]


class RateLimiterKeyFactory(IKeyFactory):

    __slots__ = (
        "__resource_name",
    )

    def __init__(
        self,
        resource_name: str,
    ) -> None:
        self.__resource_name = resource_name

    def __call__(
        self,
        interval_start: int,
        interval_length: int,
    ) -> str:
        return f"{self.__resource_name}-{interval_start}"
