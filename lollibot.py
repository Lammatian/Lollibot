#!/usr/bin/env python3

import lollibot.movement.movement_control as movement_control
import lollibot.scheduling as scheduling

from time import sleep
from datetime import datetime

if __name__ == '__main__':

    scheduler = scheduling.Scheduler()
    scheduler.set_schedule(datetime.now().date(), ["00:00:00-23:59:59"])

    while True:
        cur_datetime = datetime.now()

        if True:
            mc = movement_control.MovementControl()
            mc.move_lines(4, 0.25)

            sleep(5)

            mc.move_lines(4, -0.25)

        sleep(5)
