from pydantic import BaseModel

from typing import Optional
from typing import List


__all__ = [
    "CatalogElement",
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


class CatalogElement(BaseModel):
    id: int
    name: str
    created_by: int
    updated_by: int
    created_at: int
    updated_at: int
    is_deleted: Optional[bool]
    custom_fields_values: Optional[List[CustomFieldValue]] = None
    catalog_id: int
    account_id: int
