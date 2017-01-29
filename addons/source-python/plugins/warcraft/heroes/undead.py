## TEST HERO

from . import Hero
from . import Skill
from . import events
from . import clientcommands

from random import randint

class Undead(Hero):
    name = 'Undead Scourge'

@Undead.skill
class Unholy(Skill):
    name = 'Unholy Aura'
    max_level = 8

    @events('player_spawn')
    def _on_spawn(self, player, **kwargs):
        player.speed += 0.06 * self.level

    @clientcommands('speed')
    def _on_command(self, player, command, **kwargs):
        player.speed += 0.1

@Undead.skill
class Levitation(Skill):
    name = 'Levitation'
    max_level = 8

    @events('player_spawn')
    def _on_spawn(self, player, **kwargs):
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