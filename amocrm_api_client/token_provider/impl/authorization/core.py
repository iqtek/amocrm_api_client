import typing as t


__all__ = [
    "TokenPair",
    "GetTokensByAuthCodeFunction",
    "GetTokensByRefreshTokenFunction",
]


class TokenPair(t.NamedTuple):
    access_token: str
    refresh_token: str
    expires_in: int


class GetTokensByAuthCodeFunction:

    __slots__ = ()

    async def __call__(
        self,
        base_url: str,
        integration_id: str,
        secret_key: str,
        auth_code: str,
        redirect_uri: str,
    ) -> TokenPair:
        """
        Get access and refresh token using authorization code.

        :raise AuthorizationCodeExpiredException
        :raise InvalidAuthorizationDataException
        """
        raise NotImplementedError()


class GetTokensByRefreshTokenFunction:

    __slots__ = ()

    async def __call__(
        self,
        base_url: str,
        integration_id: str,
        secret_key: str,
        refresh_token: str,
        redirect_uri: str,
    ) -> TokenPair:
        """
        Get new access and refresh token using refresh token.

        :raise RefreshTokenExpiredException
        :raise InvalidAuthorizationDataException
        """
        raise NotImplementedError()
