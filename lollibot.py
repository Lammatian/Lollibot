#! /usr/bin/env python3
import lollibot.bluetooth_comms as bluetooth
from lollibot.data_parser import parse_data, parse_timedate, encode_data, encode_dates, parse_date
import lollibot.scheduling as scheduling
import lollibot.movement.movement_control as movement_control
from time import sleep
import logging
import sys
from datetime import datetime
from threading import Thread
from lollibot.config import config
import lollibot.movement.stuck_exception as stuck_exception

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

BATTERY_PATH = "/sys/devices/platform/legoev3-battery/power_supply/legoev3-battery/voltage_now"
speed = config.relative_speed
should_move_road = False
stuck = False
scheduler = scheduling.Scheduler()
commands_to_send = []

bc = bluetooth.BluetoothCommunicator(config.uuid, logger)


def bluetooth_listener(delay):
    global should_move_road, commands_to_send

    while True:
        sleep(delay)
        try:
            if not bc.connected:
                bc.connect()
        except:
            continue

        while commands_to_send:
            c = commands_to_send.pop()
            bc.send_data(encode_data(c))

        data = bc.receive_data()
        parsed_data = parse_data(data)

        logger.info("Parsed data: {}".format(parsed_data))

        if parsed_data:
            command, argument = parsed_data

            logger.info("command: {}".format(command))

            if command == "mvl":
                config.middle_line_count = int(argument)
                should_move_road = True
            elif command == "btr":
                with open(BATTERY_PATH) as f:
                    voltage = f.read().strip()

                bc.send_data(encode_data("bsu", voltage))
            elif command == "sts":
                continue
            elif command == "ups":
                date, times = parse_timedate(argument)
                scheduler.set_schedule(date, times)
            elif command == "rms":
                date = parse_date(argument)
                scheduler.delete_schedule(date)
                continue
            elif command == "snl":
                continue
            elif command == "mtm":
                continue
            elif command == "mfm":
                continue
            elif command == "gts":
                logger.info("Received gts!")
                schedule = scheduler.get_all_schedules()
                bc.send_data(encode_data("scs"))
                logger.info("Sent start")
                for d, s in schedule.items():
                    encoded = encode_dates(d, s)
                    logger.info(encoded)
                    bc.send_data(encode_data("scd", encoded))

                bc.send_data(encode_data("sce"))
                logger.info("Sent end")


def robot_manager(delay):
    global speed, should_move_road, stuck, commands_to_send
    while True:
        if not stuck and scheduler.in_schedule_dt(datetime.now()):
            try:
                mc = movement_control.MovementControl()
                mc.move_lines(config.middle_line_count, speed)

                sleep(5)

                mc.move_lines(config.middle_line_count, -speed)

                sleep(5)

                logger.info("Scheduled moving")
            except stuck_exception.StuckException:
                stuck = True
                commands_to_send.append('wng')
                logger.info("Stuck on the road")
            except:
                logger.info("Not moving due to an error")

        elif should_move_road:
            logger.info("Forced moving")
            should_move_road = False
            stuck = False
            mc = movement_control.MovementControl()

            direction = config.relative_speed
            line_count = config.middle_line_count

            if line_count < 0:
                direction *= -1
                line_count *= -1

            try:
                mc.move_lines(line_count, direction)
            except stuck_exception.StuckException:
                stuck = True
                commands_to_send.append('wng')
                logger.info("Stuck on the road")
        else:
            logger.info("Not in schedule")

        sleep(delay)


try:
    bluetooth_thread = Thread(target=bluetooth_listener, name="Bluetooth listener", args=(2,))
    robot_manager_thread = Thread(target=robot_manager, name="Robot manager", args=(5,))

    bluetooth_thread.start()
    robot_manager_thread.start()

    bluetooth_thread.join()
    robot_manager_thread.join()

except Exception as e:
    print("Error: unable to start thread: {}", e)
    exit(1)