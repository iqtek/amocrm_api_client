from typing import (
    Any,
    Mapping,
)
from ....core import (
    IJsonResponse,
)


__all__ = [
    "JsonResponseImpl",
]


class JsonResponseImpl(IJsonResponse):

    __slots__ = (
        "_status_code",
        "_headers",
        "_json"
    )

    def __init__(
        self,
        status_code: int,
        headers: Mapping[str, str],
        json: Mapping[str, Any]
    ) -> None:
        self._status_code = status_code
        self._headers = headers
        self._json = json

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def headers(self) -> Mapping[str, str]:
        return self._headers

    @property
    def json(self) -> Mapping[str, Any]:
        return self._json
