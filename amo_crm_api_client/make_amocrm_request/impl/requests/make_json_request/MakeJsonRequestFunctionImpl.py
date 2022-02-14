from typing import (
    Optional,
    Mapping,
    Any
)

import ujson
from aiohttp import (
    ClientSession,
    ClientTimeout,
)

from amo_crm_api_client.logger import (
    ILogger,
)
from .JsonResponseImpl import (
    JsonResponseImpl
)
from ....core import (
    IJsonResponse,
    RequestMethod,
    IMakeJsonRequestFunction,
    MakeJsonRequestException,
)


__all__ = [
    "MakeJsonRequestFunctionImpl",
]


class MakeJsonRequestFunctionImpl(IMakeJsonRequestFunction):

    _DEFAULT_REQUEST_TIMEOUT: float = 10.0

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
    ) -> IJsonResponse:
        try:
            async with ClientSession(
                timeout=ClientTimeout(
                    total=self._DEFAULT_REQUEST_TIMEOUT
                )
            ) as session:
                async with session.request(
                    method=method.value,
                    url=path,
                    params=parameters,
                    headers=headers,
                    json=json,
                ) as response:
                    status_code = response.status
                    headers = response.headers
                    binary_json = await response.read()

        except Exception as e:
            await self.__logger.error(f"Failed make request. {e}")
            raise MakeJsonRequestException() from e

        if binary_json is not None and len(binary_json) > 0:
            try:
                json = ujson.loads(binary_json)
            except Exception as e:
                raise MakeJsonRequestException(
                    status_code=status_code,
                    headers=headers,
                ) from e
        else:
            json = {}

        return JsonResponseImpl(
            status_code=status_code,
            headers=headers,
            json=json,
        )
