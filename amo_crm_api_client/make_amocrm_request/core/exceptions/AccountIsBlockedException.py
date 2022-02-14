from amo_crm_api_client.exceptions import (
    AmocrmClientException,
)


__all__ = [
    "AccountIsBlockedException",
]


class AccountIsBlockedException(AmocrmClientException):
    pass
