from typing import List, Literal
from enum import (
    Enum
)
from ...core import (
    IModelBuilder,
)
from amo_crm_api_client.worker import (
    IWorkerExecutorComponent,
)
from amo_crm_api_client.make_amocrm_request import (
    RequestMethod,
    IJsonResponse,
    IMakeAmocrmRequestFunction,
)


__all__ = [
    "CallsRepository",
]


class CallsRepository:

    def __init__(
        self,
        worker_component: IWorkerExecutorComponent,
        make_amocrm_request_function: IMakeAmocrmRequestFunction,
        model_builder: IModelBuilder,
    ) -> None:
        self.__request_executor = worker_component
        self.__make_request_function = make_amocrm_request_function
        self.__model_builder = model_builder

    async def add(
        self,
        uniq: str,
        phone: str,
        direction: Literal["inbound", "outbound"],
        duration: int,
        source: str,
        call_status: int,
        created_at: int,
        responsible_user_id: int,
        call_result: str = None,
        created_by: int = None,
        updated_at: int = None,
        updated_by: int = None,
        link: str = None,
    ) -> IJsonResponse:
        json = {
            "add": {
                    "uniq": uniq,
                    "phone": phone,
                    "source": source,
                    "duration": duration,
                    "call_status": call_status,
                    "call_result": call_result,
                    "direction": direction,
                    "responsible_user_id": responsible_user_id,
                    "link": link,
                    "created_at": created_at,
                    "created_by": created_by or responsible_user_id,
                    "updated_at": updated_at,
                    "updated_by": updated_by or responsible_user_id,
                }

        }
        json2 = {"add": {}}
        for key in json["add"].keys():
            if json["add"][key] is not None:
                json2["add"][key] = json["add"][key]
        response = await self.__request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.POST,
                path=f"/api/v4/calls",
                json=json2,
            )
        )
        return response
