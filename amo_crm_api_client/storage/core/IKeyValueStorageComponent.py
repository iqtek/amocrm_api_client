from typing import (
    Optional,
)
from amo_crm_api_client.component import (
    IComponent,
)
from .IKeyValueStorage import (
    IKeyValueStorage,
)


__all__ = [
    "IKeyValueStorageComponent",
]


class IKeyValueStorageComponent(IComponent, IKeyValueStorage):
    pass
