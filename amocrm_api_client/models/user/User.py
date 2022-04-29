from typing import Optional

from pydantic import BaseModel


__all__ = [
    "User",
]


class Rights(BaseModel):
    mail_access: bool
    catalog_access: bool
    is_admin: bool
    is_free: bool
    is_active: bool
    group_id: Optional[int] = None
    role_id: Optional[int] = None


class User(BaseModel):
    id: int
    name: str
    email: str
    lang: str
    rights: Rights
