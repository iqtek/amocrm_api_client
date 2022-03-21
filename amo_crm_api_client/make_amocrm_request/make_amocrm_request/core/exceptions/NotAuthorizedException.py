from amo_crm_api_client.exceptions import (
    AmocrmClientException,
)


__all__ = [
    "NotAuthorizedException",
]


class NotAuthorizedException(AmocrmClientException):
    pass
