import lollibot.movement.line_counter as line_counter
import lollibot.ev3.line_color_sensor as line_color_sensor
import lollibot.ev3.main_motors as main_motors
import time

from lollibot.config import config


class MovementControl(object):

    def __init__(self):
        self.lc = line_counter.LineCounter()
        self.color_sensor = line_color_sensor.LineColorSensor()
        self.main_motors = main_motors.MainMotors()

    def move_lines(self, line_count, direction=1):
        self.lc.reset()

        print("Moving {} lines at {} speed".format(line_count, direction))

        sensor_value = self.color_sensor.value()
        self.lc.register_input(sensor_value)

        while self.lc.count_lines() < line_count:
            self.main_motors.move(direction)
            time.sleep(0)
            sensor_value = self.color_sensor.value()
            self.lc.register_input(sensor_value)
            if config.DEBUG:
                print("Sensor value: {}, lines: {}".format(sensor_value, self.lc.count_lines()))

        self.main_motors.stop()
