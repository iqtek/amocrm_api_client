from datetime import (
    datetime
)
from pydantic import (
    BaseModel,
    Field
)
from typing import (
    Optional,
    List,
)


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


class Lead(BaseModel):
    id: int


class Embedded(BaseModel):
    leads: Optional[List[Lead]] = None


class GetsLead(BaseModel):
    page: int = Field(..., alias='_page')
    embedded: Embedded = Field(..., alias='_embedded')


class Contact(BaseModel):
    id: int
    name: str
    first_name: str
    last_name: str
    responsible_user_id: int
    created_at: datetime
    updated_at: datetime
    group_id: int
    created_by: int
    updated_by: int
    custom_fields_values: List[CustomFieldValue]
    embedded: Optional[Embedded] = Field(..., alias='_embedded')
