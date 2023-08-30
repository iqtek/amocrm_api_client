import typing as t

from pydantic import BaseModel, Field


__all__ = ["AddCall"]


class AddCall(BaseModel):
    uniq: t.Optional[str] = None
    direction: t.Literal["inbound", "outbound"]
    duration: int
    source: str
    link: t.Optional[str] = None
    phone: str
    call_result: t.Optional[str] = None
    call_status: t.Optional[int] = Field(None, ge=1, le=7)
    responsible_user_id: t.Optional[int] = None
    created_by: t.Optional[int] = None
    updated_by: t.Optional[int] = None
    created_at: t.Optional[int] = None
    updated_at: t.Optional[int] = None
