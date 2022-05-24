from typing import Collection, Optional, Union

from amocrm_api_client.make_json_request import RequestMethod

from amocrm_api_client.models import Page
from amocrm_api_client.models import Contact

from ..core import IPaginable
from .AbstractRepository import AbstractRepository


__all__ = [
    "ContactsRepository",
]


class ContactsRepository(IPaginable[Contact], AbstractRepository):

    __slots__ = ()

    async def get_page(
        self,
        _with: Optional[Collection[str]] = None,
        page: int = 1,
        limit: int = 250,
        query: Optional[Union[str, int]] = None
    ) -> Page[Contact]:
        response = await self._request_executor(
            lambda: self._make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/contacts",
            )
        )
        response.json["_embedded"] = response.json["_embedded"]["contacts"]
        print(response.json)
        model = self._model_builder.build_model(
            model_type=Page[Contact],
            data=response.json,
        )
        return model

    async def get_by_id(
        self,
        id: int
    ) -> Contact:
        response = await self._request_executor(
            lambda: self._make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/contacts/{id}",
            )
        )
        model = self._model_builder.build_model(Contact, response.json)
        return model
