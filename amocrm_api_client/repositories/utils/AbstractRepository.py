from amocrm_api_client.make_amocrm_request import MakeAmocrmRequestFunction
from amocrm_api_client.request_executor import ExecutorComponent


__all__ = ["AbstractRepository"]


class AbstractRepository:

    __slots__ = (
        "_request_executor",
        "_make_amocrm_request",
    )

    def __init__(
        self,
        request_executor: ExecutorComponent,
        make_amocrm_request: MakeAmocrmRequestFunction,
    ) -> None:
        self._request_executor = request_executor
        self._make_amocrm_request = make_amocrm_request
