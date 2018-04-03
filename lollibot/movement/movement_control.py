import lollibot.movement.line_counter as line_counter
import lollibot.ev3.line_color_sensor as line_color_sensor
import lollibot.ev3.main_motors as main_motors
import time
from datetime import datetime
import lollibot.movement.stuck_exception as stuck_exception

from lollibot.config import config


class MovementControl(object):

    def __init__(self):
        self.lc = line_counter.LineCounter()
        self.color_sensor = line_color_sensor.LineColorSensor()
        self.main_motors = main_motors.MainMotors()
        self.raw_measurements = []  # Used for debugging
        self.start_time = None

    def move_lines(self, line_count, direction=1):
        self.lc.reset()
        start_time = datetime.now()
        old_value = False

        print("Moving {} lines at {} speed".format(line_count, direction))

        sensor_value = self.color_sensor.value()
        self.lc.register_input(sensor_value)

        while self.lc.count_lines() < line_count:
            self.main_motors.move(direction)
            time.sleep(config.measurement_delay)
            sensor_value = self.color_sensor.value()
            self.lc.register_input(sensor_value)

            current_time = datetime.now()
            new_value = self.lc.threshold(sensor_value)
            if old_value != new_value:
                start_time = current_time
                old_value = new_value

            if (current_time - start_time).total_seconds() > config.time_per_line and config.detect_stuck:
                self.main_motors.stop()
                raise stuck_exception.StuckException()

            if config.DEBUG:
                print("Sensor value: {}, lines: {}".format(sensor_value, self.lc.count_lines()))

            if config.dump_measurements:
                self.raw_measurements.append(sensor_value)

        self.main_motors.stop()
