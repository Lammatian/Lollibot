import re

command_pattern = re.compile(r"^\[(...)(\*(.*)\*)?\]$")


def is_data_valid(data):
    return re.match(command_pattern, data) and data[1:4] in commands


def parse_data(data):
    if not is_data_valid(data):
        return None
    
    command, argument = re.match(command_pattern, data).group(1), re.match(command_pattern, data).group(3)

    if not (commands[command] ^ argument):
        return None

    return command, argument


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