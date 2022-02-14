__all__ = [
    "IKeyFactory",
]


class IKeyFactory:

    def __call__(self, interval_start: int, interval_length: int) -> str:
        raise NotImplementedError()
