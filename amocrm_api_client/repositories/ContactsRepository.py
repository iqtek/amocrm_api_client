import typing as t

from amocrm_api_client.models import Page
from amocrm_api_client.models import Contact

from .utils import AbstractRepository, Paginable, make_query_parameters, build_model


__all__ = ["ContactsRepository"]


class ContactsRepository(Paginable[Contact], AbstractRepository):

    __slots__ = ()

    async def get_page(
        self,
        _with: t.Optional[t.Collection[str]] = None,
        page: int = 1,
        limit: int = 250,
        query: t.Optional[t.Union[str, int]] = None,
        filter: str = None,
    ) -> Page[Contact]:
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/api/v4/contacts?filter[custom_fields_values][{field_id}][]={value}",
                parameters=make_query_parameters(_with=_with, page=page, limit=limit, query=query),
            )
        )

        response["_embedded"] = response["_embedded"]["contacts"]
        return build_model(model_type=Page[Contact], data=response)

    async def get_by_id(
        self,
        id: int
    ) -> Contact:
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/api/v4/contacts/{id}",
            )
        )
        return build_model(Contact, response)

    async def smart_redirect(self, phone: str) -> t.Collection[Contact]:
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/private/api/v2/json/contacts/list",
                parameters={"query": phone}
            )
        )

        return [
            build_model(Contact, json_contact)
            for json_contact in response["response"]["contacts"]
        ]
