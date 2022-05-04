__all__ = [
    "ITokenStorage",
]


class ITokenStorage:

    __slots__ = ()

    async def get_access_token(self) -> str:
        pass

    async def set_access_token(self, access_token: str, expire: int) -> None:
        pass

    async def get_refresh_token(self) -> str:
        pass

    async def set_refresh_token(self, refresh_token: str, expire: int) -> None:
        pass
