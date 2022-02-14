from amo_crm_api_client.logger import ILogger
from .RedisConnectionFactory import RedisConnectionFactoryImpl
from .RedisKeyValueStorage import RedisKeyValueStorage
from .RedisStorageConfigModel import RedisStorageConfigModel
from ....core import (
    IKeyValueStorageFactory,
)

__all__ = [
    "RedisKeyValueStorageFactory",
]


class RedisKeyValueStorageFactory(IKeyValueStorageFactory):

    __slots__ = (
        "__config",
        "__logger",
    )

    def __init__(
        self,
        logger: ILogger,
        config: RedisStorageConfigModel,
    ) -> None:
        self.__logger = logger
        self.__config = config

    @classmethod
    def type(cls) -> str:
        return "redis"

    def get_instance(self, prefix: str = None) -> RedisKeyValueStorage:

        redis_conn_factory = RedisConnectionFactoryImpl(self.__config)
        connection = redis_conn_factory.get_instance()

        return RedisKeyValueStorage(
            connection=connection,
            prefix=prefix,
            logger=self.__logger,
        )
