from dataclasses import dataclass


__all__ = [
    "TokensBundle",
]


@dataclass(frozen=True)
class TokensBundle:
    access_token: str
    refresh_token: str
    expires_in: int
