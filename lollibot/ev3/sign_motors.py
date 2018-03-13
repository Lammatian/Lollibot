import logging
import ev3dev.ev3 as ev3
from lollibot.config import config
from lollibot.util import *


class SignMotors(object):

    def __init__(self):
        self.motors = [ev3.LargeMotor(port) for port in config.sign_motor_ports]

        for m in self.motors:
            if not m.connected:
                logging.warning('Motor {} is not connected'
                                .format(m))
                bail_if_not_debug('A motor was not connected')

    def move_angle(self, angle: float, direction: float) -> None:
        """
        Move the motors a certain angle
        """

        if direction < 0:
            angle *= -1
            direction *= -1

        speed = config.speed * direction

        for m in self.motors:
            m.run_to_rel_pos(speed_sp=speed, position_sp=angle)

    def stop(self) -> None:
        """Stops the robot"""

        for m in self.motors:
            m.stop(stop_action='hold')
