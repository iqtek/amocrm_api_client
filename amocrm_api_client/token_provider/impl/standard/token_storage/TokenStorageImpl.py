import os
from time import time
from typing import Any
from typing import Mapping

from aiofile import async_open
import jwt

from .exceptions import TokenHasExpiredException
from .exceptions import TokenIsMissingException
from .ITokenStorage import ITokenStorage


__all__ = [
    "TokenStorageImpl",
]


class TokenStorageImpl(ITokenStorage):

    __ACCESS_TOKEN_KEY: str = "access_token"
    __ACCESS_TOKEN_EXPIRE_KEY: str = "access_token_expire"
    __REFRESH_TOKEN_KEY: str = "refresh_token"
    __REFRESH_TOKEN_EXPIRE_KEY: str = "refresh_token_expire"

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

    def __get_time(self) -> int:
        return int(time())

    async def _save_data(self, data: Mapping[str, Any]) -> None:
        encoded_str = jwt.encode(
            payload=data,
            key=self.__encryption_key,
            algorithm="HS256"
        )

        async with async_open(self.__backup_file_path, "w") as afp:
            await afp.write(encoded_str)

    async def _recover_data(self) -> Mapping[str, Any]:
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

    async def get_access_token(self) -> str:
        data = await self._recover_data()
        try:
            access_token = data[self.__ACCESS_TOKEN_KEY]
            access_token_expire = data[self.__ACCESS_TOKEN_EXPIRE_KEY]
        except KeyError:
            raise TokenIsMissingException("There is no access token in storage.")

        if self.__get_time() < access_token_expire:
            return access_token

        raise TokenHasExpiredException("The storage access token has expired.")

    async def set_access_token(self, access_token: str, expire: int) -> None:
        data = await self._recover_data()

        data[self.__ACCESS_TOKEN_KEY] = access_token
        data[self.__ACCESS_TOKEN_EXPIRE_KEY] = self.__get_time() + expire

        await self._save_data(data)

    async def get_refresh_token(self) -> str:
        data = await self._recover_data()
        try:
            refresh_token = data[self.__REFRESH_TOKEN_KEY]
            refresh_token_expire = data[self.__REFRESH_TOKEN_EXPIRE_KEY]
        except KeyError:
            raise TokenIsMissingException("There is no refresh token in storage.")

        if self.__get_time() < refresh_token_expire:
            return refresh_token

        raise TokenHasExpiredException("The storage refresh token has expired.")

    async def set_refresh_token(self, refresh_token: str, expire: int) -> None:
        data = await self._recover_data()

        data[self.__REFRESH_TOKEN_KEY] = refresh_token
        data[self.__REFRESH_TOKEN_EXPIRE_KEY] = self.__get_time() + expire

        await self._save_data(data)
