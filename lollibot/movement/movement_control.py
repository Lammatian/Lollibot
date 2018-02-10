import lollibot.movement.line_counter as line_counter
import lollibot.ev3.line_color_sensor as line_color_sensor
import lollibot.ev3.main_motors as main_motors
import time


class MovementControl(object):

    def __init__(self):
        self.lc = line_counter.LineCounter()
        self.color_sensor = line_color_sensor.LineColorSensor()
        self.main_motors = main_motors.MainMotors()

    def move_lines(self, line_count, direction=1):
        self.lc.reset()

        sensor_value = self.color_sensor.get_value()
        self.lc.register_input(sensor_value)

        while self.lc.count_lines() < line_count:
            self.main_motors.move(direction)
            time.sleep(0.05)
            sensor_value = self.color_sensor.get_value()
            self.lc.register_input(sensor_value)
            print("{} {}".format(sensor_value, self.lc.count_lines()))

        self.main_motors.stop()
