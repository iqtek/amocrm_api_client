import typing as t
import datetime as dt

from pydantic import BaseModel


__all__ = [
    "Task",
]


class Task(BaseModel):
    id: int
    created_by: t.Optional[int] = None
    updated_by: t.Optional[int] = None
    created_at: dt.datetime
    updated_at: dt.datetime
    responsible_user_id: t.Optional[int] = None
    group_id: t.Optional[int] = None
    entity_id: t.Optional[int] = None
    entity_type: t.Optional[str] = None
    duration: t.Optional[int] = None
    is_completed: t.Optional[bool] = None
    task_type_id: t.Optional[int] = None
    text: t.Optional[str] = None
    complete_till: t.Optional[dt.datetime] = None
    account_id: t.Optional[int] = None
