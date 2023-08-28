from amocrm_api_client.executor import IExecutorComponent
from amocrm_api_client.make_amocrm_request import IMakeAmocrmRequestFunction
from amocrm_api_client.model_builder import IModelBuilder


__all__ = [
    "AbstractRepository",
]


class AbstractRepository:

    __slots__ = (
        "_request_executor",
        "_make_request_function",
        "_model_builder",
    )

    def __init__(
        self,
        request_executor: IExecutorComponent,
        make_amocrm_request_function: IMakeAmocrmRequestFunction,
        model_builder: IModelBuilder,
    ) -> None:
        self._request_executor = request_executor
        self._make_request_function = make_amocrm_request_function
        self._model_builder = model_builder
