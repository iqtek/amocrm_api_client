from typing import Collection, Optional, Union

from amocrm_api_client.make_json_request import RequestMethod

from amocrm_api_client.models import Page
from amocrm_api_client.models import Catalog
from amocrm_api_client.models import CatalogElement

from ..core import IPaginable
from .AbstractRepository import AbstractRepository

__all__ = [
    "CatalogsRepository",
]


class CatalogsRepository(IPaginable[Catalog], AbstractRepository):

    __slots__ = ()

    async def get_page(
        self,
        _with: Optional[Collection[str]] = None,
        page: int = 1,
        limit: int = 250,
        query: Optional[Union[str, int]] = None
    ) -> Page[Catalog]:
        response = await self._request_executor(
            lambda: self._make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/catalogs",
            )
        )
        response.json["_embedded"] = response.json["_embedded"]["catalogs"]
        print(response.json)
        model = self._model_builder.build_model(
            model_type=Page[Catalog],
            data=response.json,
        )
        return model

    async def get_catalog_element(
        self,
        catalog_id: int,
        element_id: int
    ) -> CatalogElement:
        response = await self._request_executor(
            lambda: self._make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/catalogs/{catalog_id}/elements/{element_id}",
            )
        )
        model = self._model_builder.build_model(CatalogElement, response.json)
        return model
