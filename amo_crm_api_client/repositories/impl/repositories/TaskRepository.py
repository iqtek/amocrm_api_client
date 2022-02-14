from ...core import (
    IModelBuilder,
    Task,
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
    "TaskRepository",
]


class TaskRepository:

    def __init__(
        self,
        worker_component: IWorkerExecutorComponent,
        make_amocrm_request_function: IMakeAmocrmRequestFunction,
        model_builder: IModelBuilder,
    ) -> None:
        self.__amo_crm_request_executor = worker_component
        self.__make_request_function = make_amocrm_request_function
        self.__model_builder = model_builder

    async def get_by_id(self, id: int) -> Task:
        response = await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/tasks/{id}",
            )
        )
        model = self.__model_builder.build_model(
            model_type=Task,
            response=response,
        )
        return model
