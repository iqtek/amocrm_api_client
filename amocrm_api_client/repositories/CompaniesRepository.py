from amocrm_api_client.models import Company

from .utils import AbstractRepository, build_model


__all__ = ["CompaniesRepository"]


class CompaniesRepository(AbstractRepository):

    __slots__ = ()

    async def get_by_id(self, id: int) -> Company:
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/api/v4/companies/{id}",
            )
        )
        return build_model(Company, response)
