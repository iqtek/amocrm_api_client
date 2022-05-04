from typing import Collection

from amocrm_api_client.make_json_request import RequestMethod
from amocrm_api_client.models import Pipeline

from .AbstractRepository import AbstractRepository


__all__ = [
    "PipelinesRepository",
]


class PipelinesRepository(AbstractRepository):

    __slots__ = ()

    async def get_all(self) -> Collection[Pipeline]:
        response = await self._request_executor(
            lambda: self._make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/leads/pipelines",
            )
        )
        data = response.json["_embedded"]["pipelines"]
        models = self._model_builder.build_models(
            model_type=Pipeline,
            data=data,
        )
        return models
