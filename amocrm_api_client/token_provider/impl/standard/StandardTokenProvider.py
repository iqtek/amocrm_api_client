from amocrm_api_client.exceptions import AmocrmClientException

from .StandardTokenProviderConfig import StandardTokenProviderConfig
from .token_storage import ITokenStorage

from ...core import IGetTokensByAuthCodeFunction
from ...core import IGetTokensByRefreshTokenFunction
from ...core import ITokenProvider


__all__ = [
    "StandardTokenProvider",
]


class StandardTokenProvider(ITokenProvider):

    __REFRESH_TOKEN_TTL: int = 60 * 60 * 24 * 88

    __slots__ = (
        "__config",
        "__get_tokens_by_auth_code",
        "__get_tokens_by_refresh_token",
        "__token_storage",
    )

    def __init__(
        self,
        config: StandardTokenProviderConfig,
        get_tokens_by_auth_code: IGetTokensByAuthCodeFunction,
        get_tokens_by_refresh_token: IGetTokensByRefreshTokenFunction,
        token_storage: ITokenStorage,
    ) -> None:
        self.__config = config
        self.__get_tokens_by_auth_code = get_tokens_by_auth_code
        self.__get_tokens_by_refresh_token = get_tokens_by_refresh_token
        self.__token_storage = token_storage

    async def __call__(self) -> str:
        try:
            return await self.__token_storage.get_access_token()
        except AmocrmClientException:
            pass

        try:
            refresh_token = await self.__token_storage.get_refresh_token()
        except AmocrmClientException:
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

        await self.__token_storage.set_access_token(
            access_token=tokens_bundle.access_token,
            expire=tokens_bundle.expires_in,
        )
        await self.__token_storage.set_refresh_token(
            refresh_token=tokens_bundle.refresh_token,
            expire=self.__REFRESH_TOKEN_TTL,
        )

        return tokens_bundle.access_token
