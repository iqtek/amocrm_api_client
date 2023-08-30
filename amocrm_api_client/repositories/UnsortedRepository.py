from amocrm_api_client.models.unsorted import UnsortedCall

from .utils import AbstractRepository


__all__ = ["UnsortedRepository"]


class UnsortedRepository(AbstractRepository):

    __slots__ = ()

    async def add_call(self, call: UnsortedCall) -> None:
        data = call.dict(exclude_none=True)
        data["metadata"]["from"] = data["metadata"].pop("from_")
        await self._request_executor(
            lambda: self._make_amocrm_request(
                method="POST",
                path=f"/api/v4/leads/unsorted/sip",
                json=[data],
            )
        )
