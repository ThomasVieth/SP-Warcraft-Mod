## IMPORTS

from . import Skill
from . import events
from . import clientcommands

from random import randint

## 

class LifestealSkill(Skill):
	max_level = 8

	@property
	def percentage(self):
		'The percentage of the damage that will heal you.'
		return 10 * self.level

	@property
	def chance(self):
		'The chance in which when dealing damage, you will be healed.'
		return 4 * self.level

	@events('player_pre_attack')
    def _on_pre_attack(self, player, take_damage_info, **kwargs):
    	'Called upon the <on_take_damage> function happening.'
        if randint(0, 100) > self.chance:
            return

        health_to_leech = round(take_damage_info.damage * (self.percentage/100))
        player.health += health_to_leech