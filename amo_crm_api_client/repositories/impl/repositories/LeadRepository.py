import asyncio
from typing import (
    Union,
    List,
)
from ...core import (
    IModelBuilder,
    GetsLead,
    Lead,
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
    "LeadRepository",
]


class LeadRepository:

    def __init__(
        self,
        worker_component: IWorkerExecutorComponent,
        make_amocrm_request_function: IMakeAmocrmRequestFunction,
        model_builder: IModelBuilder,
    ) -> None:
        self.__amo_crm_request_executor = worker_component
        self.__make_request_function = make_amocrm_request_function
        self.__model_builder = model_builder

    async def add(
        self,
        contact_id: int,
        name: str = None,
        price: int = None,
        status_id: int = None,
        pipeline_id: int = None,
        responsible_user_id: int = None,
        closed_at: int = None,
        created_at: int = None,
        created_by: int = None,
        updated_at: int = None,
        updated_by: int = None,
    ) -> IJsonResponse:
        json = {
            "add": {
                "name": name,
                "price": price,
                "status_id": status_id,
                "pipeline_id": pipeline_id,
                "closed_at": closed_at,
                "updated_at": updated_at,
                "updated_by": updated_by,
                "created_at": created_at,
                "created_by": created_by,
                "responsible_user_id": responsible_user_id,
                "_embedded": {
                    "contacts": [
                        {
                            "id": contact_id,
                            "is_main": True
                        }
                    ]
                }
            }
        }
        response = await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/leads",
                parameters={
                    "with": "leads",
                }
            )
        )
        return response

    async def get_by_id(self, id: int) -> Lead:

        response = await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/leads/{id}",
                parameters={
                    "with": "contacts",
                }
            )
        )
        model = self.__model_builder.build_model(
            model_type=Lead,
            response=response,
        )
        return model

    async def gets_by_query(self, query: Union[int, str]) -> List[GetsLead]:

        response = await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/leads",
                parameters={
                    "query": query,
                }
            )
        )
        models = self.__model_builder.build_models(
            model_type=GetsLead,
            response=response,
        )
        return models

    async def add_tag(self, id: int, text_tag: str) -> IJsonResponse:
        tag = {
            "_embedded": {
                "tags": [
                    {
                        "name": text_tag
                    }
                ]
            }
        }
        return await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.PATCH,
                path=f"/api/v4/leads/{id}",
                json=tag,
            )
        )

    async def add_comment(self, id: int, text_comment: str) -> IJsonResponse:
        comment = [{
            "note_type": "common",
            "params": {
                "text": text_comment
            }
        }]
        return await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.POST,
                path=f"/api/v4/leads/{id}/notes",
                json=comment,
            )
        )

    async def update_status(self, id: int, new_status_id: int) -> IJsonResponse:
        lead_status = {
            "status_id": new_status_id
        }
        return await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.PATCH,
                path=f"/api/v4/leads/{id}",
                json=lead_status,
            )
        )
