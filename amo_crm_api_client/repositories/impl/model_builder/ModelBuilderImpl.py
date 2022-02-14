from typing import (
    TypeVar,
    List,
    Type,
)
from pydantic import (
    BaseModel,
)
from amo_crm_api_client.make_amocrm_request import (
    IJsonResponse,
)
from ...core.model_builder.exceptions import (
    BuildModelException,
)
from ...core import (
    IModelBuilder,
)


__all__ = [
    "ModelBuilderImpl",
]


T = TypeVar("T", bound=BaseModel)


class ModelBuilderImpl(IModelBuilder):

    def build_model(
        self,
        model_type: Type[T],
        response: IJsonResponse,
    ) -> T:
        try:
            return model_type(**response.json)
        except Exception as e:
            raise BuildModelException from e

    def build_models(
        self,
        model_type: Type[T],
        response: IJsonResponse,
    ) -> List[T]:
        try:
            return [model_type(**item) for item in response.json]
        except Exception as e:
            raise BuildModelException from e
