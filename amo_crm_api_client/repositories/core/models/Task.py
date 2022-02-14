from datetime import (
    datetime
)
from pydantic import (
    BaseModel
)


__all__ = [
    "Task",
]


class Task(BaseModel):
    id: int
    created_by: int
    updated_by: int
    created_at: datetime
    updated_at: datetime
    responsible_user_id: int
    group_id: int
    entity_id: int
    entity_type: str
    duration: int
    is_completed: bool
    task_type_id: int
    text: str
    complete_till: datetime
    account_id: int
