#! /usr/bin/env python3
from bluetooth import *
import ev3dev.ev3 as ev3

# TODO:
# Tests
# Documentation

mA = ev3.LargeMotor('outA')
mC = ev3.LargeMotor('outC')
UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
BATTERY_PATH = "/sys/devices/platform/legoev3-battery/power_supply/legoev3-battery/voltage_now"


def connect(uuid):
    server_sock = BluetoothSocket(RFCOMM)
    server_sock.bind(("", PORT_ANY))
    server_sock.listen(1)
    
    port = server_sock.getsockname()[1]

    advertise_service(server_sock, 
        "SampleServer",
        service_id = uuid,
        service_classes = [uuid, SERIAL_PORT_CLASS],
        profiles = [SERIAL_PORT_PROFILE])
                       
    print("Waiting for connection on RFCOMM channel %d" % port)

    client_sock, client_info = server_sock.accept()

    print("Accepted connection from ", client_info)

    return client_sock


def communicate():
    global mA, mC
    try:
        while True:
            data = client_sock.recv(1024)
            client_sock.send(data)

            if len(data) == 0: 
                break

            data = data.decode("utf-8")

            print("received [%s]" % data)

            if data == "moveBack":
                print("Moving back")
                mA.run_timed(time_sp=9000, speed_sp=-250)
                mC.run_timed(time_sp=9000, speed_sp=-250)
            elif data == "moveForward":
                print("Moving forward")
                mA.run_timed(time_sp=9000, speed_sp=250)
                mC.run_timed(time_sp=9000, speed_sp=250)
            elif data == "stop":
                print("Stopping...")
                mC.stop(stop_action='hold')
                mA.stop(stop_action='hold')
                print("Stopped.")
            elif data == "giveBattery":
                print("Sending battery data...")

                with open(battery_path, 'r') as f:
                    content = f.read()

                client_sock.send(("Voltage: " + content).encode())

                print("Data successfully sent.")
            elif data == "dc":
                print("Disconnecting...")
                disconnect()
    except IOError:
        pass


def disconnect():
    client_sock.close()
    server_sock.close()
    print("Disconnected.")


def main():
    connect(UUID)
    communicate()


if __name__ == "__main__":
    main()