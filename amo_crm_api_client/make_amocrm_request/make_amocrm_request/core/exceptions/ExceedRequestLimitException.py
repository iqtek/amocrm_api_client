from typing import (
    Optional,
)
from amo_crm_api_client.exceptions import (
    AmocrmClientException,
)


__all__ = [
    "ExceedRequestLimitException",
]


class ExceedRequestLimitException(AmocrmClientException):

    def __init__(
        self,
        reported_timeout: Optional[float] = None,
    ) -> None:
        self.reported_timeout = reported_timeout
