## IMPORTS

from . import Skill
from . import events
from . import clientcommands
from ..cooldown import Cooldown

from colors import Color
from random import randint

## ------------------------------
## ON SPAWN SKILLS
## ------------------------------

class spawnGiveItem(Skill):
	'Gives a weapon on spawning.'
	max_level = 8

	@property
	def chance(self):
		'The chance at which the player will get the item.'
		return 40 + (5 * self.level)

	@property
	def item_name(self):
		'The name of the item to give the player.'
		return 'weapon_ak47'

	@events('player_spawn')
	def _on_spawn(self, player, **kwargs):
		'Called upon the player spawning.'
		if randint(0, 100) > self.chance:
			return

		player.give_named_item(self.item_name)

class spawnInvisPercent(Skill):
	'Granted invisbility by percentage.'
	max_level = 8

	@property
	def percentage(self):
		'The percentage at which the player should be invisible. 0 = Not invisibile. 100 = Completely Invisible.'
		return 40 + (5 * self.level)

	@events('player_spawn')
	def _on_spawn(self, player, **kwargs):
		'Called upon the player spawning.'
		alpha = round(255*(self.percentage/100), 0) # Calculate the color alpha.
		color = player.color
		color.a = alpha
		player.color = color

class spawnColor(Skill):
	'Change a players color on spawn.'
	max_level = 8

	@property
	def alpha(self):
		'The alpha of the player.'
		return 255

	@property
	def color(self):
		'The color that the player should be. (RGB)'
		return (100, 100, 100)

	@events('player_spawn')
	def _on_spawn(self, player, **kwargs):
		'Called upon the player spawning.'
		player.color = Color(*self.color).with_alpha(self.alpha)

class spawnSpeed(Skill):
	'Movement speed increased upon spawning.'
	max_level = 8

	@property
	def addition(self):
		return 0.1 + (self.level * 0.05)

	@events('player_spawn')
	def _on_spawn(self, player, **kwargs):
		'Called upon the player spawning.'
		player.speed += self.addition

class spawnHealth(Skill):
	'Increased health upon spawning.'
	max_level = 8

	@property
	def addition(self):
		return 10 + (self.level * 5)

	@events('player_spawn')
	def _on_spawn(self, player, **kwargs):
		'Called upon the player spawning.'
		player.health += self.addition

class spawnGravity(Skill):
	'Decrease your gravity when spawned.'
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

## ------------------------------
## ON VICTIM SKILLS
## ------------------------------

class victimEvasion(Skill):
	'Given a chance to avoid incoming attacks.'
	max_level = 8

	@property
	def chance(self):
		'The chance in which you will evade damage.'
		return 16 + (self.level * 2)

	@events('player_pre_victim')
	def _on_pre_victim(self, player, take_damage_info, **kwargs):
		'Called upon the <on_take_damage> function happening.'
		if randint(0, 100) > self.chance:
			return

		take_damage_info.damage = 0


## ------------------------------
## ON ATTACK SKILLS
## ------------------------------

class attackSlow(Skill):
	'Slow enemies that you damage.'
	max_level = 8

	@property
	def chance(self):
		'The chance in which you will slow them.'
		return 20 + (self.level * 10)

	@property
	def cooldown(self):
		'The cooldown of this skill happening.'
		return 16 - self.level

	@property
	def duration(self):
		'The length of time which to be slowed for.'
		return 0.5 * self.level

	@events('player_attack')
	def _on_attack(self, player, victim, **kwargs):
		'Called upon the <player_hurt> event happening.'
		if randint(1, 100) > 30 or not self._cooldown.is_over:
			return

		self._cooldown = Cooldown(self.cooldown)
		speed = victim.speed
		victim.speed -= 0.2
		victim.delay(self.duration, victim.__setattr__, ('speed', speed))

class attackCash(Skill):
	'Remove the enemies cash upon damaging someone.'
	max_level = 8

	@property
	def cash(self):
		'The cash that you will remove.'
		return (self.level + 5) * 10

	@events('player_attack')
	def _on_attack(self, player, victim, **kwargs):
		'Called upon the <player_hurt> event happening.'
		if randint(1, 100) > 30 or victim.cash < self.cash:
			return

		victim.cash -= self._cash

class attackBeserk(Skill):
	'Gain speed when you successfully damage an enemy.'
	max_level = 8

	@property
	def chance(self):
		'The chance in which you will go beserk.'
		return 20 + (self.level * 10)

	@property
	def addition(self):
		'The speed which you gain after damaging an enemy.'
		return 0.04 + (0.005 * self.level)

	@property
	def maximum(self):
		'The maximum speed you can ever reach.'
		return 1.3 + (0.05 * self.level)

	@events('player_attack')
	def _on_attack(self, player, **kwargs):
		'Called upon the <player_hurt> event happening.'
		if randint(0, 100) > self.chance:
			return

		self._go_beserk(player)

	def _go_beserk(self, player):
		player.speed = min(player.speed+self.addition, self.maximum)


class attackLifesteal(Skill):
	'Steal health whenever you successfully damage an enemy.'
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

class attackRemoveInvis(Skill):
	'Remove the enemies invisibility if they have any.'
	max_level = 8

	@property
	def chance(self):
		'The chance in which you will remove the victims invis.'
		return 30 + (self.level * 6)

	@events('player_attack')
	def _on_attacker(self, player, victim, **kwargs):
		'Called upon the <player_hurt> event happening.'
		if randint(0, 100) > self.chance:
			return

		color = victim.color
		if color.a < 255:
			color.a = 255
			victim.color = color


## ------------------------------
## MISC SKILLS
## ------------------------------

class miscLongjump(Skill):
	'Increased distance for jumping.'
	max_level = 8

	@property
	def multiplier(self):
		'The velocity multiplier for the longjump.'
		return 200 + (10 * self.level)

	@events('player_jump')
	def _on_jump(self, player, **kwargs):
		'Called upon the <player_jump> event happening.'
		player.push(self.multiplier, self.multiplier)