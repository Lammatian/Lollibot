import pytest
import lollibot.data_parser as dp
from datetime import date, time


def test_encode_date():
    encoded = dp.encode_dates(date(2018, 1, 1), ["14:40:31-15:17:30"])
    assert encoded == "<01/01/2018||14:40:31-15:17:30>"


def test_encode_dates():
    encoded = dp.encode_dates(date(2018, 1, 30), ["14:40:31-15:17:30", "15:40:31-17:17:30"])
    expected = "<30/01/2018||14:40:31-15:17:30|15:40:31-17:17:30>"
    assert encoded == expected


def test_encode_data():
    encoded = dp.encode_data("sts", "123")
    expected = "[sts*123*]"
    assert encoded == expected


def test_encode_data_no_params():
    encoded = dp.encode_data("sts")
    expected = "[sts]"
    assert encoded == expected


def test_encode_dates():
    encoded_date = dp.encode_dates(date(2018, 1, 30), ["14:40:31-15:17:30", "15:40:31-17:17:30"])
    encoded = dp.encode_data("scd", encoded_date)
    expected = "[scd*<30/01/2018||14:40:31-15:17:30|15:40:31-17:17:30>*]"
    assert encoded == expected