from pydantic import BaseModel
from pydantic import Field

from typing import Optional
from typing import List


__all__ = [
    "Contact",
]


class Value(BaseModel):
    value: str
    enum_id: Optional[int] = None
    enum_code: Optional[str] = None


class CustomFieldValue(BaseModel):
    field_id: int
    field_name: str
    field_code: Optional[str] = None
    field_type: str
    values: List[Value]


class Contact(BaseModel):
    id: int
    name: str
    first_name: str
    last_name: str
    responsible_user_id: int
    group_id: int
    created_by: int
    updated_by: int
    created_at: int
    updated_at: int
    is_deleted: bool
    closest_task_at: Optional[int] = None
    custom_fields_values: Optional[List[CustomFieldValue]] = None
    account_id: int
