from typing import Optional
from typing import Sequence

from pydantic import BaseModel


__all__ = [
    "BaseLead",
]


class BaseLead(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    status_id: Optional[int] = None
    pipeline_id: Optional[int] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    closed_at: Optional[int] = None
    updated_at: Optional[int] = None
    loss_reason_id: Optional[int] = None
    responsible_user_id: Optional[int] = None
    custom_fields_values: Optional[Sequence] = None
