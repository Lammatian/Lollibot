import re
from datetime import datetime, date, time

command_pattern = re.compile(r"^\[(...)(\*(.*)\*)?\]$")
date_pattern = re.compile(r"^<(../../....)\|(\|(.*:.*-.*:.*))*>$")


def is_data_valid(data):
    if not data:
        return False

    return re.match(command_pattern, data) and data[1:4] in commands


def parse_data(data):

    if not is_data_valid(data):
        return None

    command, argument = re.match(command_pattern, data).group(1), re.match(command_pattern, data).group(3)

    if commands[command] ^ bool(argument):
        return None

    return command, argument


def parse_date(data):
    return datetime.strptime(data, "%d/%m/%Y").date()


def encode_data(command, data=None):
    if data:
        return "[{}*{}*]".format(command, data)
    else:
        return "[{}]".format(command)


def encode_dates(date: date, times):
    return "<{}||{}>".format(date.strftime("%d/%m/%Y"), "|".join(times))


def parse_timedate(timedate):
    if not re.match(date_pattern, timedate):
        return

    date_str, times = re.match(date_pattern, timedate).group(1), re.match(date_pattern, timedate).group(3)
    times = times.split("|")
    date = parse_date(date_str)

    return date, times


commands = {
    "mvl": True,
    "btr": False,
    "sts": False,
    "ups": True,
    "rms": True,
    "snl": True,
    "mtm": False,
    "mfm": False,
    "gts": False,
    "scs": False,
    "sce": False,
    "scd": True
}
