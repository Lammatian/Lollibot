#!/usr/bin/env python3

import lollibot.movement.movement_control as movement_control
from time import sleep
from ev3dev.ev3 import Sound

if __name__ == '__main__':
    laps = 1
    while True:
        print("Lap {}".format(laps))

        mc = movement_control.MovementControl()
        mc.move_lines(4, 0.25)

        sleep(1)

        mc.move_lines(4, -0.25)

        sleep(1)

        laps += 1

