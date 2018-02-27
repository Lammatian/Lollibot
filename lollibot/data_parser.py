import re
from datetime import datetime
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

handler = logging.FileHandler("bluetooth.log")
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


command_pattern = re.compile(r"^\[(...)(\*(.*)\*)?\]$")
date_pattern = re.compile(r"^<(../../....)\|(\|(.*:.*-.*:.*))*>$")


def is_data_valid(data):
    logger.debug("Checking validity of {}".format(data))
    return re.match(command_pattern, data) and data[1:4] in commands


def parse_data(data):
    logger.debug("Parsing {}".format(data))

    if not is_data_valid(data):
        return None
    
    logger.debug("Data is valid")
    command, argument = re.match(command_pattern, data).group(1), re.match(command_pattern, data).group(3)

    if commands[command] ^ bool(argument):
        return None

    logger.debug("Arguments match the command")

    return command, argument


def parse_timedate(timedate):
    logging.debug("Parsing timedate {}".format(timedate))

    if not re.match(date_pattern, timedate):
        return

    logging.debug("Timedate matches the pattern")

    date, times = re.match(date_pattern, timedate).group(1), re.match(date_pattern, timedate).group(3)
    times = times.split("|")
    date = datetime.strptime(date, "%d/%m/%Y").date()
    logging.debug("Finished parsing datetime: {}, {}".format(date, times))

    return date, times


commands = {
    "mvl": True,
    "btr": False,
    "sts": False,
    "ups": True,
    "rms": True,
    "snl": True,
    "mtm": False,
    "mfm": False
}
