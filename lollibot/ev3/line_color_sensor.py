from ev3dev.ev3 import *
from config import *


class LineColorSensor(object):

    def __init__(self):
        self.ev3_color_sensor = ColorSensor(color_sensor_port)
        self.ev3_color_sensor.mode = 'COL-REFLECT'

    def value(self):
        return self.ev3_color_sensor.value()
