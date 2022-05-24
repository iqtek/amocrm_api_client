from typing import Union

from pydantic import BaseModel

__all__ = [
    "AddNote",
]


class ServiceMessageParams(BaseModel):
    service: str
    text: str


class AddNote(BaseModel):
    entity_id: int
    note_type: str
    params: Union[ServiceMessageParams,]
