__all__ = [
    "IGetAccessTokenFunction",
]


class IGetAccessTokenFunction:

    async def __call__(self) -> str:
        raise NotImplementedError()
