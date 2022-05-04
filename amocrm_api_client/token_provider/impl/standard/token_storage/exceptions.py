from amocrm_api_client.exceptions import AmocrmClientException


__all__ = [
    "TokenHasExpiredException",
    "TokenIsMissingException"
]


class TokenHasExpiredException(AmocrmClientException):
    pass


class TokenIsMissingException(AmocrmClientException):
    pass
