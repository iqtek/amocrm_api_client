from amocrm_api_client.exceptions import AmocrmClientException


__all__ = [
    "AuthorizationCodeExpiredException",
    "InvalidAuthorizationDataException",
    "RefreshTokenExpiredException",
]


class AuthorizationCodeExpiredException(AmocrmClientException):
    pass


class InvalidAuthorizationDataException(AmocrmClientException):
    pass


class RefreshTokenExpiredException(AmocrmClientException):
    pass
