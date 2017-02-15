## TEST HERO

from . import Hero
from . import Skill
from . import events
from . import clientcommands
from .extensions import LifestealSkill, GravitySkill
from ..cooldown import Cooldown

class Undead(Hero):
    name = 'Undead Scourge'

@Undead.skill
class Unholy(Skill):
    name = 'Unholy Aura'
    max_level = 8

    @events('player_spawn')
    def _on_spawn(self, player, **kwargs):
        player.speed += 0.06 * self.level

    @events('player_spawn')
    def _reset_cooldowns(self, **kwargs):
        self.cooldown = Cooldown(3)

    @clientcommands('speed')
    def _on_command(self, player, command, **kwargs):
        if self.cooldown.is_over:
            player.speed += 0.1
            self.cooldown = Cooldown(20)

@Undead.skill
class Levitation(GravitySkill):
    name = 'Levitation'

@Undead.skill
class Vampiric(LifestealSkill):
    name = 'Vampiric Aura'