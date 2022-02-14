import time
from typing import (
    Union,
    Dict,
    Type,
)


__all__ = [
    "IExpiringValue",
]


class IExpiringValue:

    @classmethod
    def from_snapshot(cls: Type['IExpiringValue'], snapshot: Dict[str, Union[float, str]]) -> 'IExpiringValue':
        """
        Creates an object from a snapshot received from the call make_snapshot().
        :param snapshot: Dictionary received from the call make_snapshot().
        :return: ExpiringValue instance.
        """
        raise NotImplementedError()

    def make_snapshot(self) -> Dict[str, Union[float, str]]:
        """
        Take a snapshot of the current state from which you can then recover.
        :return: Snapshot as a dictionary.
        """
        raise NotImplementedError()

    def is_expired(self) -> bool:
        """
        Check if the value has expired.
        :return: value has expired.
        """
        raise NotImplementedError()

    def get_value(self) -> str:
        """
        Get the value if it is not expired.
        :return: value as str.
        :raise Exception if value is not fit.
        """
        raise NotImplementedError()

    def update_expire(self, expire: float) -> None:
        """
        Set the time in seconds after how long the value will expire.
        If it is not already expired.
        :param expire: time in seconds.
        """
        raise NotImplementedError()
