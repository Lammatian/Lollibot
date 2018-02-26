import logging
import ev3dev.ev3 as ev3
from lollibot.config import config
from lollibot.util import *

class MainMotors(object):

    def __init__(self):
        self.motors = [ev3.LargeMotor(port) for port in config.motor_ports]

        for m in self.motors:
            if not m.connected:
                logging.warning('Motor {} is not connected'
                                .format(m))
                bail_if_not_debug('A motor was not connected')

    def move(self, direction: int) -> None:
        """
        Moves the robot continuously until stopped
        """
        speed = direction * config.speed
        for m in self.motors:
            m.run_forever(speed_sp=speed)

    def move_distance(self, distance: float) -> None:
        """Move the robot distance metres along a straight line
        Note that distance can be negative to go backwards
        """

        reverse = distance < 0
        speed = -config.speed if reverse else config.speed
        time = config.seconds_per_metre * abs(distance)
        for m in self.motors:
            m.run_timed(speed_sp=speed, time_sp=time)

    def stop(self) -> None:
        """Stops the robot"""

        for m in self.motors:
            m.stop(stop_action='hold')
