from typing import (
    Generic,
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


__all__ = [
    "IModelBuilder",
]


T = TypeVar("T", bound=BaseModel)


class IModelBuilder(Generic[T]):

    def build_model(
        self,
        model_type: Type[T],
        response: IJsonResponse,
    ) -> T:
        raise NotImplementedError()

    def build_models(
        self,
        model_type: Type[T],
        response: IJsonResponse,
    ) -> List[T]:
        raise NotImplementedError()
