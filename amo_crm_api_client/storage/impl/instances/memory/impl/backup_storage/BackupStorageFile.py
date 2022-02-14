import os
import jwt
from typing import (
    Mapping,
    Dict,
    Any,
)
from aiofile import (
    async_open,
)
from ...core import (
    IBackupStorage,
)
from .BackupStorageFileConfigModel import (
    BackupStorageFileConfigModel,
)


__all__ = [
    "BackupStorageFile",
]


class BackupStorageFile(IBackupStorage):

    __slots__ = (
        "__config",
    )

    def __init__(
        self,
        config: BackupStorageFileConfigModel,
    ) -> None:
        self.__config = config

    async def save_data(self, data: Mapping[str, Any]) -> None:
        file_path = self.__config.backup_file_path
        encoded_str = jwt.encode(
            payload=data,
            key=self.__config.encryption_key,
            algorithm="HS256"
        )
        async with async_open(file_path, "w") as afp:
            await afp.write(encoded_str)

    async def recover_data(self) -> Mapping[str, Any]:
        file_path = self.__config.backup_file_path
        if not os.path.exists(file_path):
            return dict()
        async with async_open(file_path, "r") as afp:
            encoded_str = await afp.readline()
        data: Dict = jwt.decode(
            jwt=encoded_str,
            key=self.__config.encryption_key,
            algorithms=["HS256"],
        )
        return data
