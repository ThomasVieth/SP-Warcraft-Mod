## IMPORTS

from ..heroes.undead import Undead
from . import Skill
from . import events

@Undead.skill
class Unholy(Skill):
    name = 'Unholy Aura'

    @events('player_spawn')
    def _on_spawn(self, player):
        player.speed += 0.4