import pytest
from lollibot.line_counter import LineCounter
from random import randrange


def input_measurements(lc, count, min_val, max_val):
    for _ in range(count):
        input = tuple([randrange(min_val, max_val) for _ in range(3)])
        lc.input(input)


def test_calibrate():
    lc = LineCounter()
    input_measurements(lc, 5, 0, 25)
    assert lc.last_value() == False

    lc.calibrate((150, 170, 130))
    input_measurements(lc, 5, 80, 150)
    assert lc.last_value() == True


def test_smooth():
    lc = LineCounter()
    lc.calibrate((600, 600, 600))

    input_measurements(lc, 8, 30, 50)
    assert lc.last_value() == False

    input_measurements(lc, 2, 350, 400)
    assert lc.last_value() == False

    input_measurements(lc, 1, 60, 80)
    assert lc.last_value() == False

    assert lc.count_lines() == 0


def test_one_line():
    lc = LineCounter()
    lc.calibrate((600, 600, 600))

    input_measurements(lc, 8, 30, 50) # black
    input_measurements(lc, 15, 350, 380) # white
    input_measurements(lc, 8, 80, 100) # black

    assert lc.count_lines() == 1


def test_two_lines():
    lc = LineCounter()
    lc.calibrate((600, 600, 600))

    input_measurements(lc, 8, 30, 50)  # black
    input_measurements(lc, 15, 350, 380)  # white
    input_measurements(lc, 8, 80, 100)  # black
    input_measurements(lc, 6, 390, 410)  # white

    assert lc.count_lines() == 2


