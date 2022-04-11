from ...core import (
    IModelBuilder,
    ContactsPage,
    Contact,
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
    "ContactRepository",
]


class ContactRepository:

    def __init__(
        self,
        worker_component: IWorkerExecutorComponent,
        make_amocrm_request_function: IMakeAmocrmRequestFunction,
        model_builder: IModelBuilder,
    ) -> None:
        self.__amo_crm_request_executor = worker_component
        self.__make_request_function = make_amocrm_request_function
        self.__model_builder = model_builder

    async def get_by_id(self, id: int) -> Contact:
        response: IJsonResponse = await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/contacts/{id}",
            )
        )
        model = self.__model_builder.build_model(
            model_type=Contact,
            response=response,
        )
        return model

    async def get_page_by_phone_number(self, phone_number: str, page: Optional[int] = 0) -> ContactsPage:
        response: IJsonResponse = await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/contacts",
                parameters={
                    "page": page,
                    "query": phone_number,
                    "with": "leads",
                }
            )
        )
        models = self.__model_builder.build_model(
            model_type=ContactsPage,
            response=response,
        )
        return models
