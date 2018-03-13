import pytest
from lollibot.movement.movement_control import MovementControl
import datetime as dt

@pytest.fixture()
def standard_mock(mocker):
    patches = {}
    patches['sleep'] = mocker.patch('time.sleep')
    patches['motors'] = mocker.patch('lollibot.ev3.main_motors.MainMotors').return_value
    patches['line_counter'] = mocker.patch('lollibot.movement.line_counter.LineCounter').return_value
    patches['line_color_sensor'] = mocker.patch('lollibot.ev3.line_color_sensor.LineColorSensor').return_value
    patches['datetime'] = mocker.patch('lollibot.movement.movement_control.datetime')
    patches['datetime'].now.return_value = dt.datetime(2018, 3, 13)

    return type('', (object,), patches)()


def test_start_motors(standard_mock):
    standard_mock.line_color_sensor.value.return_value = 0
    standard_mock.line_counter.count_lines.side_effect = range(0, 5)

    mc = MovementControl()
    mc.move_lines(3, 1)

    assert standard_mock.motors.move.call_count > 0


def test_stop_motors(standard_mock):
    standard_mock.line_color_sensor.value.return_value = 0
    standard_mock.line_counter.count_lines.side_effect = range(0, 5)

    mc = MovementControl()
    mc.move_lines(3, 1)

    assert standard_mock.motors.stop.call_count > 0


def test_pass_correct_measurements(standard_mock):
    standard_mock.line_counter.count_lines.side_effect = range(0, 5)
    standard_mock.line_color_sensor.value.return_value = 50

    mc = MovementControl()
    mc.move_lines(3, 1)

    standard_mock.line_counter.register_input.assert_called_with(50)


def test_move_back(standard_mock):
    standard_mock.line_counter.count_lines.side_effect = range(0, 5)
    standard_mock.line_color_sensor.value.return_value = 50

    mc = MovementControl()
    mc.move_lines(3, 1)

    standard_mock.line_counter.register_input.assert_called_with(50)