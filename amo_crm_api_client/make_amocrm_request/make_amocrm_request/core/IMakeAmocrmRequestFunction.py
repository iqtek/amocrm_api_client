from typing import (
    Mapping,
    Optional,
    Any
)
from ...make_json_request import (
    IJsonResponse,
    RequestMethod,
)


__all__ = [
    "IMakeAmocrmRequestFunction",
]


class IMakeAmocrmRequestFunction:

    async def request(
        self,
        method: RequestMethod,
        path: str,
        parameters: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        json: Optional[Any] = None,
    ) -> IJsonResponse:
        raise NotImplementedError()
