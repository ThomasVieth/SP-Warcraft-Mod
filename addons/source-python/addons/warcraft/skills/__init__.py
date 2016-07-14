## IMPORTS

from ..debug import log

## ALL DECLARATION

__all__ = (
    'Skill',
    )

## SKILL CLASS DEFINITION

class Skill:

    '''

    Initialization of skill, containing
    only the skills level.

    '''

    def __init__(self, level=0):
        self._level = level

        log(2, 'Initialized {}.'.format(self.__cls__.__name__))

## DECORATORS

def clientcommands(*clientcommands):
    '''

    Client command decorator, could easily
    be replaced with a event on the
    virtual function (run_command).

    '''

    def decorator(method):
        method._clientcommands = clientcommands
        return method
    return decorator

def events(*events):
    '''

    Event decorator used for managing
    methods inside skills, and allowing
    us to establish which should be
    called and when.

    '''

    def decorator(method):
        method._events = events
        return method
    return decorator