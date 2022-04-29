from typing import Any
from typing import Mapping


__all__ = [
    "IDataStorage",
]


class IDataStorage:

    async def save_data(self, data: Mapping[str, Any]) -> None:
        """
        Save data to a file on disk.
        :param data: Data to save.
        """
        raise NotImplementedError()

    async def recover_data(self) -> Mapping[str, Any]:
        """
        Recover data to a file on disk.
        :return: Data
        """
        raise NotImplementedError()
