from amocrm_api_client.make_json_request import RequestMethod
from amocrm_api_client.models import AddCall

from .AbstractRepository import AbstractRepository


__all__ = [
    "CallsRepository",
]


class CallsRepository(AbstractRepository):

    __slots__ = ()

    async def add(self, call: AddCall) -> None:
        await self._request_executor(
            lambda: self._make_request_function.request(
                method=RequestMethod.POST,
                path=f"/api/v4/calls",
                json=[call.dict(exclude_none=True)],
            )
        )
