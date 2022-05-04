from typing import Optional

from amocrm_api_client.exceptions import AmocrmClientException


__all__ = [
    "AccountIsBlockedException",
    "ApiAccessException",
    "EntityNotFoundException",
    "ExceedRequestLimitException",
    "IncorrectDataException",
    "ManyEntityMutations",
    "NotAuthorizedException",
]


class AccountIsBlockedException(AmocrmClientException):
    pass


class ApiAccessException(AmocrmClientException):
    pass


class EntityNotFoundException(AmocrmClientException):
    pass


class ExceedRequestLimitException(AmocrmClientException):

    def __init__(
        self,
        reported_timeout: Optional[float] = None,
    ) -> None:
        reported_timeout = str(reported_timeout) or "not specified"
        super().__init__(f"reported_timeout: `{reported_timeout}`.")


class IncorrectDataException(AmocrmClientException):
    pass


class ManyEntityMutations(AmocrmClientException):
    pass


class NotAuthorizedException(AmocrmClientException):
    pass
