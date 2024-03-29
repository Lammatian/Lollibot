import pytest
from lollibot.movement.line_counter import LineCounter
from random import randrange


def input_measurements(lc, count, min_val, max_val):
    for _ in range(count):
        sensor_input = randrange(min_val, max_val)
        lc.register_input(sensor_input)


def test_calibrate():
    lc = LineCounter()
    input_measurements(lc, 5, 0, 25)
    assert lc.last_value() == False

    lc.calibrate(160)
    input_measurements(lc, 5, 80, 150)
    assert lc.last_value() == True


def test_smooth():
    lc = LineCounter()
    lc.calibrate(600)

    input_measurements(lc, 8, 30, 50)
    assert lc.last_value() == False

    input_measurements(lc, 1, 350, 400)
    assert lc.last_value() == False

    input_measurements(lc, 1, 60, 80)
    assert lc.last_value() == False

    assert lc.count_lines() == 0


def test_one_line():
    lc = LineCounter()
    lc.calibrate(600)

    input_measurements(lc, 8, 30, 50)  # black
    input_measurements(lc, 15, 350, 380)  # white
    input_measurements(lc, 8, 80, 100)  # black

    assert lc.count_lines() == 1


def test_two_lines():
    lc = LineCounter()
    lc.calibrate(600)

    input_measurements(lc, 8, 30, 50)  # black
    input_measurements(lc, 15, 350, 380)  # white
    input_measurements(lc, 8, 80, 100)  # black
    input_measurements(lc, 6, 390, 410)  # white

    assert lc.count_lines() == 2


def test_reset():
    lc = LineCounter()
    lc.calibrate(600)

    input_measurements(lc, 8, 30, 50)  # black
    input_measurements(lc, 15, 350, 380)  # white
    input_measurements(lc, 8, 80, 100)  # black

    assert lc.count_lines() == 1

    lc.reset()

    assert lc.count_lines() == 0

    input_measurements(lc, 8, 30, 50)  # black
    input_measurements(lc, 15, 350, 380)  # white
    input_measurements(lc, 8, 80, 100)  # black

    assert lc.count_lines() == 1


TRACE_BASE_PATH = "tests/movement/traces"


@pytest.mark.parametrize('lines', range(1, 5))
@pytest.mark.parametrize('delay', [0, 0.001, 0.002, 0.005, 0.01, 0.015, 0.02])
@pytest.mark.parametrize('direction', ['forward', 'back'])
def test_trace(lines, delay, direction):
    lc = LineCounter()

    with open("{}/measurement-{}-{}-{}.txt".format(TRACE_BASE_PATH, lines, delay, direction), 'r') as f:
        for line in f:
            measurement = int(line)
            lc.register_input(measurement)

    assert lc.count_lines() == lines