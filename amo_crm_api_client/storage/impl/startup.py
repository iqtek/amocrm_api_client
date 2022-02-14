from typing import Optional
from amo_crm_api_client.logger import (
    get_logger,
    ILogger,
)
from .FactoryStoreImpl import FactoryStoreImpl
from .instances import (
    MemoryKeyValueStorageFactory,
    RedisKeyValueStorageFactory,
)
from .KeyValueStorageConfigModel import KeyValueStorageConfigModel
from ..core import IKeyValueStorageFactory


__all__ = [
    "handle_startup",
]


def handle_startup(
    config: KeyValueStorageConfigModel,
    logger: Optional[ILogger] = None,
) -> IKeyValueStorageFactory:

    selected_type = config.type
    storage_config = config.settings

    logger = logger or get_logger()
    factory_store = FactoryStoreImpl()

    factory_store.register_factory(
        MemoryKeyValueStorageFactory(
            config=storage_config,
            logger=logger,
        )
    )

    factory_store.register_factory(
        RedisKeyValueStorageFactory(
            config=storage_config,
            logger=logger,
        )
    )
    storage_factory = factory_store.get_instance(
        type=selected_type,
    )

    return storage_factory
