import asyncio
import typing as t
from time import time

from ...core import TokenProvider

from ..authorization import TokenPair
from ..token_storage import TokenBundle, TokenStorage


__all__ = ["DefaultTokenProvider"]


class DefaultTokenProvider(TokenProvider):

    __REFRESH_TOKEN_TTL: int = 60 * 60 * 24 * 88

    __slots__ = (
        "__get_tokens",
        "__refresh_tokens",
        "__token_storage",
        "__token_bundle",
        "__update_tokens_task",
    )

    def __init__(
        self,
        get_tokens: t.Callable[[], t.Awaitable[TokenPair]],
        refresh_tokens: t.Callable[[str], t.Awaitable[TokenPair]],
        token_storage: TokenStorage,
    ) -> None:
        self.__get_tokens = get_tokens
        self.__refresh_tokens = refresh_tokens
        self.__token_storage = token_storage

        self.__token_bundle: t.Optional[TokenBundle] = None
        self.__update_tokens_task: t.Optional[asyncio.Task] = None

    def __token_pair_to_token_bundle(self, token_pair: TokenPair) -> TokenBundle:
        timestamp = int(time())
        return TokenBundle(
            access_token=token_pair.access_token,
            access_token_expires_in=timestamp + token_pair.expires_in,
            refresh_token=token_pair.refresh_token,
            refresh_token_expires_in=timestamp + self.__REFRESH_TOKEN_TTL
        )

    async def __update_tokens(self) -> str:
        if self.__token_bundle is None:
            token_pair = await self.__get_tokens()
        else:
            if self.__token_bundle.refresh_token_expires_in <= time():
                token_pair = await self.__refresh_tokens(self.__token_bundle.refresh_token)
            else:
                token_pair = await self.__get_tokens()

        self.__token_bundle = self.__token_pair_to_token_bundle(token_pair)
        await self.__token_storage.set_tokens(self.__token_bundle)

        return self.__token_bundle.access_token

    async def get_access_token(self) -> str:
        if self.__token_bundle is None:
            try:
                self.__token_bundle = await self.__token_storage.get_tokens()
                print(self.__token_bundle)
            except KeyError:
                self.__update_tokens_task = asyncio.create_task(self.__update_tokens())
                return await self.__update_tokens_task

        if self.__update_tokens_task is not None:
            return await self.__update_tokens_task

        if self.__token_bundle.access_token_expires_in <= time():
            self.__update_tokens_task = asyncio.create_task(self.__update_tokens())
            return await self.__update_tokens_task

        return self.__token_bundle.access_token

    async def revoke_access_token(self) -> None:
        self.__update_tokens_task = asyncio.create_task(self.__update_tokens())
