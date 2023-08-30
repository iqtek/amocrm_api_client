import typing as t

from pydantic import BaseModel


__all__ = [
    "UserRights",
    "User",
]


class UserRights(BaseModel):
    mail_access: bool
    catalog_access: bool
    is_admin: bool
    is_free: bool
    is_active: bool
    group_id: t.Optional[int] = None
    role_id: t.Optional[int] = None


class User(BaseModel):
    id: int
    name: str
    email: str
    lang: str
    rights: UserRights
