from typing import Mapping
from typing import Optional
from urllib.parse import urljoin

from amocrm_api_client.make_json_request import IJsonResponse
from amocrm_api_client.make_json_request import Json
from amocrm_api_client.make_json_request import IMakeJsonRequestFunction
from amocrm_api_client.make_json_request import MakeJsonRequestException
from amocrm_api_client.make_json_request import RequestMethod
from amocrm_api_client.token_provider import ITokenProvider
from amocrm_api_client.logger import api_client_logger

from ..core import AccountIsBlockedException
from ..core import ApiAccessException
from ..core import ExceedRequestLimitException
from ..core import EntityNotFoundException
from ..core import MakeAmocrmRequestFunction
from ..core import IncorrectDataException
from ..core import ManyEntityMutations
from ..core import NotAuthorizedException


__all__ = [
    "MakeAmocrmRequestFunctionImpl",
]


class MakeAmocrmRequestFunctionImpl(IMakeAmocrmRequestFunction):

    __slots__ = (
        "__base_url",
        "__make_json_request_function",
        "__token_provider",
    )

    def __init__(
        self,
        base_url: str,
        make_json_request_function: IMakeJsonRequestFunction,
        token_provider: ITokenProvider,
    ) -> None:
        self.__base_url = base_url
        self.__make_json_request_function = make_json_request_function
        self.__token_provider = token_provider

    async def __check_response_code(self, status_code: int, text: Optional[str] = "") -> None:
        if status_code == 204 or status_code == 404:
            raise EntityNotFoundException(text)

        elif status_code == 400:
            # await self.__token_provider.revoke_tokens()
            raise IncorrectDataException(text)

        elif status_code == 401:
            await self.__token_provider.revoke_tokens()
            api_client_logger.info(f"Tokens was revoked. Status code: {status_code} Reason: {text}")
            raise NotAuthorizedException(text)

        elif status_code == 402:
            await self.__token_provider.revoke_tokens()
            api_client_logger.info(f"Tokens was revoked. Status code: {status_code} Reason: {text}")
            raise ApiAccessException(text)

        elif status_code == 403:
            raise AccountIsBlockedException(text)

        elif status_code == 429:
            raise ExceedRequestLimitException(text)

        elif status_code == 504:
            raise ManyEntityMutations(text)

    async def request(
        self,
        method: RequestMethod,
        path: str,
        parameters: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        json: Optional[Json] = None,
    ) -> IJsonResponse:

        url = urljoin(self.__base_url, path)

        if headers is None:
            headers = {}

        access_token = await self.__token_provider()
        headers.update(
            {
                "Authorization": f"Bearer {access_token}",
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
                await self.__check_response_code(e.status_code)
            raise e

        await self.__check_response_code(response.status_code, text=str(response.json))
        return response
