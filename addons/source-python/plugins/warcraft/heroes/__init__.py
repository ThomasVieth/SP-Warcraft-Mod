## IMPORTS

from collections import defaultdict
from os.path import dirname, basename, isfile
from glob import glob

from ..debug import log

## ALL DECLARATION

__all__ = (
    'Hero',
    )

## INIT ALL HERO MODULES

modules = glob(dirname(__file__) + '/*.py')
heroes = tuple(basename(f)[:-3] for f in modules if isfile(f))

__all__ += heroes

## RACE CLASS DEFINITION

class Hero:

    _skills = list()

    requirement = 'None'

    '''

    Initialization of heroes, which builds
    all skills, and dictionaries required.

    '''

    def __init__(self, experience=0, level=0):
        self._experience = experience
        self._level = level
        self._clientcommands = defaultdict(set)
        self._events = defaultdict(set)

        self.skills = set()

        for _skill in self._skills:
            skill = _skill()

            self.skills.add(skill)

            for attr in dir(skill):
                method = getattr(skill, attr)

                if not callable(method):
                    continue

                if hasattr(method, '_events'):
                    for event in method._events:
                        self._events[event].add(method)

                if hasattr(method, '_clientcommands'):
                    for clientcommand in method._clientcommands:
                        self._clientcommands[clientcommand].add(method)


        log(2, 'Initialized {}.'.format(self.__class__.__name__))

    @property
    def clientcommands(self):
        return self._clientcommands

    @property
    def events(self):
        return self._events

    # Management of current hero,
    # experience and levels. Added access
    # to give and take levels/experience.

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, amount):
        self._experience = amount

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, amount):
        self._level = amount

    def unused_points(self, level):
        return self._level - sum(skill.level for skill in self.skills)

    def required_experience(self, level):
        return 80 + (40 * self._level)

    def give_experience(self, amount):
        if not isinstance(amount, int):
            raise TypeError('<Hero>.give_experience will only take integer values.')

        self._experience += amount
        while self._experience >= self.required_experience(self._level):
            self._experience -= self.required_experience(self._level)
            self._level += 1

    def take_experience(self, amount):
        if not isinstance(amount, int):
            raise TypeError('<Hero>.take_experience will only take integer values.')

        self._experience -= amount
        while self._experience < 0:
            self._level -= 1
            self._experience += self.required_experience(self._level)

    def give_levels(self, amount):
        if not isinstance(amount, int):
            raise TypeError('<Hero>.give_levels will only take integer values.')

        self._level += amount

    def take_levels(self, amount):
        if not isinstance(amount, int):
            raise TypeError('<Hero>.take_levels will only take integer values.')

        self._level -= amount

    # Methods used for external calling of
    # skill methods.

    def call_events(self, event_name, *args, **kwargs):
        if not event_name in self._events:
            return
        for method in self._events[event_name]:
            method(*args, **kwargs)

    def call_clientcommands(self, clientcommand, *args, **kwargs):
        if not clientcommand in self._clientcommands:
            return
        for method in self._clientcommands[clientcommand]:
            method(*args, **kwargs)

    # Decorators for embedding skills into
    # heroes.

    @classmethod
    def skill(cls, skill):
        cls._skills.append(skill)

        log(2, 'Embedded skill {} into {}.'.format(skill.__name__,
            cls.__name__))

        return skill

    # Form dictionaries of all subclassed
    # heroes.

    @classmethod
    def get_subclasses(cls):
        for subcls in cls.__subclasses__():
            yield subcls
            yield from subcls.get_subclasses()

    @classmethod
    def get_subclass_dict(cls):
        return {subcls.__name__: subcls for subcls in cls.get_subclasses()}

    @classmethod
    def meets_requirements(self, player):
        return True