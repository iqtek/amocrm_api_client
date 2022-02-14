from typing import Optional

from pydantic import BaseModel

from amo_crm_api_client.rate_limiter import RateLimiterConfig
from amo_crm_api_client.repeater import RepeaterConfigModel
from amo_crm_api_client.storage import (
    KeyValueStorageConfigModel,
    MemoryStorageConfigModel,
    RedisStorageConfigModel,
)

__all__ = [
    "AmoCrmApiClientConfig",
    "KeyValueStorageConfigModel",
    "MemoryStorageConfigModel",
    "RateLimiterConfig",
    "RedisStorageConfigModel",
    "RepeaterConfigModel",
]


class AmoCrmApiClientConfig(BaseModel):

    integration_id: str
    secret_key: str
    auth_code: str
    base_url: str
    redirect_uri: str

    repeater: Optional[RepeaterConfigModel] = RepeaterConfigModel()
    rate_limiter: Optional[RateLimiterConfig] = RateLimiterConfig()
    storage: Optional[KeyValueStorageConfigModel] = KeyValueStorageConfigModel()
