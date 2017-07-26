## IMPORTS

from events import Event

from .config import WARCRAFT_KILL_EXPERIENCE
from .config import WARCRAFT_ASSIST_EXPERIENCE
from .players import players
from .strings import give_experience

## ALL DECLARATION

__all__ = tuple()

## EXPERIENCE GAIN

@Event('player_death')
def _on_kill_assist_give_experience(event_data):
    if event_data['userid'] == event_data['attacker']:
        return

    attacker = players.from_userid(event_data['attacker'])
    victim = players.from_userid(event_data['userid'])
    assister = None
    if event_data['assister']:
        assister = players.from_userid(event_data['assister'])

    attacker.hero.give_experience(WARCRAFT_KILL_EXPERIENCE)
    give_experience.send(attacker.index, amount=WARCRAFT_KILL_EXPERIENCE,
        reason='for killing an enemy')

    if assister:
        assister.hero.give_experience(WARCRAFT_ASSIST_EXPERIENCE)
        give_experience.send(assister.index, amount=WARCRAFT_ASSIST_EXPERIENCE,
        reason='for assisting a kill')
