import typing as t

from amocrm_api_client.models import Account

from .utils import make_query_parameters, build_model, AbstractRepository


__all__ = ["AccountsRepository"]


class AccountsRepository(AbstractRepository):

    __slots__ = ()

    async def get_info(
        self,
        _with: t.Optional[t.Collection[str]] = None,
        priority: int = 0,
        ttl: t.Optional[float] = None,
    ) -> Account:
        params = make_query_parameters(_with=_with)
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/api/v4/account",
                parameters=params,
            ),
            priority=priority,
            ttl=ttl,
        )
        return build_model(Account, response)
