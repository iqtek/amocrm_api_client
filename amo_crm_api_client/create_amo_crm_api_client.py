from asyncio import (
    AbstractEventLoop,
    get_event_loop,
)
from typing import Optional

from amo_crm_api_client.AmoCrmApiClient import AmoCrmApiClient
from amo_crm_api_client.AmoCrmApiClientConfig import AmoCrmApiClientConfig
from amo_crm_api_client.logger import get_logger
from amo_crm_api_client.logger import ILogger
from amo_crm_api_client.make_amocrm_request import handle_startup as crm_startup
from amo_crm_api_client.make_amocrm_request.core.exceptions import (
    ExceedRequestLimitException,
)
from amo_crm_api_client.rate_limiter import IRateLimiter
from amo_crm_api_client.repositories import (
    CallsRepository,
    CompanyRepository,
    ContactRepository,
    EventsRepository,
    LeadRepository,
    ModelBuilderImpl,
    PipelinesRepository,
    TaskRepository,
    UnsortedRepository,
    UsersRepository,
)
from amo_crm_api_client.storage import handle_startup as storage_startup
from amo_crm_api_client.storage import IKeyValueStorage
from amo_crm_api_client.worker import handle_startup as worker_startup
from .rate_limiter import SimpleRateLimiter
from .repeater import RepeaterDecoratorImpl


__all__ = [
    "create_amo_crm_api_client",
]


def create_amo_crm_api_client(
    config: AmoCrmApiClientConfig,
    key_value_storage: Optional[IKeyValueStorage] = None,
    rate_limiter: Optional[IRateLimiter] = None,
    event_loop: Optional[AbstractEventLoop] = None,
    logger: Optional[ILogger] = None,
) -> AmoCrmApiClient:

    if logger is None:
        logger = get_logger()

    if event_loop is None:
        event_loop = get_event_loop()

    if key_value_storage is None:
        key_value_storage_factory = storage_startup(
            config=config.storage,
            logger=logger,
        )
        prefix = config.storage.settings.prefix or "AmocrmApiClient"
        key_value_storage = key_value_storage_factory.get_instance(prefix)
    if rate_limiter is None:
        rate_limiter = SimpleRateLimiter(
            config=config.rate_limiter,
            trigger_exceptions=(ExceedRequestLimitException,),
            logger=logger,
        )
    repeater = RepeaterDecoratorImpl(
        config=config.repeater,
        trigger_exceptions=(ExceedRequestLimitException,),
        logger=logger,
    )
    make_amocrm_req = crm_startup(
        config=config,
        storage=key_value_storage,
        logger=logger,
    )
    worker_component = worker_startup(
        rate_limiter=rate_limiter,
        repeater=repeater,
        event_loop=event_loop,
    )
    model_builder = ModelBuilderImpl()

    lead_repository = LeadRepository(
        worker_component=worker_component,
        make_amocrm_request_function=make_amocrm_req,
        model_builder=model_builder,
    )
    unsorted_repository = UnsortedRepository(
        worker_component=worker_component,
        make_amocrm_request_function=make_amocrm_req,
    )
    calls_repository = CallsRepository(
        worker_component=worker_component,
        make_amocrm_request_function=make_amocrm_req,
        model_builder=model_builder,
    )
    events_repository = EventsRepository(
        worker_component=worker_component,
        make_amocrm_request_function=make_amocrm_req,
        model_builder=model_builder,
    )
    pipelines_repository = PipelinesRepository(
        worker_component=worker_component,
        make_amocrm_request_function=make_amocrm_req,
        model_builder=model_builder,
    )
    task_repository = TaskRepository(
        worker_component=worker_component,
        make_amocrm_request_function=make_amocrm_req,
        model_builder=model_builder,
    )
    company_repository = CompanyRepository(
        worker_component=worker_component,
        make_amocrm_request_function=make_amocrm_req,
        model_builder=model_builder,
    )
    contact_repository = ContactRepository(
        worker_component=worker_component,
        make_amocrm_request_function=make_amocrm_req,
        model_builder=model_builder,
    )
    users_repository = UsersRepository(
        worker_component=worker_component,
        make_amocrm_request_function=make_amocrm_req,
        model_builder=model_builder,
    )
    client = AmoCrmApiClient(
        worker_component=worker_component,
        lead_repository=lead_repository,
        company_repository=company_repository,
        contact_repository=contact_repository,
        unsorted_repository=unsorted_repository,
        pipelines_repository=pipelines_repository,
        events_repository=events_repository,
        calls_repository=calls_repository,
        task_repository=task_repository,
        users_repository=users_repository,
        storage=key_value_storage,
    )
    return client
