__all__ = [
    "ITokenProvider",
]


class ITokenProvider:

    __slots__ = ()

    async def __call__(self) -> str:
        raise NotImplementedError()

    async def revoke_tokens(self) -> None:
        raise NotImplementedError()
