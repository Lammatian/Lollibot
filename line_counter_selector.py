#! /usr/bin/env python3
from lollibot.bluetooth_comms import BluetoothCommunicator
from lollibot.data_parser import parse_data, parse_timedate
from lollibot.scheduling import Scheduler
import lollibot.movement.movement_control as movement_control
from time import sleep
import logging
import sys
from datetime import datetime
import _thread

from lollibot.config import config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

BATTERY_PATH = "/sys/devices/platform/legoev3-battery/power_supply/legoev3-battery/voltage_now"
UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
scheduler = Scheduler()

try:
    mc = movement_control.MovementControl()
except:
    pass

bc = BluetoothCommunicator(UUID, logger)
bc.connect()

should_move_road = False


def bluetooth_listener(threadName, delay):
    global should_move_road
    while True:
        sleep(delay)

        data = bc.receive_data()

        parsed_data = parse_data(data)

        if parsed_data:
            command, argument = parsed_data

            if command == "mvl":
                config.middle_line_count = int(argument)
                should_move_road = True
            elif command == "btr":
                with open(BATTERY_PATH) as f:
                    voltage = f.read()

                bc.send_data(("Voltage: " + voltage).encode())
            elif command == "sts":
                continue
            elif command == "ups":
                date, times = parse_timedate(argument)
                scheduler.set_schedule(date, times)
            elif command == "rms":
                continue
            elif command == "snl":
                continue
            elif command == "mtm":
                continue
            elif command == "mfm":
                continue


def robot_manager(threadName, delay):
    global should_move_road

    while True:
        if should_move_road:
            should_move_road = False
            mc = movement_control.MovementControl()
            direction = 1
            line_count = config.middle_line_count

            if line_count < 0:
                direction *= -1
                line_count *= -1

            mc.move_lines(line_count, direction*0.15)


try:
    _thread.start_new_thread(bluetooth_listener, ("Bluetooth listener", 2,))
    _thread.start_new_thread(robot_manager, ("Robot manager", 5))
except:
    print("Error: unable to start thread")

while True:
    pass

