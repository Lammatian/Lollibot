# some utility functions

import logging
import os
import sys

import config

def bail_if_not_debug(message: str = '') -> None:
    """Crash with a user provided message if we
    are not in debug mode."""

    if not config.DEBUG:
        exit(message)

    logging.warning(message)


def app_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
