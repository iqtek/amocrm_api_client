import typing as t
from urllib.parse import urljoin

import aiohttp

from amocrm_api_client.token_provider import TokenProvider
from amocrm_api_client.utils import amocrm_api_client_logger

from .core import AccountIsBlockedException
from .core import ApiAccessException
from .core import EntityNotFoundException
from .core import ExceedRequestLimitException
from .core import IncorrectDataException
from .core import MakeAmocrmRequestFunction
from .core import ManyEntityMutations
from .core import NotAuthorizedException


__all__ = ["DefaultMakeAmocrmRequestFunction"]


class DefaultMakeAmocrmRequestFunction(MakeAmocrmRequestFunction):

    __slots__ = (
        "__base_url",
        "__token_provider",
    )

    def __init__(
        self,
        base_url: str,
        token_provider: TokenProvider,
    ) -> None:
        self.__base_url = base_url
        self.__token_provider = token_provider

    async def __check_response_code(self, status_code: int, text: t.Optional[str] = "") -> None:
        if status_code == 204 or status_code == 404:
            raise EntityNotFoundException(text)

        elif status_code == 400:
            raise IncorrectDataException(text)

        elif status_code == 401:
            await self.__token_provider.revoke_tokens()
            amocrm_api_client_logger.info(f"Tokens was revoked. Status code: {status_code} Reason: {text}")
            raise NotAuthorizedException(text)

        elif status_code == 402:
            await self.__token_provider.revoke_tokens()
            amocrm_api_client_logger.info(f"Tokens was revoked. Status code: {status_code} Reason: {text}")
            raise ApiAccessException(text)

        elif status_code == 403:
            raise AccountIsBlockedException(text)

        elif status_code == 429:
            raise ExceedRequestLimitException(text)

        elif status_code == 504:
            raise ManyEntityMutations(text)

    async def __call__(
        self,
        method: str,
        path: str,
        parameters: t.Optional[t.Mapping[str, str]] = None,
        headers: t.Optional[t.Mapping[str, str]] = None,
        json: t.Optional[t.Union[t.Mapping[str, t.Any], t.Sequence[t.Any]]] = None,
    ) -> t.Mapping[str, t.Any]:
        url = urljoin(self.__base_url, path)

        access_token = await self.__token_provider.get_access_token()

        headers = headers or {}
        headers.update(
            {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
        )

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                params=parameters,
                json=json
            ) as response:
                body = await response.json()
                await self.__check_response_code(response.status, text=str(body))
                return body
