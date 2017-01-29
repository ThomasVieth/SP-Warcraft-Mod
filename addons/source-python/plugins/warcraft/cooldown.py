## IMPORTS

from time import time

from .debug import log

## ALL DECLARATION

__all__ = (
    'Cooldown',
)

## COOLDOWN CLASS

class Cooldown:

    def __init__(self, duration):
        self.max_cooldown = duration
        self._end_time = time.time() + duration

        log(2, 'Creating cooldown with length ({} seconds)'.format(duration))

    @property
    def is_over(self):
        return self._end_time <= time.time()

    @property
    def remaining(self):
        r = time.time() - self._end_time
        return r if r > 0 else 0