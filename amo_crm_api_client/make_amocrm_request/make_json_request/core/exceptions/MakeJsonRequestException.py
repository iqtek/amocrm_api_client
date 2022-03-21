from typing import (
    Optional,
    Mapping,
    Any,
)


__all__ = [
    "MakeJsonRequestException",
]


class MakeJsonRequestException(Exception):

    def __init__(
        self,
        status_code: Optional[int] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        self.status_code = status_code
        self.headers = headers

    def __repr__(self) -> str:
        return "MakeJsonRequestException(" \
                f"status_code: {self.status_code}, " \
                f"headers: {self.headers})"
