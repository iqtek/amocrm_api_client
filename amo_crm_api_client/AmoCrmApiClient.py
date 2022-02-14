from amo_crm_api_client.component import IComponent
from amo_crm_api_client.worker import IWorkerExecutorComponent
from amo_crm_api_client.repositories import (
    PipelinesRepository,
    UnsortedRepository,
    CompanyRepository,
    ContactRepository,
    EventsRepository,
    CallsRepository,
    LeadRepository,
    TaskRepository,
    UsersRepository,
)


__all__ = [
    "AmoCrmApiClient",
]


class AmoCrmApiClient(IComponent):

    __slots__ = (
        "companies",
        "pipelines",
        "contacts",
        "unsorted",
        "events",
        "calls",
        "leads",
        "tasks",
        "users",
        "__worker"
        "__storage"
    )

    def __init__(
        self,
        worker_component: IComponent,
        company_repository: CompanyRepository,
        contact_repository: ContactRepository,
        unsorted_repository: UnsortedRepository,
        pipelines_repository: PipelinesRepository,
        events_repository: EventsRepository,
        calls_repository: CallsRepository,
        task_repository: TaskRepository,
        lead_repository: LeadRepository,
        users_repository: UsersRepository,
        storage: IComponent,
    ) -> None:
        self.leads = lead_repository
        self.companies = company_repository
        self.contacts = contact_repository
        self.tasks = task_repository
        self.unsorted = unsorted_repository
        self.calls = calls_repository
        self.pipelines = pipelines_repository,
        self.events = events_repository
        self.users = users_repository

        self.__worker = worker_component
        self.__storage = storage

    async def initialize(self) -> None:
        await self.__storage.initialize()
        await self.__worker.initialize()

    async def deinitialize(self) -> None:
        await self.__worker.deinitialize()
        await self.__storage.deinitialize()
