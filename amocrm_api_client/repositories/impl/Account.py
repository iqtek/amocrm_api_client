from typing import Collection
from typing import Optional

from amocrm_api_client.make_json_request import RequestMethod
from amocrm_api_client.models import Account as AccountModel

from .AbstractRepository import AbstractRepository
from .functions import make_params


__all__ = [
    "Account",
]


class Account(AbstractRepository):

    __slots__ = ()

    async def get_info(self, _with: Optional[Collection[str]] = None) -> AccountModel:
        params = make_params(_with=_with)

        response = await self._request_executor(
            lambda: self._make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/account",
                parameters=params,
            )
        )
        model = self._model_builder.build_model(AccountModel, response.json)
        return model
