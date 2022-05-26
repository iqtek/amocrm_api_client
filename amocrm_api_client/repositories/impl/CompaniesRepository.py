from amocrm_api_client.make_json_request import RequestMethod

from amocrm_api_client.models import Company

from .AbstractRepository import AbstractRepository

__all__ = [
    "CompaniesRepository",
]


class CompaniesRepository(AbstractRepository):

    __slots__ = ()

    async def get_by_id(self, id: int) -> Company:
        response = await self._request_executor(
            lambda: self._make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/companies/{id}",
            )
        )
        model = self._model_builder.build_model(Company, response.json)
        return model
