from typing import (
    Optional,
)
from pydantic import (
    BaseModel,
)


__all__ = [
    "BackupStorageFileConfigModel"
]


class BackupStorageFileConfigModel(BaseModel):

    backup_file_path: Optional[str] = "backup.txt"
    encryption_key: Optional[str] = "secret"
