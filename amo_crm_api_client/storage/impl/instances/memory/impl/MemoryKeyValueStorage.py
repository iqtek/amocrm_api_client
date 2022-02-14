from typing import (
    Dict,
)
from amo_crm_api_client.logger import (
    ILogger,
)
from .....core import (
    IKeyValueStorage,
)
from ..core import (
    IBackupStorage,
    IExpiringValue,
)
from .expiring_value import ExpiringValue


__all__ = [
    "MemoryKeyValueStorage",
]


class MemoryKeyValueStorage(IKeyValueStorage):

    __DELIMITER: str = '-'

    def __init__(
        self,
        backup_storage: IBackupStorage,
        logger: ILogger,
        prefix: str = None,
    ) -> None:
        self.__storage: Dict[str, IExpiringValue] = {}
        self.__backup_storage = backup_storage
        self.__logger = logger
        if prefix is not None:
            self.__prefix = prefix + self.__DELIMITER
        else:
            self.__prefix = ""

    async def initialize(self) -> None:
        data = await self.__backup_storage.recover_data()
        recovered_data = {key: ExpiringValue.from_snapshot(value)
                          for key, value in data.items()}
        self.__storage.update(recovered_data)

    async def deinitialize(self) -> None:
        data = dict()
        for key in self.__storage.keys():
            try:
                value_obj = await self.__get_value_object(key)
                data[key] = value_obj.make_snapshot()
            except KeyError:
                pass
        await self.__backup_storage.save_data(data)

    async def __get_value_object(self, full_key: str) -> IExpiringValue:
        try:
            value_obj = self.__storage[full_key]
        except KeyError:
            raise KeyError(
                "MemoryKeyValueStorage: "
                f"Failed to get value for key={full_key}. "
                f"The key={full_key} is missing."
            )
        return value_obj

    async def get(self, key: str) -> str:
        full_key = self.__prefix + key
        value_obj: IExpiringValue = await self.__get_value_object(full_key)
        try:
            return value_obj.get_value()
        except Exception:
            await self.delete(key)
            raise KeyError(
                "MemoryKeyValueStorage: "
                f"Failed to get value for key={full_key}."
                f"The key={full_key} is missing."
            )

    async def set_expire(self, key: str, expire: float) -> None:
        full_key = self.__prefix + key
        try:
            value_obj = await self. __get_value_object(full_key)
        except KeyError:
            raise LookupError(
                "MemoryKeyValueStorage: "
                "Could not update expire for key. "
                f"The key={full_key} missing."
            )
        else:
            value_obj.update_expire(expire)
        await self.__logger.debug(
            "MemoryKeyValueStorage: "
            "Key expiration updated. "
            f"The key={full_key} expire={expire}."
        )

    async def set(self, key: str, value: str, expire: float = None) -> None:
        full_key = self.__prefix + key
        try:
            await self.__get_value_object(full_key)
        except KeyError:
            value_obj = ExpiringValue(value=value, expire=expire)
            self.__storage[full_key] = value_obj
            await self.__logger.debug(
                "MemoryKeyValueStorage: "
                f"Set value={value} by key={full_key}."
            )
        else:
            raise LookupError(
                "MemoryKeyValueStorage: "
                "Could not set value for key. "
                f"The key={full_key} already exists."
            )

    async def update(self, key: str, value: str, expire=None) -> None:
        full_key = self.__prefix + key
        try:
            await self.__get_value_object(full_key)
        except KeyError:
            raise LookupError(
                "MemoryKeyValueStorage: "
                "Could not update value for key. "
                f"The key={full_key} missing."
            )
        value_obj = ExpiringValue(value=value, expire=expire)
        self.__storage[full_key] = value_obj
        await self.__logger.debug(
            "MemoryKeyValueStorage: "
            f"Update value={value} by key={full_key}."
        )

    async def delete(self, key: str) -> None:
        full_key = self.__prefix + key
        try:
            await self.__get_value_object(full_key)
        except KeyError:
            raise LookupError(
                "MemoryKeyValueStorage: "
                "Could not delete value for key. "
                f"The key={full_key} missing ."
            )
        self.__storage.pop(full_key)
        await self.__logger.debug(
            "MemoryKeyValueStorage: "
            f"Delete key={full_key}."
        )
