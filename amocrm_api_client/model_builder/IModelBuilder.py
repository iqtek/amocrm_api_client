from typing import Any
from typing import Collection
from typing import Generic
from typing import Mapping
from typing import Type
from typing import TypeVar


__all__ = [
    "IModelBuilder",
]


T = TypeVar("T")


class IModelBuilder(Generic[T]):

    __slots__ = ()

    def build_model(
        self,
        model_type: Type[T],
        data: Mapping[str, Any],
    ) -> T:
        raise NotImplementedError()

    def build_models(
        self,
        model_type: Type[T],
        data: Mapping[str, Any],
    ) -> Collection[T]:
        raise NotImplementedError()
