from typing import Mapping
from typing import Optional

from .IJsonResponse import IJsonResponse
from .Json import Json
from .RequestMethod import RequestMethod


__all__ = [
    "IMakeJsonRequestFunction",
]


class IMakeJsonRequestFunction:

    async def __call__(
        self,
        method: RequestMethod,
        path: str,
        parameters: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        json: Optional[Json] = None,
        timeout: Optional[float] = 10.0,
    ) -> IJsonResponse:
        """
        :raise MakeJsonRequestException: If returned data is not valid.
        :raise TimeoutError: If response timed out.
        """
        raise NotImplementedError()
