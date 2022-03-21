import asyncio
from typing import Any, Mapping, Optional

from aiohttp import ClientSession, ClientTimeout
import ujson

from amo_crm_api_client.logger import ILogger
from .JsonResponseImpl import JsonResponseImpl
from ..core import (
    IJsonResponse,
    IMakeJsonRequestFunction,
    MakeJsonRequestException,
    RequestMethod,
)


__all__ = [
    "MakeJsonRequestFunctionImpl",
]


class MakeJsonRequestFunctionImpl(IMakeJsonRequestFunction):

    def __init__(
        self,
        logger: ILogger,
    ) -> None:
        self.__logger = logger

    async def __call__(
        self,
        method: RequestMethod,
        path: str,
        parameters: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        json: Optional[Any] = None,
        timeout: float = 10.0
    ) -> IJsonResponse:
        try:
            async with ClientSession(
                    timeout=ClientTimeout(total=timeout)) as session:
                async with session.request(
                    method=method.value,
                    url=path,
                    params=parameters,
                    headers=headers,
                    json=json,
                ) as response:
                    status_code = response.status
                    headers = response.headers
                    binary_response = await response.read()

        except asyncio.TimeoutError:
            raise TimeoutError

        except Exception as e:
            self.__logger.error(f"Failed make json request.")
            self.__logger.exception(e)
            raise MakeJsonRequestException() from e

        if binary_response is not None and len(binary_response) > 0:

            try:
                json = ujson.loads(binary_response)
            except ValueError as e:
                raise MakeJsonRequestException(
                    status_code=status_code,
                    headers=headers,
                ) from e

        if len(binary_response) == 0:
            json = {}

        return JsonResponseImpl(
            status_code=status_code,
            headers=headers,
            json=json,
        )
