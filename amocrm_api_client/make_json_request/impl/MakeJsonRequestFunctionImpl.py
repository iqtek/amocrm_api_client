import asyncio
from typing import Mapping
from typing import Optional

from aiohttp import ClientSession
from aiohttp import ClientTimeout
from ujson import loads

from .JsonResponseImpl import JsonResponseImpl

from ..core import IJsonResponse
from ..core import IMakeJsonRequestFunction
from ..core import Json
from ..core import MakeJsonRequestException
from ..core import RequestMethod


__all__ = [
    "MakeJsonRequestFunctionImpl",
]


class MakeJsonRequestFunctionImpl(IMakeJsonRequestFunction):

    async def __call__(
        self,
        method: RequestMethod,
        path: str,
        parameters: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        json: Optional[Json] = None,
        timeout: float = 10.0,
    ) -> IJsonResponse:
        try:
            async with ClientSession(
                timeout=ClientTimeout(total=timeout),
                trust_env=True,
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
                    binary_response = await response.read()

        except asyncio.TimeoutError:
            raise TimeoutError()

        except Exception as e:
            raise MakeJsonRequestException() from e

        if binary_response is not None and len(binary_response) > 0:

            try:
                json = loads(binary_response)
            except ValueError as e:
                raise MakeJsonRequestException(
                    status_code=status_code,
                    headers=headers,
                    content=binary_response.decode("utf-8"),
                ) from e

        if len(binary_response) == 0:
            json = {}

        json_response = JsonResponseImpl(
            status_code=status_code,
            headers=headers,
            json=json,
        )

        return json_response
