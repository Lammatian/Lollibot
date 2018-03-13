#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import lollibot.movement.movement_control as movement_control
from lollibot.config import config
from time import sleep

if __name__ == '__main__':
    config.debug = True

    for lines in [4]:
        for delay in [0, 0.001, 0.002, 0.005, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.0225]:
            config.measurement_delay = delay
            config.dump_measurements = True

            mc = movement_control.MovementControl()
            mc.move_lines(lines, 0.25)

            with open("/tmp/measurement-{}-{}-forward.txt".format(lines, delay), 'w') as f:
                measurement_str = "\n".join([str(i) for i in mc.raw_measurements])
                f.write(measurement_str)

            mc.raw_measurements = []

            sleep(2)

            mc.move_lines(lines, -0.25)

            with open("/tmp/measurement-{}-{}-back.txt".format(lines, delay), 'w') as f:
                measurement_str = "\n".join([str(i) for i in mc.raw_measurements])
                f.write(measurement_str)

            sleep(2)
