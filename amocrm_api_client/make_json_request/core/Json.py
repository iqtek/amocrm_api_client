from typing import Mapping
from typing import Sequence
from typing import Union
from typing import Any

__all__ = [
    "Json",
]

# JsonSimpleType = Union[str, int, float, bool]
# JsonCollections = Union[Mapping[str, JsonSimpleType], Sequence[JsonSimpleType]]
#
# JsonType = Union[JsonCollections, JsonSimpleType, Mapping[str, 'JsonCollections']]
Json = Union[Mapping[str, Any], Sequence[Any]]
