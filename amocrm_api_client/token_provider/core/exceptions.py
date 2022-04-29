from amocrm_api_client.exceptions import AmocrmClientException


class AuthorizationCodeExpiredException(AmocrmClientException):
    pass


class InvalidAuthorizationDataException(AmocrmClientException):
    pass


class RefreshTokenExpiredException(AmocrmClientException):
    pass
