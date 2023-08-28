from amocrm_api_client.component import IComponent

from amocrm_api_client.repositories import Account
from amocrm_api_client.repositories import CallsRepository
from amocrm_api_client.repositories import CatalogsRepository
from amocrm_api_client.repositories import CompaniesRepository
from amocrm_api_client.repositories import ContactsRepository
from amocrm_api_client.repositories import EventsRepository
from amocrm_api_client.repositories import LeadsRepository
from amocrm_api_client.repositories import PipelinesRepository
from amocrm_api_client.repositories import TasksRepository
from amocrm_api_client.repositories import UnsortedRepository
from amocrm_api_client.repositories import UsersRepository


__all__ = ["AmoCrmApiClient"]


class AmoCrmApiClient(IComponent):

    __slots__ = (
        "account",
        "companies",
        "catalogs",
        "pipelines",
        "contacts",
        "unsorted",
        "events",
        "calls",
        "leads",
        "tasks",
        "users",
        "__executor_component",
    )

    def __init__(
        self,
        account: Account,
        contacts_repository: ContactsRepository,
        companies_repository: CompaniesRepository,
        catalogs_repository: CatalogsRepository,
        unsorted_repository: UnsortedRepository,
        pipelines_repository: PipelinesRepository,
        events_repository: EventsRepository,
        calls_repository: CallsRepository,
        leads_repository: LeadsRepository,
        tasks_repository: TasksRepository,
        users_repository: UsersRepository,
        executor_component: IComponent,
    ) -> None:
        self.leads = leads_repository
        self.tasks = tasks_repository
        self.account = account
        self.contacts = contacts_repository
        self.companies = companies_repository
        self.catalogs = catalogs_repository
        self.unsorted = unsorted_repository
        self.calls = calls_repository
        self.pipelines = pipelines_repository
        self.events = events_repository
        self.users = users_repository

        self.__executor_component = executor_component


    async def initialize(self) -> None:
        await self.__executor_component.initialize()

    async def deinitialize(self) -> None:
        await self.__executor_component.deinitialize()
