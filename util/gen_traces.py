#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import lollibot.movement.movement_control as movement_control
from lollibot.config import config
from time import sleep

if __name__ == '__main__':
    config.debug = False

    for i in range(10):
        for lines in [4]:
            for delay in [0]:
                config.measurement_delay = delay
                config.dump_measurements = True

                print("Delay: {}".format(delay))

                mc = movement_control.MovementControl()
                mc.move_lines(lines, 0.06)

                with open("/tmp/measurement-{}-{}.txt".format(lines, delay), 'a') as f:
                    measurement_str = "\n".join([str(i) for i in mc.raw_measurements])
                    f.write(measurement_str)

                mc.raw_measurements = []

                sleep(2)

                mc.move_lines(lines, -0.06)

                with open("/tmp/measurement-{}-{}.txt".format(lines, delay), 'a') as f:
                    measurement_str = "\n".join([str(i) for i in mc.raw_measurements])
                    f.write(measurement_str)

                sleep(2)
