from typing import Optional

from pydantic import BaseModel

from amocrm_api_client.rate_limiter import RateLimiterConfig
from amocrm_api_client.repeater import RepeaterConfigModel


__all__ = [
    "AmoCrmApiClientConfig",
    "RateLimiterConfig",
    "RepeaterConfigModel",
]


class AmoCrmApiClientConfig(BaseModel):
    base_url: str
    repeater: RepeaterConfigModel = RepeaterConfigModel()
    rate_limiter: RateLimiterConfig = RateLimiterConfig()
