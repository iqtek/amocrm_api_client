from typing import Optional
from typing import Sequence

from pydantic import BaseModel
from pydantic import Field

from ..Tag import Tag

__all__ = [
    "Lead",
    "CreateLead",
]


class Contact(BaseModel):
    id: int


class Company(BaseModel):
    id: int


class CatalogElementMetaData(BaseModel):
    catalog_id: Optional[int] = None


class CatalogElement(BaseModel):
    id: Optional[int] = None
    metadata: Optional[CatalogElementMetaData] = None


class Embedded(BaseModel):
    tags: Optional[Sequence[Tag]] = None
    contacts: Optional[Sequence[Contact]] = None
    companies: Optional[Sequence[Company]] = None
    catalog_elements: Optional[Sequence[CatalogElement]] = None


class Lead(BaseModel):
    id: int
    name: Optional[str] = None
    price: Optional[int] = None
    responsible_user_id: Optional[int] = None
    group_id: Optional[int] = None
    status_id: Optional[int] = None
    pipeline_id: Optional[int] = None
    loss_reason_id: Optional[int] = None
    source_id: Optional[int] = None
    created_by: int
    updated_by: int
    closed_at: Optional[int] = None
    created_at: int
    updated_at: int
    closest_task_at: Optional[int] = None
    is_deleted: bool
    custom_fields_values: Optional[Sequence] = None
    score: Optional[int] = None
    account_id: Optional[int] = None
    is_price_modified_by_robot: Optional[bool] = None
    embedded: Embedded = Field(..., alias='_embedded')
