import time
from typing import (
    Optional,
    Callable,
    Generic,
    TypeVar,
    Dict,
    Type,
)
from ...core import (
    IExpiringValue,
)


__all__ = [
    "ExpiringValue",
]


class ExpiringValue(IExpiringValue):

    __slots__ = (
        "__value",
        "__expiration_time",
        "__get_time",
    )

    def __init__(
        self,
        value: str,
        expire: Optional[float] = None,
        get_time_function: Optional[Callable[[], float]] = None,
    ) -> None:
        self.__value: str = value
        self.__get_time = get_time_function or time.time
        if expire:
            curr_time = self.__get_time()
            self.__expiration_time: Optional[float] = curr_time + expire
        else:
            self.__expiration_time = None

    @classmethod
    def from_snapshot(cls: Type['ExpiringValue'], snapshot: Dict) -> 'ExpiringValue':
        value_obj = ExpiringValue(
            value=snapshot["value"],
            expire=snapshot["expire"],
        )
        return value_obj

    def make_snapshot(self) -> Dict:
        return {
            "value": self.__value,
            "expire": self.__expiration_time
        }

    def is_expired(self) -> bool:
        if self.__expiration_time is None:
            return False

        curr_time = self.__get_time()
        if self.__expiration_time >= curr_time:
            return False

        return True

    def get_value(self) -> str:
        if self.is_expired():
            raise Exception(
                "The value has expired."
            )
        return self.__value

    def update_expire(self, expire: float) -> None:
        if self.is_expired():
            raise Exception(
                "The value has expired."
            )
        curr_time = self.__get_time()
        self.__expiration_time = curr_time + expire

    def __str__(self) -> str:
        return "<ExpiringValue value={} expire={}>".format(
            self.__value,
            self.__expiration_time
        )
