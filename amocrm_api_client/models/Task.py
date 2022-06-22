from datetime import (
    datetime
)
from typing import Optional

from pydantic import (
    BaseModel
)


__all__ = [
    "Task",
]


class Task(BaseModel):
    id: int
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    responsible_user_id: Optional[int] = None
    group_id: Optional[int] = None
    entity_id: Optional[int] = None
    entity_type: Optional[str] = None
    duration: Optional[int] = None
    is_completed: Optional[bool] = None
    task_type_id: Optional[int] = None
    text: Optional[str] = None
    complete_till: Optional[datetime] = None
    account_id: Optional[int] = None
