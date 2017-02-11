## IMPORTS

from listeners import ListenerManager
from listeners import ListenerManagerDecorator

## ALL DECLARATION

__all__ = (
    'HeroLevelChange',
    )

##

class HeroLevelChange(ListenerManagerDecorator):
    manager = ListenerManager()