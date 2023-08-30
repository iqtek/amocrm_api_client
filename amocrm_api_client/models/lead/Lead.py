import typing as t
from pydantic import BaseModel, Field

from ..tag import Tag


__all__ = [
    "Lead",
    "CreateLead",
]


class Contact(BaseModel):
    id: int


class Company(BaseModel):
    id: int


class CatalogElementMetaData(BaseModel):
    catalog_id: t.Optional[int] = None


class CatalogElement(BaseModel):
    id: t.Optional[int] = None
    metadata: t.Optional[CatalogElementMetaData] = None


class Embedded(BaseModel):
    tags: t.Optional[t.List[Tag]] = None
    contacts: t.Optional[t.List[Contact]] = None
    companies: t.Optional[t.List[Company]] = None
    catalog_elements: t.Optional[t.List[CatalogElement]] = None


class Lead(BaseModel):
    id: int
    name: t.Optional[str] = None
    price: t.Optional[int] = None
    responsible_user_id: t.Optional[int] = None
    group_id: t.Optional[int] = None
    status_id: t.Optional[int] = None
    pipeline_id: t.Optional[int] = None
    loss_reason_id: t.Optional[int] = None
    source_id: t.Optional[int] = None
    created_by: int
    updated_by: int
    closed_at: t.Optional[int] = None
    created_at: int
    updated_at: int
    closest_task_at: t.Optional[int] = None
    is_deleted: bool
    custom_fields_values: t.Optional[t.List] = None
    score: t.Optional[int] = None
    account_id: t.Optional[int] = None
    is_price_modified_by_robot: t.Optional[bool] = None
    embedded: Embedded = Field(..., alias='_embedded')
