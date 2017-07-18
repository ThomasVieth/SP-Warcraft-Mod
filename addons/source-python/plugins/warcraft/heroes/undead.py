## TEST HERO

from . import Hero
from .extensions import attackLifesteal, spawnGravity, spawnSpeed

class Undead(Hero):
    name = 'Undead Scourge'

@Undead.skill
class Unholy(spawnSpeed):
    name = 'Unholy Aura'

    @property
    def addition(self):
        return 0.2 + (self.level * 0.05)

@Undead.skill
class Levitation(spawnGravity):
    name = 'Levitation'

@Undead.skill
class Vampiric(attackLifesteal):
    name = 'Vampiric Aura'