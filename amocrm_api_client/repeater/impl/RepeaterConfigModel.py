from pydantic import BaseModel
from pydantic import NonNegativeFloat
from pydantic import PositiveInt


__all__ = [
    "RepeaterConfigModel",
]


class RepeaterConfigModel(BaseModel):
    tries: PositiveInt = 5
    delay: NonNegativeFloat = 1.0
    max_delay: NonNegativeFloat = 5.0
    backoff: NonNegativeFloat = 0
