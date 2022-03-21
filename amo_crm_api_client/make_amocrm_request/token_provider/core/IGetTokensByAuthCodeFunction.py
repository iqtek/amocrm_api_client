from .TokensBundle import TokensBundle


__all__ = [
    "IGetTokensByAuthCodeFunction",
]


class IGetTokensByAuthCodeFunction:

    async def __call__(
        self,
        base_url: str,
        integration_id: str,
        secret_key: str,
        auth_code: str,
        redirect_uri: str,
    ) -> TokensBundle:
        """
        Get access and refresh token using authorization code.
        :raise AuthorizationCodeExpiredException:
            If authorization code has expired.
        :raise InvalidAuthorizationDataException:
            If other authorization data is invalid.
        """
        raise NotImplementedError()
