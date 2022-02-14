import time
import pytest
from amo_crm_api_client.storage.impl.instances.memory.impl.expiring_value import (
    ExpiringValue,
)
from ..get_time_mock import (
    get_time_mock,
)


@pytest.fixture()
def get_time_function():
    return get_time_mock(time_step=1.0)


def test_create_no_expiring_value():
    exp_value = ExpiringValue(
        value="str_value",
    )
    assert not exp_value.is_expired()


def test_expiring_value(get_time_function):
    exp_value = ExpiringValue(
        value="str_value",
        expire=1.0,
        get_time_function=get_time_function,
    )
    assert not exp_value.is_expired()
    get_time_function()
    assert exp_value.is_expired()


def test_get_fresh_value():
    exp_value = ExpiringValue(
        value="str_value",
    )
    assert exp_value.get_value() == "str_value"


def test_get_not_fresh_value(get_time_function):
    exp_value = ExpiringValue(
        value="str_value",
        expire=1.0,
        get_time_function=get_time_function,
    )
    get_time_function()
    with pytest.raises(Exception):
        exp_value.get_value()
