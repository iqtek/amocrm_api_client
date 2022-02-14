from datetime import (
    datetime
)
from pydantic import (
    BaseModel
)
from typing import (
    Optional,
    List,
)


__all__ = [
    "Company",
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


class Company(BaseModel):
    id: int
    name: str
    responsible_user_id: int
    created_at: datetime
    updated_at: datetime
    group_id: int
    created_by: int
    updated_by: int
    is_deleted: bool
    custom_fields_values: Optional[List[CustomFieldValue]]
