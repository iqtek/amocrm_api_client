from pydantic import BaseModel

__all__ = [
    "Catalog",
]


class Catalog(BaseModel):
    id: int
    name: str
    created_by: int
    updated_by: int
    created_at: int
    updated_at: int
