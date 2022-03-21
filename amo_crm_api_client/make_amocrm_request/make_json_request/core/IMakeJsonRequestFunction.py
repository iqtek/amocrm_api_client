from typing import (
    Optional,
    Mapping,
    Any,
)

from .IJsonResponse import IJsonResponse
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
        json: Optional[Any] = None,
    ) -> IJsonResponse:
        """
        :raise MakeJsonRequestException: If returned data is not valid.
        :raise TimeoutError: If response timed out.
        """
        raise NotImplementedError()
