from amo_crm_api_client.exceptions import (
    AmocrmClientException,
)


__all__ = [
    "ManyEntityMutations",
]


class ManyEntityMutations(AmocrmClientException):
    pass
