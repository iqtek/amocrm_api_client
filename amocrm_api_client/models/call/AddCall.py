from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


__all__ = [
    "AddCall",
]


class AddCall(BaseModel):
    uniq: Optional[str] = None
    direction: Literal["inbound", "outbound"]
    duration: int
    source: str
    link: Optional[str] = None
    phone: str
    call_result: Optional[str] = None
    call_status: Optional[int] = Field(None, ge=1, le=7)
    responsible_user_id: Optional[int] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
