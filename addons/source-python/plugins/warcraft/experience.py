## IMPORTS

from events import Event

from .config import (WARCRAFT_KILL_EXPERIENCE, WARCRAFT_ASSIST_EXPERIENCE,
                     WARCRAFT_HEADSHOT_EXPERIENCE, WARCRAFT_KNIFE_EXPERIENCE,
                     WARCRAFT_ROUND_WIN_EXPERIENCE, WARCRAFT_ROUND_LOSS_EXPERIENCE,
                     WARCRAFT_PLANT_EXPERIENCE, WARCRAFT_EXPLODE_EXPERIENCE, WARCRAFT_DEFUSE_EXPERIENCE,
                     WARCRAFT_CHICKEN_EXPERIENCE)
from .players import players
from .strings import give_experience

## ALL DECLARATION

__all__ = tuple()

## EXPERIENCE GAIN

@Event('other_death')
def _on_kill_other_give_experience(event_data):
    if event_data['userid'] == event_data['attacker'] or event_data['attacker'] == 0:
        return

    attacker = players.from_userid(event_data['attacker'])
    attacker.hero.give_experience(WARCRAFT_CHICKEN_EXPERIENCE)
    give_experience.send(attacker.index, amount=WARCRAFT_CHICKEN_EXPERIENCE,
        reason='for killing a chicken')

@Event('player_death')
def _on_kill_assist_give_experience(event_data):
    if event_data['userid'] == event_data['attacker'] or event_data['attacker'] == 0:
        return

    attacker = players.from_userid(event_data['attacker'])

    exp = WARCRAFT_KILL_EXPERIENCE
    reason = 'for killing an enemy'

    if event_data['weapon'] == 'knife':
        exp += WARCRAFT_KNIFE_EXPERIENCE
        reason += ' with a knife'

    if event_data['headshot']:
        exp += WARCRAFT_HEADSHOT_EXPERIENCE
        reason += ' with a headshot'

    attacker.hero.give_experience(exp)
    give_experience.send(attacker.index, amount=exp, reason=reason)

    if 'assister' in event_data.variables and event_data['assister']:
        assister = players.from_userid(event_data['assister'])

        assister.hero.give_experience(WARCRAFT_ASSIST_EXPERIENCE)
        give_experience.send(assister.index, amount=WARCRAFT_ASSIST_EXPERIENCE,
        reason='for assisting a kill')

@Event('round_end')
def _on_round_end_give_experience(event_data):
    winner = event_data['winner']
    for player in players.values():
        if player.team == winner:
            player.hero.give_experience(WARCRAFT_ROUND_WIN_EXPERIENCE)
            give_experience.send(player.index, amount=WARCRAFT_ROUND_WIN_EXPERIENCE,
                reason='for winning a round')
        elif player.team == 5-winner:
            player.hero.give_experience(WARCRAFT_ROUND_LOSS_EXPERIENCE)
            give_experience.send(player.index, amount=WARCRAFT_ROUND_LOSS_EXPERIENCE,
                reason='for losing a round')

@Event('bomb_planted')
def _on_plant_give_experience(event_data):
    player = players.from_userid(event_data['userid'])
    player.hero.give_experience(WARCRAFT_PLANT_EXPERIENCE)
    give_experience.send(player.index, amount=WARCRAFT_PLANT_EXPERIENCE,
                reason='for planting the bomb')

@Event('bomb_exploded')
def _on_explode_give_experience(event_data):
    player = players.from_userid(event_data['userid'])
    player.hero.give_experience(WARCRAFT_EXPLODE_EXPERIENCE)
    give_experience.send(player.index, amount=WARCRAFT_EXPLODE_EXPERIENCE,
                reason='for making the bomb explode')

@Event('bomb_defused')
def _on_defuse_give_experience(event_data):
    player = players.from_userid(event_data['userid'])
    player.hero.give_experience(WARCRAFT_DEFUSE_EXPERIENCE)
    give_experience.send(player.index, amount=WARCRAFT_DEFUSE_EXPERIENCE,
                reason='for defusing the bomb')
