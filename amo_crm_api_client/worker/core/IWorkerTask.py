__all__ = [
    "IWorkerTask"
]


class IWorkerTask:

    async def execute(self) -> None:
        raise NotImplementedError()
