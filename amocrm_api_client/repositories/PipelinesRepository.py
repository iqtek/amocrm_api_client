import typing as t

from amocrm_api_client.models import Pipeline

from .utils import AbstractRepository, build_models


__all__ = ["PipelinesRepository"]


class PipelinesRepository(AbstractRepository):

    __slots__ = ()

    async def get_all(self) -> t.Collection[Pipeline]:
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/api/v4/leads/pipelines",
            )
        )
        data = response["_embedded"]["pipelines"]
        return build_models(model_type=Pipeline, data=data)
