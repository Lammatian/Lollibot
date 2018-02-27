import configparser
import os
import json

USER_CONFIG_LOCATION = os.path.expanduser("~/.lollibot/lollibot.cfg")
DEFAULT_SECTION_HEADING = "DEFAULT"


class Config(object):

    # Share state between all instances
    config = configparser.ConfigParser()

    def __init__(self):
        self.reload()

    def reload(self):
        self.config.read([os.path.join(os.getcwd(), "config/default.cfg"), "/etc/lollibot/lollibot.cfg", USER_CONFIG_LOCATION])

    def write(self):
        os.makedirs(os.path.dirname(USER_CONFIG_LOCATION), exist_ok=True)
        with open(USER_CONFIG_LOCATION, "w") as file:
            self.config.write(file)

    def get(self, item):
        if item in self.config[DEFAULT_SECTION_HEADING]:
            return json.loads(self.config[DEFAULT_SECTION_HEADING][item])

        return None

    def set(self, key, value):
        if DEFAULT_SECTION_HEADING not in self.config:
            self.config[DEFAULT_SECTION_HEADING] = {}

        self.config[DEFAULT_SECTION_HEADING][key] = json.dumps(value)

        self.write()

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self.set(key, value)


config = Config()
