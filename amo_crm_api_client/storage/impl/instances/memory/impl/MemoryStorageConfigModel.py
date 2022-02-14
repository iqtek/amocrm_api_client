from typing import Optional
from pydantic import BaseModel


__all__ = [
    "MemoryStorageConfigModel",
]


class MemoryStorageConfigModel(BaseModel):
    backup_file_path: str = "backup.txt"
    encryption_key: str = "secret"
