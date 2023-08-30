import typing as t

from amocrm_api_client.models import Page, User

from .utils import Paginable, make_query_parameters, AbstractRepository, build_model


__all__ = ["UsersRepository"]


class UsersRepository(Paginable[User], AbstractRepository):

    __slots__ = ()

    async def get_page(
        self,
        _with: t.Optional[t.Collection[str]] = None,
        page: int = 1,
        limit: int = 250,
        query: t.Optional[t.Union[str, int]] = None
    ) -> Page[User]:
        params = make_query_parameters(_with=_with, page=page, limit=limit, query=query)
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/api/v4/users",
                parameters=params,
            )
        )
        response["_embedded"] = response["_embedded"]["users"]
        return build_model(model_type=Page[User], data=response)
