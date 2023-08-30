from amocrm_api_client.models import Task

from .utils import AbstractRepository, build_model


__all__ = ["TasksRepository"]


class TasksRepository(AbstractRepository):

    __slots__ = ()

    async def get_by_id(
        self,
        id: int
    ) -> Task:
        response = await self._request_executor(
            lambda: self._make_amocrm_request(
                method="GET",
                path=f"/api/v4/tasks/{id}",
            )
        )
        return build_model(Task, response)
