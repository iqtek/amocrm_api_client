import typing as t

from pydantic import BaseModel


__all__ = [
    "Contact",
]


class Value(BaseModel):
    value: str
    enum_id: t.Optional[int] = None
    enum_code: t.Optional[str] = None


class CustomFieldValue(BaseModel):
    field_id: int
    field_name: str
    field_code: t.Optional[str] = None
    field_type: str
    values: t.List[Value]


class Contact(BaseModel):
    id: int
    name: t.Optional[str] = None
    first_name: t.Optional[str] = None
    last_name: t.Optional[str] = None
    responsible_user_id: t.Optional[int] = None
    group_id: t.Optional[int] = None
    created_by: t.Optional[int] = None
    updated_by: t.Optional[int] = None
    created_at: t.Optional[int] = None
    updated_at: t.Optional[int] = None
    is_deleted: t.Optional[bool] = None
    closest_task_at: t.Optional[int] = None
    custom_fields_values: t.Optional[t.List[CustomFieldValue]] = None
    account_id: int
