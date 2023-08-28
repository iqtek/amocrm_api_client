import typing as t


__all__ = [
    "TokenBundle",
    "TokenStorage",
]


class TokenBundle(t.NamedTuple):
    access_token: str
    access_token_expires_in: int

    refresh_token: str
    refresh_token_expires_in: int


class TokenStorage:

    __slots__ = ()

    async def get_tokens(self) -> TokenBundle:
        raise NotImplementedError()

    async def set_tokens(self, tokens: TokenBundle) -> None:
        raise NotImplementedError()

    async def clear(self) -> None:
        raise NotImplementedError()
