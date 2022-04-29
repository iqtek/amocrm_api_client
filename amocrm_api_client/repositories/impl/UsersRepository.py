from typing import Collection
from typing import Optional
from typing import Union

from amocrm_api_client.make_json_request import IJsonResponse
from amocrm_api_client.make_json_request import RequestMethod
from amocrm_api_client.models import Page
from amocrm_api_client.models.user import User

from .AbstractRepository import AbstractRepository
from ..core import IPaginable


__all__ = [
    "UsersRepository",
]


class UsersRepository(IPaginable[User], AbstractRepository):

    __slots__ = ()

    async def get_page(
        self,
        _with: Optional[Collection[str]] = None,
        page: int = 1,
        limit: int = 250,
        query: Optional[Union[str, int]] = None
    ) -> Page[User]:
        response: IJsonResponse = await self._request_executor(
            lambda: self._make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/users",
            )
        )
        response.json["_embedded"] = response.json["_embedded"]["users"]
        model = self._model_builder.build_model(
            model_type=Page[User],
            data=response.json,
        )
        return model
