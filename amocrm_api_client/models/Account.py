from typing import Any
from typing import Mapping
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic_collections import BaseCollectionModel


__all__ = [
    "Account",
    "AmojoRights",
    "UsersGroup",
    "TaskType",
    "DatetimeSettings",
    "AccountEmbedded",
]


class AmojoRights(BaseModel):
    can_direct: bool
    can_create_groups: bool


class UsersGroup(BaseModel):
    id: int
    name: str
    uuid: Optional[str] = None


class UsersGroups(BaseCollectionModel[UsersGroup]):
    pass


class TaskType(BaseModel):
    id: int
    name: str
    color: Optional[str] = None
    icon_id: Optional[str] = None
    code: Optional[str] = None


class TaskTypes(BaseCollectionModel[TaskType]):
    pass


class DatetimeSettings(BaseModel):
    date_pattern: str
    short_date_pattern: str
    short_time_pattern: str
    date_format: str
    time_format: str
    timezone: str
    timezone_offset: str


class AccountEmbedded(BaseModel):
    amojo_rights: Optional[AmojoRights] = None
    users_groups: Optional[UsersGroups] = None
    task_types: Optional[TaskTypes] = None
    datetime_settings: Optional[DatetimeSettings] = None
    entity_names: Optional[Mapping[str, Any]] = None


class Account(BaseModel):
    id: int
    name: str
    subdomain: str
    created_at: int
    created_by: int
    updated_at: int
    updated_by: int
    current_user_id: int
    country: str
    customers_mode: str
    is_unsorted_on: bool
    is_loss_reason_enabled: bool
    is_helpbot_enabled: bool
    is_technical_account: bool
    contact_name_display_order: int
    amojo_id: Optional[str] = None
    version: Optional[int] = None
    embedded: Optional[AccountEmbedded] = Field(None, alias='_embedded')
