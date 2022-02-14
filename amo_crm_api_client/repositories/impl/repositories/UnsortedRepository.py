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
    "UnsortedRepository",
]


class UnsortedRepository:

    def __init__(
        self,
        worker_component: IWorkerExecutorComponent,
        make_amocrm_request_function: IMakeAmocrmRequestFunction,
    ) -> None:
        self.__amo_crm_request_executor = worker_component
        self.__make_request_function = make_amocrm_request_function

    async def add_call(
        self,
        uniq: str,
        caller: str,
        called: str,
        duration: int,
        source_name: str,
        source_uid: str,
        service_code: str,
        created_at: int,
        pipeline_id: int,
        link: str = None,
    ) -> IJsonResponse:
        json = {
            "add": {
                "source_name": source_name,
                "source_uid": source_uid,
                "pipeline_id": pipeline_id,
                "created_at": created_at,
                "metadata": {
                    "is_call_event_needed": True,
                    "duration": duration,
                    "service_code": service_code,
                    "link": link,
                    "phone": called,
                    "called_at": created_at,
                    "from": caller,
                    "uniq": uniq,
                }
            }
        }
        response = await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.POST,
                path=f"/api/v4/leads/unsorted/sip",
                json=json,
            )
        )
        return response
