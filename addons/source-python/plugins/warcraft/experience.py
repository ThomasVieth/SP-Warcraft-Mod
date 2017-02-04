## IMPORTS

from events import Event

from .config import *
from .players import players
from .strings import give_experience

## ALL DECLARATION

__all__ = tuple()

## EXPERIENCE GAIN

@Event('player_spawn')
def _on_spawn_give_experience(event_data):
    player = players[event_data['userid']]
    exp = SPAWN_EXPERIENCE * MULTIPLIER_EXPERIENCE
    player.hero.give_experience(exp);
    give_experience.send(player.index, amount=exp, reason='on spawn')

@Event('player_death')
def _on_kill_assist_give_experience(event_data):
    if event_data['userid'] == event_data['attacker']:
        return

    attacker = players[event_data['attacker']]
    victim = players[event_data['userid']]
    assister = None
    if event_data['assister']:
        assister = players[event_data['assister']]

    attacker.hero.give_experience(WARCRAFT_KILL_EXPERIENCE)
    give_experience.send(attacker.index, amount=WARCRAFT_KILL_EXPERIENCE,
        reason='for killing an enemy')

    if assister:
        assister.hero.give_experience(WARCRAFT_ASSIST_EXPERIENCE)
        give_experience.send(assister.index, amount=WARCRAFT_ASSIST_EXPERIENCE,
        reason='for assisting a kill')
        
@Event('round_mvp')
def _give_xp_on_mvp(event_data):
    player = players[event_data['userid']]
    exp = SPAWN_EXPERIENCE * MULTIPLIER_EXPERIENCE
    give_experience.send(player.index, amount=exp, reason='for being MVP')
    player.hero.give_experience(exp)

@Event('round_end')
def _give_xp_on_round_end(event_data):
    for player in players.values():
        if player.team == 1:
            return
        key = 'WIN' if player.team == event_data['winner'] else 'LOSS'
        exp = eval(key + '_EXPERIENCE') * MULTIPLIER_EXPERIENCE
        give_experience.send(player.index, amount=exp, reason='for winning round')
        player.hero.give_experience(exp) 
        
@Event('bomb_planted')
def _give_xp_on_plant(event_data):
    player = players[event_data['userid']]
    exp = PLANT_EXPERIENCE * MULTIPLIER_EXPERIENCE
    player.hero.give_experience(exp)
    give_experience.send(player.index, amount=exp, reason='for planting bomb')
    
@Event('bomb_defused')
def _give_xp_on_defuse(event_data):
    player = players[event_data['userid']]
    exp = DEFUSE_EXPERIENCE * MULTIPLIER_EXPERIENCE
    player.hero.give_experience(exp)
    give_experience.send(player.index, amount=exp, reason='for planting bomb')
    
@Event('hostage_follows')
def _hostage_follows(event_data):
    player = players[event_data['userid']]
    exp = HOSTAGE_PICK_EXPERIENCE * MULTIPLIER_EXPERIENCE
    player.hero.give_experience(exp)
    give_experience.send(player.index, amount=exp, reason='for planting bomb')
