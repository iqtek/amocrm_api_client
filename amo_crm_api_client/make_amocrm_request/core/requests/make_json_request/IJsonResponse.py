from typing import (
    Any,
    Mapping,
)


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
    def json(self) -> Mapping[str, Any]:
        raise NotImplementedError()
