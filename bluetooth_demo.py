from lollibot.bluetooth import BluetoothCommunicator
from lollibot.data_parser import parse_data
import lollibot.movement.movement_control as movement_control
from time import sleep

BATTERY_PATH = "/sys/devices/platform/legoev3-battery/power_supply/legoev3-battery/voltage_now"
UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
mc = movement_control.MovementControl()

bc = BluetoothCommunicator(UUID)
bc.connect()

while True:
    data = bc.receive_data()

    parsed_data = parse_data(data)

    if parsed_data:
        command, argument = parsed_data

        if command == "mvl":
            mc.move_lines(int(argument))
        elif command == "btr":
            with open(BATTERY_PATH) as f:
                voltage = f.read()

            bc.send_data(("Voltage: " + voltage).encode())
        elif command == "sts":
            continue
        elif command == "ups":
            continue
        elif command == "rms":
            continue
        elif command == "snl":
            continue
        elif command == "mtm":
            continue
        elif command == "mfm":
            continue    