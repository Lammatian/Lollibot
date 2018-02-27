from ev3dev.ev3 import *
from lollibot.config import config


class LineColorSensor(object):

    def __init__(self):
        self.ev3_color_sensor = ColorSensor(config.color_sensor_port)
        self.ev3_color_sensor.mode = 'COL-REFLECT'

    def value(self):
        return self.ev3_color_sensor.value()
