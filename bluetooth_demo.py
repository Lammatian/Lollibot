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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

BATTERY_PATH = "/sys/devices/platform/legoev3-battery/power_supply/legoev3-battery/voltage_now"
UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
DIRECTION = 0.25
scheduler = Scheduler()

try:
    mc = movement_control.MovementControl()
except:
    mc = None

bc = BluetoothCommunicator(UUID, logger)
bc.connect()


def bluetooth_listener(threadName, delay):
    while True:
        sleep(delay)

        data = bc.receive_data()

        parsed_data = parse_data(data)

        if parsed_data:
            command, argument = parsed_data

            if command == "mvl":
                mc = movement_control.MovementControl()
                mc.move_lines(int(argument))
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
    global DIRECTION
    while True:
        if scheduler.in_schedule_dt(datetime.now()):
            if mc:
                mc.move_lines(1, DIRECTION)
                DIRECTION *= -1
            logger.info("Moving")
        else:
            logger.info("Not in schedule")
        sleep(delay)


try:
    _thread.start_new_thread(bluetooth_listener, ("Bluetooth listener", 2,))
    _thread.start_new_thread(robot_manager, ("Robot manager", 5))
except:
    print("Error: unable to start thread")

while True:
    pass
