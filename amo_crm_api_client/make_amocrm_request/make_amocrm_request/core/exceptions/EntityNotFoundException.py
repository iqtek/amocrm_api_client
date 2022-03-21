from amo_crm_api_client.exceptions import (
    AmocrmClientException,
)


__all__ = [
    "EntityNotFoundException",
]


class EntityNotFoundException(AmocrmClientException):
    pass
