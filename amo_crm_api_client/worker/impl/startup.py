from typing import (
    Optional,
)
from asyncio import (
    AbstractEventLoop,
    PriorityQueue,
)
from amo_crm_api_client.logger import (
    ILogger,
)
from amo_crm_api_client.rate_limiter import (
    IRateLimiter,
)
from amo_crm_api_client.repeater import (
    IRepeaterDecorator,
)
from ..core import (
    IWorkerExecutorComponent,
)
from .WorkerExecutorComponent import WorkerExecutorComponent


__all__ = [
    "handle_startup",
]


def handle_startup(
    queue: Optional[PriorityQueue] = None,
    event_loop: Optional[AbstractEventLoop] = None,
    rate_limiter: Optional[IRateLimiter] = None,
    repeater: Optional[IRepeaterDecorator] = None,
    logger: Optional[ILogger] = None,
) -> IWorkerExecutorComponent:
    worker = WorkerExecutorComponent(
        queue=queue,
        event_loop=event_loop,
        rate_limiter=rate_limiter,
        repeater=repeater,
        logger=logger,
    )
    return worker
