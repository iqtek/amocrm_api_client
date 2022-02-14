from pydantic import BaseModel, PositiveInt, NonNegativeFloat


__all__ = [
    "RepeaterConfigModel",
]


class RepeaterConfigModel(BaseModel):
    tries: PositiveInt = 5
    delay: NonNegativeFloat = 1.0
    max_delay: NonNegativeFloat = 5.0
    backoff: NonNegativeFloat = 0
