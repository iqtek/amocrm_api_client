from amocrm_api_client.exceptions import AmocrmClientException


__all__ = [
    "TimeoutException",
]


class TimeoutException(AmocrmClientException):
    pass
