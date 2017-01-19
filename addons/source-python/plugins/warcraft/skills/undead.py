## IMPORTS

from ..heroes.undead import Undead
from . import Skill
from . import events

from random import randint

@Undead.skill
class Unholy(Skill):
    name = 'Unholy Aura'
    max_level = 8

    @events('player_spawn')
    def _on_spawn(self, player):
        player.speed += 0.06 * self.level

@Undead.skill
class Levitation(Skill):
    name = 'Levitation'
    max_level = 8

    @events('player_spawn')
    def _on_spawn(self, player):
        player.gravity = 1 - (0.08 * self.level)

    @events('player_death')
    def _on_death(self, player, **kwargs):
        player.gravity = 1.0

@Undead.skill
class Vampiric(Skill):
    name = 'Vampiric Aura'
    max_level = 8

    divisor = 1.5

    @events('player_pre_attack')
    def _on_pre_attack(self, player, take_damage_info, **kwargs):
        if randint(0, 100) > 35:
            return

        health_to_leech = round(take_damage_info.damage / self.divisor)
        player.health += health_to_leech
