import typing as t

from amocrm_api_client.models import AddCall

from .utils import AbstractRepository


__all__ = ["CallsRepository"]


class CallsRepository(AbstractRepository):

    __slots__ = ()

    async def add(
        self,
        call: AddCall,
        priority: int = 0,
        ttl: t.Optional[float] = None,
    ) -> None:
        await self._request_executor(
            lambda: self._make_amocrm_request(
                method="POST",
                path=f"/api/v4/calls",
                json=[call.dict(exclude_none=True)],
            ),
            priority=priority,
            ttl=ttl,
        )
