from typing import Any
from typing import Mapping

from ..core import IJsonResponse
from ..core import Json


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
        json: Json,
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
    def json(self) -> Json:
        return self._json

    def __repr__(self) -> str:
        return "JsonResponseImpl(" \
                f"status_code: {self._status_code}, " \
                f"headers: {self._headers}, " \
                f"json: {self._json})"
