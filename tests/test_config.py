import pytest
import importlib
import unittest.mock as mock


@pytest.fixture
def common_mock(mocker, tmpdir):
    local_conf_path = str(tmpdir.join('lollibot.cfg'))
    config = importlib.import_module("lollibot.config")
    mocker.patch.object(config, 'USER_CONFIG_LOCATION', local_conf_path)
    return config.config


def test_load_defaults(common_mock):
    assert common_mock.DEBUG is not None


def test_stickiness(common_mock):
    common_mock.new_value = '123'

    assert common_mock.new_value == '123'


def test_overwrite(common_mock):
    common_mock.something = '123'

    common_mock.something = 'abc'

    assert common_mock.something == 'abc'


def test_case_insensitive(common_mock):
    common_mock.SOMETHING = '123'

    assert common_mock.something == '123'
    assert common_mock.SOMEthing == '123'
    assert common_mock.SOMETHING == '123'


def test_store_lists(common_mock):
    array = ['hello', 'world everybody!']
    common_mock.array = array

    assert common_mock.array == array


def test_store_integer(common_mock):
    common_mock.number = 420

    assert common_mock.number == 420


def test_store_float(common_mock):
    common_mock.number = 42.25

    assert common_mock.number == 42.25
