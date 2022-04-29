from pydantic import BaseModel
from pydantic import PositiveInt


__all__ = [
    "RateLimiterConfig",
]


class RateLimiterConfig(BaseModel):
    """
    interval_length: The length of the interval
        in which requests must fit (seconds).
    max_request_count: Maximum requests per interval.
    interval_length: Delay after exceeding the number of requests.
    """

    interval_length: PositiveInt = 1
    max_request_count: PositiveInt = 7
    forced_delay: PositiveInt = 1
