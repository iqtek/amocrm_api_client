from amocrm_api_client.utils import AmocrmClientException


__all__ = [
    "InvalidAuthorizationCodeException",
    "InvalidClientSecretException",
    "InvalidRedirectUriException",
    "RefreshTokenExpiredException",
    "InvalidRefreshTokenException",
    "AuthorizationCodeExpiredException",
]


class InvalidAuthorizationCodeException(AmocrmClientException):
    pass


class InvalidClientSecretException(AmocrmClientException):
    pass


class InvalidRedirectUriException(AmocrmClientException):
    pass


class RefreshTokenExpiredException(AmocrmClientException):
    pass


class InvalidRefreshTokenException(AmocrmClientException):
    pass


class AuthorizationCodeExpiredException(AmocrmClientException):
    pass
