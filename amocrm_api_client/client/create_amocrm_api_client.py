import functools
import logging
import typing as t

from amocrm_api_client.features import RepeaterDecorator, RateLimiterDecorator, RepeaterConfig
from amocrm_api_client.make_amocrm_request import DefaultMakeAmocrmRequestFunction
from amocrm_api_client.make_amocrm_request import ExceedRequestLimitException
from amocrm_api_client.make_amocrm_request import NotAuthorizedException, ApiAccessException

from amocrm_api_client.request_executor import DefaultExecutorComponent
from amocrm_api_client.token_provider import TokenProvider
from amocrm_api_client.utils import amocrm_api_client_logger

from amocrm_api_client.repositories import *

from .AmoCrmApiClientConfig import AmoCrmApiClientConfig
from .AmoCrmApiClient import AmoCrmApiClient


__all__ = ["create_amocrm_api_client"]


T = t.TypeVar('T', bound=t.Callable[[], t.Awaitable])


def create_amocrm_api_client(
    config: AmoCrmApiClientConfig,
    token_provider: TokenProvider,
    task_decorator: t.Optional[t.Callable[[T], T]] = None,
    logger: t.Optional[logging.Logger] = None,
) -> AmoCrmApiClient:
    logger = logger or amocrm_api_client_logger

    decorators_chain = [
        RepeaterDecorator(
            config=RepeaterConfig(
                tries=5,
                min_delay=0,
                max_delay=0,
                factor=1,
            ),
            trigger_exceptions=(NotAuthorizedException, ApiAccessException),
        )
    ]

    if config.rate_limiter is not None:
        decorators_chain.append(
            RateLimiterDecorator(
                config=config.rate_limiter,
                trigger_exceptions=(ExceedRequestLimitException,),
            )
        )

    if config.repeater is not None:
        decorators_chain.append(
            RepeaterDecorator(
                config=config.repeater,
                trigger_exceptions=(ExceedRequestLimitException,),
            )
        )

    if task_decorator is not None:
        decorators_chain.append(task_decorator)

    def request_decorator(__func):
        return functools.reduce(lambda func, deco: deco(func), decorators_chain, __func)

    make_amocrm_request_function = DefaultMakeAmocrmRequestFunction(
        base_url=config.base_url,
        token_provider=token_provider,
    )

    executor_component = DefaultExecutorComponent(
        task_decorator=request_decorator,
        logger=logger,
    )

    create = lambda repository_type: repository_type(
        request_executor=executor_component,
        make_amocrm_request=make_amocrm_request_function,
    )

    client = AmoCrmApiClient(
        executor_component=executor_component,
        leads_repository=create(LeadsRepository),
        tasks_repository=create(TasksRepository),
        account=create(AccountsRepository),
        contacts_repository=create(ContactsRepository),
        companies_repository=create(CompaniesRepository),
        catalogs_repository=create(CatalogsRepository),
        unsorted_repository=create(UnsortedRepository),
        pipelines_repository=create(PipelinesRepository),
        events_repository=create(EventsRepository),
        calls_repository=create(CallsRepository),
        users_repository=create(UsersRepository),
    )
    return client
