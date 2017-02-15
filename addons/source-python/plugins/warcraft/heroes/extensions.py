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

class GravitySkill(Skill):
	max_level = 8

	@property
	def percentage(self):
		'The percentage of gravity that will still affect the player.'
		return 1 - (0.08 * self.level)

	@events('player_spawn')
	def _on_spawn_set_gravity(self, player, **kwargs):
		'Called upon the player spawning.'
		player.gravity = self.percentage

	@events('player_death')
	def _on_death_reset_gravity(self, player, **kwargs):
		'Called upon the player dying.'
		player.gravity = 1.0