from typing import (
    Callable,
)


__all__ = [
    "get_time_mock",
]


def get_time_mock(time_step: float) -> Callable[[], float]:
    """
    With each call, the function returns a value
    that differs from the previous one by a time_step.
    :param time_step: time_delta
    :return: simulated time change
    """
    curr_time: float = 0

    def get_time() -> float:
        nonlocal curr_time
        curr_time += time_step
        return curr_time

    return get_time
