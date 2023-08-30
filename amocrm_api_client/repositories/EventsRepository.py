import typing as t

from .utils import AbstractRepository


__all__ = ["EventsRepository"]


class EventsRepository(AbstractRepository):

    __slots__ = ()

    async def add_card(self, phone_number: str, users: t.Collection[int]) -> None:
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
            lambda: self._make_amocrm_request(
                method="POST",
                path=f"/api/v2/events",
                json=json,
            )
        )
