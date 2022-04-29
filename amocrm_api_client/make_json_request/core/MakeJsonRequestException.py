from typing import Mapping
from typing import Optional

from amocrm_api_client.exceptions import AmocrmClientException


__all__ = [
    "MakeJsonRequestException",
]


class MakeJsonRequestException(AmocrmClientException):

    __slots__ = (
        "status_code",
        "headers",
        "content",
    )

    def __init__(
        self,
        status_code: Optional[int] = None,
        headers: Optional[Mapping[str, str]] = None,
        content: Optional[str] = None,
    ) -> None:
        super().__init__(
            f"status_code: {status_code},  headers: {headers}, content: {content}."
        )
        self.status_code = status_code
        self.headers = headers
        self.content = content
