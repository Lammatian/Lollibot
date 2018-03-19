import sys
import os
import argparse
import re
import json
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from lollibot.config import config

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for p in config.find_all(re.compile('.*')):
        parser.add_argument("--{}".format(p), dest=p, type=json.loads, help="Default: {}".format(json.dumps(config.get(p))))

    args = vars(parser.parse_args())
    for k, v in args.items():
        if v is not None:
            print("{}={}".format(k, v))
            config.set(k, v)

