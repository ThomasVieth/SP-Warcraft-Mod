## IMPORTS

from os.path import dirname, basename, isfile
from glob import glob

from ..debug import log

## ALL DECLARATION

__all__ = (
    'Skill',
    )

## INIT ALL SKILL MODULES

modules = glob(dirname(__file__) + '/*.py')
skills = tuple(basename(f)[:-3] for f in modules if isfile(f))

__all__ += skills

## SKILL CLASS DEFINITION

class Skill:

    '''

    Initialization of skill, containing
    only the skills level.

    '''

    def __init__(self, level=0):
        self._level = level

        log(2, 'Initialized {}.'.format(self.__class__.__name__))

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, amount):
        self._level = amount

    def give_levels(self, amount):
        if not isinstance(amount, int):
            raise TypeError('<Skill>.give_levels will only take integer values.')

        self._level += amount

    def take_levels(self, amount):
        if not isinstance(amount, int):
            raise TypeError('<Skill>.take_levels will only take integer values.')

        self._level -= amount

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
