from typing import (
    Optional,
    Mapping,
    Union,
    Any,
)
from pydantic import BaseModel
from .instances import (
    RedisStorageConfigModel,
    MemoryStorageConfigModel,
)

__all__ = [
    "KeyValueStorageConfigModel",
]


class KeyValueStorageConfigModel(BaseModel):

    type: str = "memory"
    settings: Union[
        RedisStorageConfigModel,
        MemoryStorageConfigModel
    ] = MemoryStorageConfigModel()
