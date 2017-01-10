## IMPORTS

from time import strftime

from core import echo_console

from .config import LOG_PRIORITY
from .config import LOG_LOCATION

## ALL DECLARATION

__all__ = (
    'log',
    )

## LOG FUNCTIONS

def write_to_log(text):
    with open(LOG_LOCATION, 'a+') as log_book:
        log_book.writelines('{} ({}){}'.format(text, strftime('%X'), '\n'))

def echo_to_console(text):
    echo_console("{} ({})".format(text, strftime('%X')))

## DICTIONARY DEFINITION

log_priority = {
    1: write_to_log,
    2: echo_to_console,
}

## LOG FUNCTION DEFINITION

def log(priority=0, *args):
    if priority not in log_priority:
        return

    if priority >= LOG_PRIORITY:
        return

    log_function = log_priority[priority]
    for s in args:
        log_function(s)