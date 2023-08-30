import typing as t

from pydantic import BaseModel

from amocrm_api_client.features import RateLimiterConfig
from amocrm_api_client.features import RepeaterConfig


__all__ = ["AmoCrmApiClientConfig"]


class AmoCrmApiClientConfig(BaseModel):
    base_url: str
    repeater: t.Optional[RepeaterConfig] = None
    rate_limiter: t.Optional[RateLimiterConfig] = None
