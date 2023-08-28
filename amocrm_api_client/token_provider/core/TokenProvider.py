__all__ = ["TokenProvider"]


class TokenProvider:

    __slots__ = ()

    async def get_access_token(self) -> str:
        raise NotImplementedError()

    async def revoke_access_token(self) -> None:
        raise NotImplementedError()
