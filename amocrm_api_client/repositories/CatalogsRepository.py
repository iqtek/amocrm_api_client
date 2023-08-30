import typing as t

from amocrm_api_client.models import Page
from amocrm_api_client.models import Catalog
from amocrm_api_client.models import Element
from amocrm_api_client.models import CatalogElement

from .utils import Paginable, make_query_parameters, build_model, AbstractRepository


__all__ = ["CatalogsRepository"]


class CatalogsRepository(Paginable[Catalog], AbstractRepository):

    __slots__ = ()

    async def get_page(
        self,
        _with: t.Optional[t.Collection[str]] = None,
        page: int = 1,
        limit: int = 250,
        query: t.Optional[t.Union[str, int]] = None
    ) -> Page[Catalog]:
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/api/v4/catalogs",
            )
        )
        response["_embedded"] = response["_embedded"]["catalogs"]
        return build_model(model_type=Page[Catalog], data=response.json)

    async def get_page_elements(
        self,
        catalog_id: int,
        _with: t.Optional[t.Collection[str]] = None,
        page: int = 1,
        limit: int = 250,
        query: t.Optional[t.Union[str, int]] = None
    ) -> Page[Element]:
        # TODO
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/api/v4/catalogs/{catalog_id}/elements",
            )
        )
        response["_embedded"] = response["_embedded"]["elements"]
        return build_model(model_type=Page[Element], data=response)

    async def get_catalog_element(
        self,
        catalog_id: int,
        element_id: int
    ) -> CatalogElement:
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/api/v4/catalogs/{catalog_id}/elements/{element_id}",
            )
        )
        return build_model(CatalogElement, response)
