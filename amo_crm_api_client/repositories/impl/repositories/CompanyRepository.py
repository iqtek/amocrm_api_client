from typing import (
    List,
)
from ...core import (
    IModelBuilder,
    Company,
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
    "CompanyRepository",
]


class CompanyRepository:

    def __init__(
        self,
        worker_component: IWorkerExecutorComponent,
        make_amocrm_request_function: IMakeAmocrmRequestFunction,
        model_builder: IModelBuilder,
    ) -> None:
        self.__request_executor = worker_component
        self.__make_request_function = make_amocrm_request_function
        self.__model_builder = model_builder

    async def get_by_id(self, id: int) -> Company:
        response = await self.__request_executor(
            lambda:  self.__make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/companies/{id}",
            )
        )
        model = self.__model_builder.build_model(
            model_type=Company,
            response=response,
        )
        return model

    async def gets_by_phone_number(self, phone_number: str) -> List[Company]:
        response = await self.__request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.GET,
                path=f"/companies",
                parameters={
                    "query": phone_number,
                    "with": "leads",
                }
            )
        )
        models = self.__model_builder.build_models(
            model_type=Company,
            response=response,
        )
        return models
