from typing import List
from ...core import IModelBuilder, UsersPage
from amo_crm_api_client.worker import (
    IWorkerExecutorComponent,
)
from amo_crm_api_client.make_amocrm_request import (
    RequestMethod,
    IJsonResponse,
    IMakeAmocrmRequestFunction,
)


__all__ = [
    "UsersRepository",
]


class UsersRepository:

    def __init__(
        self,
        worker_component: IWorkerExecutorComponent,
        make_amocrm_request_function: IMakeAmocrmRequestFunction,
        model_builder: IModelBuilder,
    ) -> None:
        self.__amo_crm_request_executor = worker_component
        self.__make_request_function = make_amocrm_request_function
        self.__model_builder = model_builder

    async def get_all(self) -> UsersPage:
        response: IJsonResponse = await self.__amo_crm_request_executor(
            lambda: self.__make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/users",
            )
        )
        model = self.__model_builder.build_model(
            model_type=UsersPage,
            response=response,
        )
        return model
