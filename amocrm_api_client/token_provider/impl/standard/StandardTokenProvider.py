from warnings import warn
import typing as t
from amocrm_api_client.utils import AmocrmClientException

from .StandardTokenProviderConfig import StandardTokenProviderConfig

from ..token_storage import TokenBundle
from ..token_storage import TokenStorage

from ..authorization import TokenPair
from ..authorization import GetTokensByAuthCodeFunction
from ..authorization import GetTokensByRefreshTokenFunction
from ...core import TokenProvider

from ...core import RefreshTokenExpiredException


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
        get_tokens_by_auth_code: GetTokensByAuthCodeFunction,
        get_tokens_by_refresh_token: GetTokensByRefreshTokenFunction,
        token_storage: TokenStorage,
    ) -> None:
        self.__config = config
        self.__get_tokens_by_auth_code = get_tokens_by_auth_code
        self.__get_tokens_by_refresh_token = get_tokens_by_refresh_token
        self.__token_storage = token_storage
        self.__token_bundle: t.Optional[TokenBundle] = None

    def __token_pair_to_token_bundle(self, token_pair: TokenPair) -> TokenBundle:
        return TokenBundle(
            access_token=token_pair.access_token,
            access_token_expires_in=token_pair.expires_in,
            refresh_token=token_pair.refresh_token,
            refresh_token_expires_in=int(time()) + self.__REFRESH_TOKEN_TTL
        )

    async def __call__(self) -> str:
        tokens = self.__token_bundle or (await self.__token_storage.get_tokens())

        if tokens.access_token_expires_in <= time():
            return tokens.access_token

        if tokens.refresh_token_expires_in <= time():
            token_pair = await self.__get_tokens_by_refresh_token(
                base_url=self.__config.base_url,
                integration_id=self.__config.integration_id,
                secret_key=self.__config.secret_key,
                refresh_token=tokens.refresh_token,
                redirect_uri=self.__config.redirect_uri,
            )

            self.__token_bundle = self.__token_pair_to_token_bundle(token_pair)
            await self.__token_storage.set_tokens(self.__token_bundle)
            return self.__token_bundle.access_token

        token_pair = await self.__get_tokens_by_auth_code(
            base_url=self.__config.base_url,
            integration_id=self.__config.integration_id,
            secret_key=self.__config.secret_key,
            auth_code=self.__config.auth_code,
            redirect_uri=self.__config.redirect_uri,
        )

        self.__token_bundle = self.__token_pair_to_token_bundle(token_pair)
        await self.__token_storage.set_tokens(self.__token_bundle)
        return self.__token_bundle.access_token

    async def revoke_access_token(self) -> None:
        token_pair = await self.__get_tokens_by_refresh_token(
            base_url=self.__config.base_url,
            integration_id=self.__config.integration_id,
            secret_key=self.__config.secret_key,
            refresh_token=tokens.refresh_token,
            redirect_uri=self.__config.redirect_uri,
        )

        self.__token_bundle = self.__token_pair_to_token_bundle(token_pair)
        await self.__token_storage.set_tokens(self.__token_bundle)
