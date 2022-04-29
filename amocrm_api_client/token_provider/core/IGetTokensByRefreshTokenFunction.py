from .TokensBundle import TokensBundle


__all__ = [
    "IGetTokensByRefreshTokenFunction",
]


class IGetTokensByRefreshTokenFunction:

    __slots__ = ()

    async def __call__(
        self,
        base_url: str,
        integration_id: str,
        secret_key: str,
        refresh_token: str,
        redirect_uri: str,
    ) -> TokensBundle:
        raise NotImplementedError()
