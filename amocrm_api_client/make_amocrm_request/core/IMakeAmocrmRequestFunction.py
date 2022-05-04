from typing import Mapping
from typing import Optional

from amocrm_api_client.make_json_request import IJsonResponse
from amocrm_api_client.make_json_request import Json
from amocrm_api_client.make_json_request import RequestMethod


__all__ = [
    "IMakeAmocrmRequestFunction",
]


class IMakeAmocrmRequestFunction:

    __slots__ = ()

    async def request(
        self,
        method: RequestMethod,
        path: str,
        parameters: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        json: Optional[Json] = None,
    ) -> IJsonResponse:
        raise NotImplementedError()
