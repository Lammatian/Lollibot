import pytest
import importlib

from datetime import date, time

import lollibot.scheduling as scheduling

@pytest.fixture
def common_mock(mocker, tmpdir):
    local_conf_path = str(tmpdir.join('lollibot.cfg'))
    config = importlib.import_module("lollibot.config")
    mocker.patch.object(config, 'USER_CONFIG_LOCATION', local_conf_path)
    return config.config

def test_empty(common_mock):
    scheduler = scheduling.Scheduler()

    test_date = date(2018, 2, 28)

    assert scheduler.get_schedule(test_date) == []

def test_store(common_mock):
    scheduler = scheduling.Scheduler()

    test_date = date(2018, 2, 28)
    test_schedule = ["10:00:00-11:00:00", "12:00:00-12:30:30"]

    scheduler.set_schedule(test_date, test_schedule)

    assert scheduler.get_schedule(test_date) == test_schedule


def test_in_time(common_mock):
    scheduler = scheduling.Scheduler()

    test_date = date(2018, 2, 28)
    test_schedule = ["10:00:00-11:00:00", "12:00:00-12:30:30"]

    scheduler.set_schedule(test_date, test_schedule)

    test_time = time(10, 35, 11)

    assert scheduler.in_schedule(test_date, test_time)


def test_not_in_time(common_mock):
    scheduler = scheduling.Scheduler()

    test_date = date(2018, 2, 28)
    test_schedule = ["10:00:00-11:00:00", "12:00:00-12:30:30"]

    scheduler.set_schedule(test_date, test_schedule)

    test_time = time(11, 35, 11)

    assert not scheduler.in_schedule(test_date, test_time)


def test_override(common_mock):
    scheduler = scheduling.Scheduler()

    test_date = date(2018, 2, 28)
    test_schedule = ["10:00:00-11:00:00", "12:00:00-12:30:30"]
    test_schedule_2 = ["15:00:00-17:00:00"]

    scheduler.set_schedule(test_date, test_schedule)

    test_time = time(10, 35, 11)

    assert scheduler.in_schedule(test_date, test_time)

    scheduler.set_schedule(test_date, test_schedule_2)

    assert scheduler.get_schedule(test_date) == test_schedule_2
    assert not scheduler.in_schedule(test_date, test_time)


def test_delete(common_mock):
    scheduler = scheduling.Scheduler()

    test_date = date(2018, 2, 28)
    test_schedule = ["10:00:00-11:00:00", "12:00:00-12:30:30"]

    scheduler.set_schedule(test_date, test_schedule)

    test_time = time(10, 35, 11)

    assert scheduler.in_schedule(test_date, test_time)

    scheduler.delete_schedule(test_date)

    assert scheduler.get_schedule(test_date) == []
    assert not scheduler.in_schedule(test_date, test_time)