from amo_crm_api_client.AmoCrmApiClientConfig import AmoCrmApiClientConfig
from amo_crm_api_client.logger import ILogger
from amo_crm_api_client.storage import IKeyValueStorage
from ..core import ICheckAccessTokenFunction, IGetTokensByAuthCodeFunction, IGetTokensByRefreshTokenFunction
from ..core import IGetAccessTokenFunction


__all__ = [
    "GetAccessTokenFunctionImpl",
]


class GetAccessTokenFunctionImpl(IGetAccessTokenFunction):

    __ACCESS_TOKEN_KEY: str = "access_token"
    __REFRESH_TOKEN_KEY: str = "refresh_token"
    __REFRESH_TOKEN_TTL: int = 60 * 60 * 24 * 88
    __DEFAULT_REQUEST_TIMEOUT: float = 10.0

    def __init__(
        self,
        config: AmoCrmApiClientConfig,
        get_tokens_by_auth_code: IGetTokensByAuthCodeFunction,
        get_tokens_by_refresh_token: IGetTokensByRefreshTokenFunction,
        check_access_token_function: ICheckAccessTokenFunction,
        storage: IKeyValueStorage,
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__get_tokens_by_auth_code = get_tokens_by_auth_code
        self.__get_tokens_by_refresh_token = get_tokens_by_refresh_token
        self.__check_access_token_function = check_access_token_function
        self.__storage = storage
        self.__logger = logger

    async def __get_access_token_from_storage(self) -> str:
        return await self.__storage.get(self.__ACCESS_TOKEN_KEY)

    async def __set_access_token_to_storage(self, access_token: str, ttl: int) -> None:
        try:
            await self.__storage.set(self.__ACCESS_TOKEN_KEY, access_token, expire=ttl)
        except Exception:
            await self.__storage.update(self.__ACCESS_TOKEN_KEY, access_token, expire=ttl)

    async def __get_refresh_token_from_storage(self) -> str:
        return await self.__storage.get(self.__REFRESH_TOKEN_KEY)

    async def __set_refresh_token_to_storage(self, refresh_token: str) -> None:
        try:
            await self.__storage.set(self.__REFRESH_TOKEN_KEY, refresh_token, expire=self.__REFRESH_TOKEN_TTL)
        except Exception:
            await self.__storage.update(self.__REFRESH_TOKEN_KEY, refresh_token, expire=self.__REFRESH_TOKEN_TTL)

    async def __call__(self):
        try:
            access_token = await self.__get_access_token_from_storage()
        except Exception as e:
            access_token = None

        if access_token is not None:
            if await self.__check_access_token_function(
                    base_url=self.__config.base_url,
                    access_token=access_token,
            ):
                await self.__logger.info(f"Access token in storage not valid.")
                return access_token

        else:
            await self.__logger.info(f"Access token not found in storage.")
            try:
                refresh_token = await self.__get_refresh_token_from_storage()
            except Exception as e:
                refresh_token = None

            if refresh_token is None:
                await self.__logger.info(f"Refresh token not found in storage.")
                try:
                    tokens_bundle = await self.__get_tokens_by_auth_code(
                        base_url=self.__config.base_url,
                        integration_id=self.__config.integration_id,
                        secret_key=self.__config.secret_key,
                        auth_code=self.__config.auth_code,
                        redirect_uri=self.__config.redirect_uri,
                    )
                except Exception as e:
                    self.__logger.warning(f"Unable to get access token.")
                    self.__logger.exception(e)
                    raise e

                await self.__set_access_token_to_storage(
                    access_token=tokens_bundle.access_token,
                    ttl=tokens_bundle.expires_in,
                )
                await self.__set_refresh_token_to_storage(
                    refresh_token=tokens_bundle.refresh_token,
                )
                return tokens_bundle.access_token

            await self.__logger.info(f"Refresh token found in storage.")
            try:
                tokens_bundle = await self.__get_tokens_by_refresh_token(
                    base_url=self.__config.base_url,
                    integration_id=self.__config.integration_id,
                    secret_key=self.__config.secret_key,
                    refresh_token=refresh_token,
                    redirect_uri=self.__config.redirect_uri,
                )
            except Exception as e:
                self.__logger.warning(f"Unable to get access token.")
                self.__logger.exception(e)
                raise e

            await self.__set_access_token_to_storage(
                access_token=tokens_bundle.access_token,
                ttl=tokens_bundle.expires_in,
            )
            await self.__set_refresh_token_to_storage(
                refresh_token=tokens_bundle.refresh_token,
            )
            return tokens_bundle.access_token
