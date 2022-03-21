from amo_crm_api_client.exceptions import (
    AmocrmClientException,
)
from typing import (
    Optional,
    Mapping,
    Dict,
    Any,
)


__all__ = [
    "MakeJsonRequestException",
]


class MakeJsonRequestException(AmocrmClientException):

    def __init__(
        self,
        status_code: Optional[int] = None,
        headers: Optional[Mapping[str, str]] = None,
        json: Optional[Mapping[str, Any]] = None,
    ) -> None:
        self.status_code = status_code
        self.headers = headers
        self.json = json
