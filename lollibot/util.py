# some utility functions

import logging

import config

def bail_if_not_debug(message: str = '') -> None:
    """Crash with a user provided message if we
    are not in debug mode."""

    if not config.DEBUG:
        exit(message)

    logging.warning(message)