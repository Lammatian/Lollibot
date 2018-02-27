import re
from datetime import datetime

command_pattern = re.compile(r"^\[(...)(\*(.*)\*)?\]$")
date_pattern = re.compile(r"^<(../../....)\|(\|(.*:.*-.*:.*))*>$")


def is_data_valid(data):
    return re.match(command_pattern, data) and data[1:4] in commands


def parse_data(data):
    if not is_data_valid(data):
        return None
    
    command, argument = re.match(command_pattern, data).group(1), re.match(command_pattern, data).group(3)

    if not (commands[command] ^ argument):
        return None

    return command, argument


def parse_timedate(timedate):
    if not re.match(date_pattern, timedate):
        return

    date, times = re.match(date_pattern, timedate).group(1), re.match(date_pattern, timedate).group(3)
    times = times.split("|")
    date = datetime.strptime(date, "%d/%m/%Y")

    return date, times


commands = {
    "mvl": True
    "btr": False
    "sts": False
    "ups": True
    "rms": True
    "snl": True
    "mtm": False
    "mfm": False
}