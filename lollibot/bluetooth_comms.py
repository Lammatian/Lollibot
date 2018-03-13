#! /usr/bin/env python3
# pylint: skip-file
import bluetooth as bt
import logging
from lollibot.config import config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

handler = logging.FileHandler("bluetooth.log")
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


class BluetoothCommunicator:

    def __init__(self, uuid, log=None):
        self.logger = log or logging.getLogger(__name__)
        self.uuid = uuid

        logger.info("Setting up bluetooth socket")

        self.server_sock = bt.BluetoothSocket(bt.RFCOMM)
        self.server_sock.bind(("", bt.PORT_ANY))
        self.server_sock.listen(1)
        self.client_sock = None
        self.client_info = None

        self.port = self.server_sock.getsockname()[1]
        self.connected = False

        bt.advertise_service(self.server_sock,
                             "LollibotAppCommunicator",
                             service_id=self.uuid,
                             service_classes=[self.uuid, bt.SERIAL_PORT_CLASS],
                             profiles=[bt.SERIAL_PORT_PROFILE])

        logger.info("Socket set up")

    def connect(self):
        logger.info("Advertising service")

        logger.info("Waiting for connection on RGCOMM port {}...".format(self.port))

        self.client_sock, self.client_info = self.server_sock.accept()
        self.connected = True
        self.client_sock.settimeout(config.socket_timeout)
        self.server_sock.settimeout(config.socket_timeout)

        logger.info("Accepted connection from {}".format(self.client_info))

    def disconnect(self):
        logger.info("Disconnecting...")
        self.client_sock.close()
        self.server_sock.close()
        self.connected = False
        logger.info("Disconnected")

    def receive_data(self):
        logger.info("Receiving data")
        try:
            data = self.client_sock.recv(1024)

            if not data:
                logger.debug("No data found")
                return None

            decoded_data = data.decode("utf-8")
            logger.debug("Received {}".format(decoded_data))

            return decoded_data
        except TimeoutError as e:
            logger.info("Receive timed out: {}".format(e))
            return None
        except IOError as e:
            logger.info("Device disconnected: {}".format(e))
            self.connected = False
            return None

    def send_data(self, data):
        logger.debug("Sending {} to the client".format(data))
        try:
            self.client_sock.send(data.encode())
            logger.info("Data successfully sent")
        except TimeoutError as e:
            logger.info("Send timed out: {}".format(e))
            return None
        except IOError as e:
            logger.info("Device disconnected: {}".format(e))
            self.connected = False
