from amocrm_api_client.make_json_request import RequestMethod

from amocrm_api_client.models.unsorted import UnsortedCall

from .AbstractRepository import AbstractRepository


__all__ = [
    "UnsortedRepository",
]


class UnsortedRepository(AbstractRepository):

    __slots__ = ()

    async def add_call(self, call: UnsortedCall) -> None:
        await self._request_executor(
            lambda: self._make_request_function.request(
                method=RequestMethod.POST,
                path=f"/api/v4/leads/unsorted/sip",
                json=[call.dict(exclude_none=True)],
            )
        )
