from pydantic import BaseModel

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
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    responsible_user_id: Optional[int] = None
    group_id: Optional[int] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: int
    updated_at: int
    is_deleted: Optional[bool] = None
    closest_task_at: Optional[int] = None
    custom_fields_values: Optional[List[CustomFieldValue]] = None
    account_id: int
