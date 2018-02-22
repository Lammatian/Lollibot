#!/usr/bin/env python3

import lollibot.movement.movement_control as movement_control

if __name__ == '__main__':
    mc = movement_control.MovementControl()
    mc.move_lines(3)