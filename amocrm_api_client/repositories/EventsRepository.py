from typing import Collection

from amocrm_api_client.make_json_request import IJsonResponse
from amocrm_api_client.make_json_request import RequestMethod

from .AbstractRepository import AbstractRepository


__all__ = [
    "EventsRepository",
]


class EventsRepository(AbstractRepository):

    __slots__ = ()

    async def add_card(self, phone_number: str, users: Collection[int]) -> None:
        json = {
            "add": [
                {
                    "type": "phone_call",
                    "phone_number": phone_number,
                    "users": users,
                }
            ]
        }
        await self._request_executor(
            lambda: self._make_request_function.request(
                method=RequestMethod.POST,
                path=f"/api/v2/events",
                json=json,
            )
        )
