import fakeredis.aioredis
import asyncio
import pytest
from aiologger import Logger
from amo_crm_api_client.storage import (
    handle_startup
)
from amo_crm_api_client.logger.impl.instances.SilentLoggerImpl import (
    SilentLoggerImpl
)


@pytest.fixture()
async def memory_storage():
    logger = SilentLoggerImpl()
    storage_factory = handle_startup(
        settings={"type": "memory"},
        logger=logger,
    )
    memory_storage = storage_factory.get_instance(prefix="prefix")
    return memory_storage


@pytest.fixture()
async def redis_storage(monkeypatch):
    logger = SilentLoggerImpl()
    storage_factory = handle_startup(
        settings={"type": "redis"},
        logger=logger,
    )
    redis_storage = storage_factory.get_instance(prefix="prefix")
    r = fakeredis.aioredis.FakeRedis()
    print(redis_storage)
    monkeypatch.setattr(
        target=redis_storage,
        name="_RedisKeyValueStorage__connection",
        value=r,

    )
    return redis_storage


@pytest.fixture(params=[pytest.param(memory_storage), pytest.param(redis_storage)])
async def ready_storage(request):
    print(request)
    await request.initialize()
    yield request
    await request.deinitialize()
