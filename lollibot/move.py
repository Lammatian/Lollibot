#!/usr/bin/env python3
"""move.py
This module should deal with basic movement.
"""

import logging
import time

import ev3dev.ev3 as ev3
import config
from .util import *


motors = [ ev3.LargeMotor(name)
            for name in config.motor_ports ]

for m in motors:
    if not m.connected:
        logging.warning('Motor {} is not connected'
            .format(m))
        bail_if_not_debug('A motor was not connected')

# all the motors are connected


def move(distance: float) -> None:
    """Move the robot distance metres along a straight line
    Note that distance can be negative to go backwards
    """

    reverse = distance < 0
    speed = -config.speed if reverse else config.speed
    time = config.seconds_per_metre * abs(distance)
    for m in motors:
        m.run_timed(speed_sp=speed, time_sp=time)


def stop() -> None:
    """Stops the robot"""

    for m in motors:
        m.stop()

# move(1)
# while True:
#     x = input('how far? ')
#     if x == 's':
#         stop()
#         continue
#     if x == 'q':
#         exit()
#     x = float(x)
#     move(x)