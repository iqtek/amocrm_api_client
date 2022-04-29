from time import time

from .data_storage import IDataStorage
from .StandardTokenProviderConfig import StandardTokenProviderConfig

from ...core import IGetTokensByAuthCodeFunction
from ...core import IGetTokensByRefreshTokenFunction
from ...core import ITokenProvider


__all__ = [
    "StandardTokenProvider",
]


class StandardTokenProvider(ITokenProvider):

    __ACCESS_TOKEN_KEY: str = "access_token"
    __ACCESS_TOKEN_EXPIRE_KEY: str = "access_token_expire"
    __REFRESH_TOKEN_KEY: str = "refresh_token"
    __REFRESH_TOKEN_EXPIRE_KEY: str = "refresh_token_expire"
    __REFRESH_TOKEN_TTL: int = 60 * 60 * 24 * 88

    __slots__ = (
        "__config",
        "__get_tokens_by_auth_code",
        "__get_tokens_by_refresh_token",
        "__data_storage",
    )

    def __init__(
        self,
        config: StandardTokenProviderConfig,
        get_tokens_by_auth_code: IGetTokensByAuthCodeFunction,
        get_tokens_by_refresh_token: IGetTokensByRefreshTokenFunction,
        data_storage: IDataStorage,
    ) -> None:
        self.__config = config
        self.__get_tokens_by_auth_code = get_tokens_by_auth_code
        self.__get_tokens_by_refresh_token = get_tokens_by_refresh_token
        self.__data_storage = data_storage

    def __get_time(self) -> int:
        return int(time())

    async def __get_access_token_from_storage(self) -> str:
        data = await self.__data_storage.recover_data()
        try:
            access_token = data[self.__ACCESS_TOKEN_KEY]
            access_token_expire = data[self.__ACCESS_TOKEN_EXPIRE_KEY]
        except KeyError:
            raise Exception("There is no access token in storage.")

        if self.__get_time() < access_token_expire:
            return access_token

        raise Exception("The storage access token has expired.")

    async def __set_access_token_to_storage(self, access_token: str, expire: int) -> None:
        data = await self.__data_storage.recover_data()

        data[self.__ACCESS_TOKEN_KEY] = access_token
        data[self.__ACCESS_TOKEN_EXPIRE_KEY] = self.__get_time() + expire

        await self.__data_storage.save_data(data)

    async def __get_refresh_token_from_storage(self) -> str:
        data = await self.__data_storage.recover_data()
        try:
            refresh_token = data[self.__REFRESH_TOKEN_KEY]
            refresh_token_expire = data[self.__REFRESH_TOKEN_EXPIRE_KEY]
        except KeyError:
            raise Exception("There is no refresh token in storage.")

        if self.__get_time() < refresh_token_expire:
            return refresh_token

        raise Exception("The storage refresh token has expired.")

    async def __set_refresh_token_to_storage(self, refresh_token: str) -> None:
        data = await self.__data_storage.recover_data()

        data[self.__REFRESH_TOKEN_KEY] = refresh_token
        data[self.__REFRESH_TOKEN_EXPIRE_KEY] = self.__get_time() + self.__REFRESH_TOKEN_TTL

        await self.__data_storage.save_data(data)

    async def __call__(self) -> str:
        try:
            return await self.__get_access_token_from_storage()
        except Exception:
            pass

        try:
            refresh_token = await self.__get_refresh_token_from_storage()
        except Exception:
            tokens_bundle = await self.__get_tokens_by_auth_code(
                base_url=self.__config.base_url,
                integration_id=self.__config.integration_id,
                secret_key=self.__config.secret_key,
                auth_code=self.__config.auth_code,
                redirect_uri=self.__config.redirect_uri,
            )
        else:
            tokens_bundle = await self.__get_tokens_by_refresh_token(
                base_url=self.__config.base_url,
                integration_id=self.__config.integration_id,
                secret_key=self.__config.secret_key,
                refresh_token=refresh_token,
                redirect_uri=self.__config.redirect_uri,
            )

        await self.__set_access_token_to_storage(
            access_token=tokens_bundle.access_token,
            expire=tokens_bundle.expires_in,
        )
        await self.__set_refresh_token_to_storage(
            refresh_token=tokens_bundle.refresh_token,
        )

        return tokens_bundle.access_token
