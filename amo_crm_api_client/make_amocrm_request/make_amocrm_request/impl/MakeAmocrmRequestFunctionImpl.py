from typing import (
    Optional,
    Mapping,
    Any
)
from urllib.parse import urljoin
from ..core import (
    IMakeAmocrmRequestFunction,
    ExceedRequestLimitException,
    IncorrectDataException,
    AccountIsBlockedException,
    MakeJsonRequestException,
    EntityNotFoundException,
    NotAuthorizedException,
    ManyEntityMutations,
    ApiAccessException,
)
from ...make_json_request import (
    IMakeJsonRequestFunction,
    IJsonResponse,
    RequestMethod,
)
from ...token_provider import IGetAccessTokenFunction


__all__ = [
    "MakeAmocrmRequestFunctionImpl",
]


class MakeAmocrmRequestFunctionImpl(IMakeAmocrmRequestFunction):

    def __init__(
        self,
        base_url: str,
        make_json_request_function: IMakeJsonRequestFunction,
        get_access_token_function: IGetAccessTokenFunction,
    ) -> None:
        self.__base_url = base_url
        self.__make_json_request_function = make_json_request_function
        self.__get_access_token_function = get_access_token_function

    def __check_response_code(self, status_code: int) -> None:

        exception: Optional[Exception] = None

        if status_code == 204 or status_code == 404:
            exception = EntityNotFoundException()

        elif status_code == 400:
            exception = IncorrectDataException()

        elif status_code == 401:
            exception = NotAuthorizedException()

        elif status_code == 402:
            exception = ApiAccessException()

        elif status_code == 403:
            exception = AccountIsBlockedException()

        elif status_code == 429:
            exception = ExceedRequestLimitException()

        elif status_code == 504:
            exception = ManyEntityMutations()

        if exception:
            raise exception

    async def request(
        self,
        method: RequestMethod,
        path: str,
        parameters: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        json: Optional[Any] = None,
    ) -> IJsonResponse:

        url = urljoin(self.__base_url, path)
        if headers is None:
            headers = {}
        headers.update(
            {
                "Authorization": "Bearer {}".format(
                    await self.__get_access_token_function()
                ),
                "Content-Type": "application/json",
            }
        )

        try:
            response = await self.__make_json_request_function(
                method=method,
                path=url,
                parameters=parameters,
                headers=headers,
                json=json,
            )
        except MakeJsonRequestException as e:
            if e.status_code:
                self.__check_response_code(e.status_code)
            raise e

        self.__check_response_code(response.status_code)
        return response
