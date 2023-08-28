import typing as t

from amocrm_api_client.exceptions import AmocrmClientException


__all__ = [
    "MakeAmocrmRequestFunction",
    "AccountIsBlockedException",
    "ApiAccessException",
    "EntityNotFoundException",
    "ExceedRequestLimitException",
    "IncorrectDataException",
    "ManyEntityMutations",
    "NotAuthorizedException",
]


class MakeAmocrmRequestFunction:

    __slots__ = ()

    async def request(
        self,
        method: str,
        path: str,
        parameters: Optional[t.Mapping[str, str]] = None,
        headers: Optional[t.Mapping[str, str]] = None,
        json: Optional[t.Mapping[str, t.Any]] = None,
    ) -> t.Mapping[str, t.Any]:
        raise NotImplementedError()


class AccountIsBlockedException(AmocrmClientException):
    pass


class ApiAccessException(AmocrmClientException):
    pass


class EntityNotFoundException(AmocrmClientException):
    pass


class ExceedRequestLimitException(AmocrmClientException):

    def __init__(
        self,
        reported_timeout: t.Optional[float] = None,
    ) -> None:
        reported_timeout = str(reported_timeout) or "not specified"
        super().__init__(f"reported_timeout: `{reported_timeout}`.")


class IncorrectDataException(AmocrmClientException):
    pass


class ManyEntityMutations(AmocrmClientException):
    pass


class NotAuthorizedException(AmocrmClientException):
    pass
