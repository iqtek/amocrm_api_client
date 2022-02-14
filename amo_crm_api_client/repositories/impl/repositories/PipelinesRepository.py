from typing import (
    List,
)
from ...core import (
    IModelBuilder,
    Pipeline,
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
    "PipelinesRepository",
]


class PipelinesRepository:

    def __init__(
        self,
        worker_component: IWorkerExecutorComponent,
        make_amocrm_request_function: IMakeAmocrmRequestFunction,
        model_builder: IModelBuilder,
    ) -> None:
        self.__amo_crm_request_executor = worker_component
        self.__make_request_function = make_amocrm_request_function
        self.__model_builder = model_builder

    async def get_all(self) -> List[Pipeline]:
        response = await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/leads/pipelines",
            )
        )
        models = self.__model_builder.build_models(
            model_type=Pipeline,
            response=response,
        )
        return models

    async def get_by_id(self, id: int) -> Pipeline:
        response = await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/leads/pipelines/{id}",
            )
        )
        model = self.__model_builder.build_model(
            model_type=Pipeline,
            response=response,
        )
        return model
