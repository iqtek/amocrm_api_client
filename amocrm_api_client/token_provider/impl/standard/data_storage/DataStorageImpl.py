import os
from typing import Any
from typing import Mapping
from typing import Optional

from aiofile import async_open
import jwt

from .IDataStorage import IDataStorage


__all__ = [
    "DataStorageImpl",
]


class DataStorageImpl(IDataStorage):

    __slots__ = (
        "__backup_file_path",
        "__encryption_key",
    )

    def __init__(
        self,
        backup_file_path: str = "backup.txt",
        encryption_key: str = "secret",
    ) -> None:
        self.__backup_file_path = backup_file_path
        self.__encryption_key = encryption_key

    async def save_data(self, data: Mapping[str, Any]) -> None:
        encoded_str = jwt.encode(
            payload=data,
            key=self.__encryption_key,
            algorithm="HS256"
        )

        async with async_open(self.__backup_file_path, "w") as afp:
            await afp.write(encoded_str)

    async def recover_data(self) -> Mapping[str, Any]:
        if not os.path.exists(self.__backup_file_path):
            return dict()

        async with async_open(self.__backup_file_path, "r") as afp:
            encoded_str = await afp.readline()

        data: Mapping[str, Any] = jwt.decode(
            jwt=encoded_str,
            key=self.__encryption_key,
            algorithms=["HS256"],
        )
        return data
