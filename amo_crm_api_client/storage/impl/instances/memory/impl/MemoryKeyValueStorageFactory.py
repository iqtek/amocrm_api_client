from amo_crm_api_client.logger import ILogger
from .backup_storage import BackupStorageFile, BackupStorageFileConfigModel
from .MemoryKeyValueStorage import MemoryKeyValueStorage
from .MemoryStorageConfigModel import MemoryStorageConfigModel
from .....core import IKeyValueStorage, IKeyValueStorageFactory


__all__ = [
    "MemoryKeyValueStorageFactory",
]


class MemoryKeyValueStorageFactory(IKeyValueStorageFactory):

    def __init__(
        self,
        config: MemoryStorageConfigModel,
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__logger = logger

    @classmethod
    def type(cls) -> str:
        return "memory"

    def get_instance(self, prefix: str = None) -> IKeyValueStorage:

        backup_storage_config = BackupStorageFileConfigModel(**self.__config.dict())
        backup_storage = BackupStorageFile(
            config=backup_storage_config,
        )
        return MemoryKeyValueStorage(
            logger=self.__logger,
            backup_storage=backup_storage,
            prefix=prefix,
        )
