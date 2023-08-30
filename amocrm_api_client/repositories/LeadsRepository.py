import typing as t

from amocrm_api_client.models import AddNote
from amocrm_api_client.models import CreateLead
from amocrm_api_client.models import Lead
from amocrm_api_client.models import Page
from amocrm_api_client.models import UpdateLead

from .utils import AbstractRepository, Paginable, build_model, make_query_parameters


__all__ = ["LeadsRepository"]


class LeadsRepository(Paginable[Lead], AbstractRepository):

    __slots__ = ()

    async def get_page(
        self,
        _with: t.Optional[t.Collection[str]] = None,
        page: int = 1,
        limit: int = 250,
        query: t.Optional[t.Union[str, int]] = None,
    ) -> Page[Lead]:
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/api/v4/leads",
                parameters=make_query_parameters(_with=_with, page=page, limit=limit, query=query),
            )
        )
        response["_embedded"] = response["_embedded"]["leads"]
        return build_model(Page[Lead], response)

    async def get_by_id(
        self,
        id: int,
        _with: t.Optional[t.Collection[str]] = None
    ) -> Lead:
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/api/v4/leads/{id}",
                parameters=make_query_parameters(_with=_with),
            )
        )
        return build_model(Lead, response)

    async def add(self, new_lead: CreateLead) -> None:
        await self._request_executor(
            lambda: self._make_amocrm_request(
                method="POST",
                path=f"/api/v4/leads",
                json=[new_lead.dict(by_alias=True, exclude_none=True)]
            )
        )

    async def update(self, lead: UpdateLead) -> None:
        await self._request_executor(
            lambda: self._make_amocrm_request(
                method="PATCH",
                path=f"/api/v4/leads",
                json=[lead.dict(by_alias=True, exclude_none=True)]
            )
        )

    async def updates(self, leads: t.Collection[UpdateLead]) -> None:
        await self._request_executor(
            lambda: self._make_amocrm_request(
                method="PATCH",
                path=f"/api/v4/leads",
                json=[lead.dict(by_alias=True, exclude_none=True) for lead in leads]
            )
        )

    async def add_notes(self, notes: t.Collection[AddNote]) -> None:
        await self._request_executor(
            lambda: self._make_amocrm_request(
                method="POST",
                path=f"/api/v4/leads/notes",
                json=[note.dict() for note in notes]
            )
        )
