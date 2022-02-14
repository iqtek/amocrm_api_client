from typing import (
    Optional,
    Mapping,
    Any
)
from ....core import (
    ExceedRequestLimitException,
    IncorrectDataException,
    AccountIsBlockedException,
    MakeJsonRequestException,
    EntityNotFoundException,
    NotAuthorizedException,
    ManyEntityMutations,
    ApiAccessException,
)
from ....core import (
    IMakeAmocrmRequestFunction,
    IMakeJsonRequestFunction,
    IGetAccessTokenFunction,
    IJsonResponse,
    RequestMethod,
)
from ..make_url import make_url


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

    def __check_response_code(self, response: IJsonResponse) -> None:

        exception: Optional[Exception] = None

        if response.status_code == 204 or response.status_code == 404:
            exception = EntityNotFoundException(response.json)

        elif response.status_code == 400:
            exception = IncorrectDataException(response.json)

        elif response.status_code == 401:
            exception = NotAuthorizedException(response.json)

        elif response.status_code == 402:
            exception = ApiAccessException(response.json)

        elif response.status_code == 403:
            exception = AccountIsBlockedException(response.json)

        elif response.status_code == 429:
            exception = ExceedRequestLimitException()

        elif response.status_code == 504:
            exception = ManyEntityMutations(response.json)

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

        url = make_url(self.__base_url, path)
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
            self.__check_response_code(e.status_code)
            raise e

        self.__check_response_code(response)
        return response
