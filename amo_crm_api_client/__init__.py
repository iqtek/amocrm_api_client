from .AmoCrmApiClient import AmoCrmApiClient
from .AmoCrmApiClientConfig import (
    AmoCrmApiClientConfig,
    AmoCrmApiClientConfig,
    KeyValueStorageConfigModel,
    MemoryStorageConfigModel,
    RateLimiterConfig,
    RedisStorageConfigModel,
    RepeaterConfigModel,
)
from .create_amo_crm_api_client import create_amo_crm_api_client

__package_name__: str = 'amo_crm_api_client'
__description__: str = 'Api Client for AmoCrm'
__license__: str = 'MIT'
__version__: str = '1.0.0'


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


VERSION = tuple(map(int_or_str, __version__.split(".")))


__all__ = [
    "AmoCrmApiClientConfig",
    "KeyValueStorageConfigModel",
    "MemoryStorageConfigModel",
    "RateLimiterConfig",
    "RedisStorageConfigModel",
    "RepeaterConfigModel",
    "AmoCrmApiClient",
    "create_amo_crm_api_client",

    "__package_name__",
    "__description__",
    "__version__",
    "__license__",
]
