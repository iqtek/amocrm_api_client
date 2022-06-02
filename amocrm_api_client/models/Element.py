from pydantic import BaseModel

__all__ = [
    "Element",
]


class Element(BaseModel):
    id: int
    name: str
    created_by: int
    updated_by: int
    created_at: int
    updated_at: int
