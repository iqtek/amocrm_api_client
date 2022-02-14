from amo_crm_api_client.exceptions import (
    AmocrmClientException,
)


__all__ = [
    "ApiAccessException",
]


class ApiAccessException(AmocrmClientException):
    pass
