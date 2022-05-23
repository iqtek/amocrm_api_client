from amocrm_api_client.make_json_request import RequestMethod
from amocrm_api_client.models import Task

from .AbstractRepository import AbstractRepository

__all__ = [
    "TasksRepository",
]


class TasksRepository(AbstractRepository):

    __slots__ = ()

    async def get_by_id(
        self,
        id: int
    ) -> Task:
        response = await self._request_executor(
            lambda: self._make_request_function.request(
                method=RequestMethod.GET,
                path=f"/api/v4/tasks/{id}",
            )
        )
        model = self._model_builder.build_model(Task, response.json)
        return model
