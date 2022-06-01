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
    catalog_id: int


class CatalogElement(BaseModel):
    id: int
    metadata: CatalogElementMetaData


class Embedded(BaseModel):
    tags: Optional[Sequence[Tag]] = None
    contacts: Optional[Sequence[Contact]] = None
    companies: Optional[Sequence[Company]] = None
    catalog_elements: Optional[Sequence[CatalogElement]] = None


class Lead(BaseModel):
    id: int
    name: str
    price: int
    responsible_user_id: int
    group_id: int
    status_id: int
    pipeline_id: int
    loss_reason_id: Optional[int] = None
    source_id: Optional[int] = None
    created_by: int
    updated_by: int
    closed_at: Optional[int] = None
    created_at: int
    updated_at: int
    closest_task_at: Optional[int]
    is_deleted: bool
    custom_fields_values: Optional[Sequence] = None
    score: Optional[int] = None
    account_id: int
    is_price_modified_by_robot: Optional[bool] = None
    embedded: Embedded = Field(..., alias='_embedded')
