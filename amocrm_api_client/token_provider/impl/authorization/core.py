import typing as t


__all__ = [
    "TokenPair",
]


class TokenPair(t.NamedTuple):
    access_token: str
    refresh_token: str
    expires_in: int
