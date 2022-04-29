from asyncio import AbstractEventLoop
from asyncio import get_event_loop
from logging import Logger
from typing import Optional

from amocrm_api_client.AmoCrmApiClient import AmoCrmApiClient
from amocrm_api_client.AmoCrmApiClientConfig import AmoCrmApiClientConfig
from amocrm_api_client.executor import ExecutorComponent
from amocrm_api_client.logger import api_client_logger

from amocrm_api_client.make_amocrm_request import ExceedRequestLimitException
from amocrm_api_client.make_amocrm_request import MakeAmocrmRequestFunctionImpl
from amocrm_api_client.make_json_request import MakeJsonRequestFunctionImpl
from amocrm_api_client.model_builder import ModelBuilderImpl
from amocrm_api_client.rate_limiter import IRateLimiterDecorator
from amocrm_api_client.rate_limiter import RateLimiterImpl
from amocrm_api_client.repeater import RepeaterDecoratorImpl

from amocrm_api_client.repositories import Account
from amocrm_api_client.repositories import CallsRepository
from amocrm_api_client.repositories import ContactsRepository
from amocrm_api_client.repositories import EventsRepository
from amocrm_api_client.repositories import LeadsRepository
from amocrm_api_client.repositories import PipelinesRepository
from amocrm_api_client.repositories import UnsortedRepository
from amocrm_api_client.repositories import UsersRepository
from amocrm_api_client.token_provider import ITokenProvider


__all__ = [
    "create_amocrm_api_client",
]


def create_amocrm_api_client(
    token_provider: ITokenProvider,
    config: Optional[AmoCrmApiClientConfig] = None,
    rate_limiter: Optional[IRateLimiterDecorator] = None,
    event_loop: Optional[AbstractEventLoop] = None,
    logger: Optional[Logger] = None,
) -> AmoCrmApiClient:

    logger = logger or api_client_logger

    if event_loop is None:
        event_loop = get_event_loop()

    if rate_limiter is None:
        rate_limiter = RateLimiterImpl(
            config=config.rate_limiter,
            trigger_exceptions=(ExceedRequestLimitException,),
        )

    repeater = RepeaterDecoratorImpl(
        config=config.repeater,
        trigger_exceptions=(ExceedRequestLimitException,),
    )

    make_amocrm_request_function = MakeAmocrmRequestFunctionImpl(
        base_url=config.base_url,
        make_json_request_function=MakeJsonRequestFunctionImpl(),
        token_provider=token_provider,
    )

    executor_component = ExecutorComponent(
        rate_limiter=rate_limiter,
        repeater=repeater,
        event_loop=event_loop,
        logger=logger,
    )

    model_builder = ModelBuilderImpl()

    leads_repository = LeadsRepository(
        request_executor=executor_component,
        make_amocrm_request_function=make_amocrm_request_function,
        model_builder=model_builder,
    )

    account = Account(
        request_executor=executor_component,
        make_amocrm_request_function=make_amocrm_request_function,
        model_builder=model_builder,
    )
    unsorted_repository = UnsortedRepository(
        request_executor=executor_component,
        make_amocrm_request_function=make_amocrm_request_function,
        model_builder=model_builder,
    )
    calls_repository = CallsRepository(
        request_executor=executor_component,
        make_amocrm_request_function=make_amocrm_request_function,
        model_builder=model_builder,
    )
    events_repository = EventsRepository(
        request_executor=executor_component,
        make_amocrm_request_function=make_amocrm_request_function,
        model_builder=model_builder,
    )
    pipelines_repository = PipelinesRepository(
        request_executor=executor_component,
        make_amocrm_request_function=make_amocrm_request_function,
        model_builder=model_builder,
    )
    contacts_repository = ContactsRepository(
        request_executor=executor_component,
        make_amocrm_request_function=make_amocrm_request_function,
        model_builder=model_builder,
    )
    users_repository = UsersRepository(
        request_executor=executor_component,
        make_amocrm_request_function=make_amocrm_request_function,
        model_builder=model_builder,
    )
    client = AmoCrmApiClient(
        executor_component=executor_component,
        leads_repository=leads_repository,
        account=account,
        contacts_repository=contacts_repository,
        unsorted_repository=unsorted_repository,
        pipelines_repository=pipelines_repository,
        events_repository=events_repository,
        calls_repository=calls_repository,
        users_repository=users_repository,
    )
    return client
