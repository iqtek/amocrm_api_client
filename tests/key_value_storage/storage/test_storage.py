import asyncio
import pytest


@pytest.mark.asyncio
async def test_set_value1(ready_storage):
    await ready_storage.set("key", "value")
    result = await ready_storage.get("key")
    assert result == "value"


@pytest.mark.asyncio
async def test_set_value1(ready_storage):
    await ready_storage.set("key", 666)
    result = await ready_storage.get("key")
    assert result == 666


@pytest.mark.asyncio
async def test_set_value2(ready_storage):
    await ready_storage.set("key2", "value2", expire=1)
    result = await ready_storage.get("key2")
    assert result == "value2"


@pytest.mark.asyncio
async def test_set_value3(ready_storage):
    await ready_storage.set("key3", "value3", expire=1)
    await asyncio.sleep(1)
    with pytest.raises(LookupError):
        result = await memory_storage.get("key3")