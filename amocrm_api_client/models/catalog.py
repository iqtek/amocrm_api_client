import typing as t

from pydantic import BaseModel


__all__ = [
    "Catalog",
    "CatalogElement",
]


class Catalog(BaseModel):
    id: int
    name: str
    created_by: int
    updated_by: int
    created_at: int
    updated_at: int


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


class CatalogElement(BaseModel):
    id: int
    name: str
    created_by: int
    updated_by: int
    created_at: int
    updated_at: int
    is_deleted: t.Optional[bool]
    custom_fields_values: t.Optional[t.List[CustomFieldValue]] = None
    catalog_id: int
    account_id: int
