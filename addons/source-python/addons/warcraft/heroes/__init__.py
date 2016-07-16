## IMPORTS

from collections import defaultdict

from ..debug import log

## ALL DECLARATION

__all__ = (
    'Hero',
    )

## RACE CLASS DEFINITION

class Hero:

    _skills = set()

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

    '''

    Management of current hero,
    experience and levels. Added access
    to give and take levels/experience.

    '''

    @property
    def experience(self):
        return self._experience

    @property
    def level(self):
        return self._level

    def unused_points(self, level):
        return self._level - sum(skill._level for skill in self.skills)

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

    '''

    Methods used for external calling of
    skill methods.

    '''

    def call_events(self, event_name, *args, **kwargs):
        for method in self._events[event_name]:
            method(*args, **kwargs)

    def call_clientcommands(self, clientcommand, *args, **kwargs):
        for method in self._clientcommands[clientcommand]:
            method(*args, **kwargs)

    '''

    Decorators for embedding skills into
    heroes.

    '''

    @classmethod
    def skill(self, skill):
        self._skills.add(skill)

        log(2, 'Embeded skill {} into {}.'.format(skill.__name__,
            self.__class__.__name__))

        return skill

    '''

    Form dictionaries of all subclassed
    heroes.

    '''

    @classmethod
    def get_subclasses(cls):
        for subcls in cls.__subclasses__():
            yield subcls
            yield from subcls.subclasses

    @classmethod
    def get_subclass_dict(cls):
        return {subcls.__class__.__name__: subcls for subcls in cls.get_subclasses()}