from typing import Optional
from aiologger import Logger
from aiologger.levels import LogLevel
from ..core import ILogger


__all__ = [
    "get_logger",
]


def get_logger(name: Optional[str] = None) -> ILogger:
    return Logger.with_default_handlers(
        name=name,
        level=LogLevel.DEBUG
    )

