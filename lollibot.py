#!/usr/bin/env python3

import lollibot.movement.movement_control as movement_control
from time import sleep

if __name__ == '__main__':
    mc = movement_control.MovementControl()
    mc.move_lines(4)

    sleep(5)

    mc.move_lines(4, -1)
