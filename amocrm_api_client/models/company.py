import datetime as dt
import typing as t

from pydantic import BaseModel


__all__ = ["Company"]


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


class Company(BaseModel):
    id: int
    name: str
    responsible_user_id: int
    created_at: dt.datetime
    updated_at: dt.datetime
    group_id: t.Optional[int] = None
    created_by: t.Optional[int] = None
    updated_by: t.Optional[int] = None
    is_deleted: bool
    custom_fields_values: t.Optional[t.List[CustomFieldValue]]
