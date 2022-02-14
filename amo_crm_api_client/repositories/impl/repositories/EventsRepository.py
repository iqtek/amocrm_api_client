from typing import (
    List,
)
from ...core import (
    IModelBuilder,
)
from amo_crm_api_client.worker import (
    IWorkerExecutorComponent,
    TaskPriority,
)
from amo_crm_api_client.make_amocrm_request import (
    RequestMethod,
    IJsonResponse,
    IMakeAmocrmRequestFunction,
)


__all__ = [
    "EventsRepository",
]


class EventsRepository:

    def __init__(
        self,
        worker_component: IWorkerExecutorComponent,
        make_amocrm_request_function: IMakeAmocrmRequestFunction,
        model_builder: IModelBuilder,
    ) -> None:
        self.__request_executor = worker_component
        self.__make_request_function = make_amocrm_request_function
        self.__model_builder = model_builder

    async def add_card(self, phone_number: str, users: List[int]) -> IJsonResponse:
        json = {
            "add": [
                {
                    "type": "phone_call",
                    "phone_number": phone_number,
                    "users": users,
                }
            ]
        }
        response = await self.__request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.POST,
                path=f"/api/v2/events",
                json=json,
            )
        )
        return response
