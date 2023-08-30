import typing as t

from pydantic import BaseModel


__all__ = [
    "BaseLead",
]


class BaseLead(BaseModel):
    name: t.Optional[str] = None
    price: t.Optional[int] = None
    status_id: t.Optional[int] = None
    pipeline_id: t.Optional[int] = None
    created_by: t.Optional[int] = None
    updated_by: t.Optional[int] = None
    closed_at: t.Optional[int] = None
    updated_at: t.Optional[int] = None
    loss_reason_id: t.Optional[int] = None
    responsible_user_id: t.Optional[int] = None
    custom_fields_values: t.Optional[t.List] = None
