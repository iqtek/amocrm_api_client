import typing as t

from amocrm_api_client.utils import AmocrmClientException


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

    async def __call__(
        self,
        method: str,
        path: str,
        parameters: t.Optional[t.Mapping[str, str]] = None,
        headers: t.Optional[t.Mapping[str, str]] = None,
        json: t.Optional[t.Union[t.Mapping[str, t.Any], t.Sequence[t.Any]]] = None,
    ) -> t.Mapping[str, t.Any]:
        raise NotImplementedError()


class AccountIsBlockedException(AmocrmClientException):
    pass


class ApiAccessException(AmocrmClientException):
    pass


class EntityNotFoundException(AmocrmClientException):
    pass


class ExceedRequestLimitException(AmocrmClientException):
    pass


class IncorrectDataException(AmocrmClientException):
    pass


class ManyEntityMutations(AmocrmClientException):
    pass


class NotAuthorizedException(AmocrmClientException):
    pass
