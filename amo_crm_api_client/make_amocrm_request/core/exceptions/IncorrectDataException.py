from amo_crm_api_client.exceptions import (
    AmocrmClientException,
)


__all__ = [
    "IncorrectDataException",
]


class IncorrectDataException(Exception):
    pass
