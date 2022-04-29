from typing import Any
from typing import Collection
from typing import Mapping
from typing import Type

from pydantic import BaseModel

from .exceptions import BuildModelException
from .IModelBuilder import IModelBuilder


__all__ = [
    "ModelBuilderImpl",
]


class ModelBuilderImpl(IModelBuilder[BaseModel]):

    __slots__ = ()

    def build_model(
        self,
        model_type: Type[BaseModel],
        data: Mapping[str, Any],
    ) -> BaseModel:
        try:
            return model_type(**data)
        except Exception as e:
            raise BuildModelException() from e

    def build_models(
        self,
        model_type: Type[BaseModel],
        data: Mapping[str, Any],
    ) -> Collection[BaseModel]:
        try:
            return [model_type(**item) for item in data]
        except Exception as e:
            raise BuildModelException() from e
