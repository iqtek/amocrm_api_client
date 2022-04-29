from typing import Any
from typing import Mapping

from .Json import Json


__all__ = [
    "IJsonResponse",
]


class IJsonResponse:

    __slots__ = ()

    @property
    def status_code(self) -> int:
        raise NotImplementedError()

    @property
    def headers(self) -> Mapping[str, str]:
        raise NotImplementedError()

    @property
    def json(self) -> Json:
        raise NotImplementedError()
