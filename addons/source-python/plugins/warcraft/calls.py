## IMPORTS

from entities import TakeDamageInfo
from entities.hooks import EntityCondition
from entities.hooks import EntityPreHook
from events import Event
from memory import make_object
from players.helpers import userid_from_pointer

from .players import players

## CALL EVENTS

@Event('player_death')
def _on_kill_assist_call_events(event_data):
    if event_data['userid'] == event_data['attacker'] or event_data['attacker'] == 0:
        player = players[event_data['userid']]
        player.hero.call_events('player_suicide', player=player)
        return

    attacker = players[event_data['attacker']]
    victim = players[event_data['userid']]
    assister = None
    if event_data['assister']:
        assister = players[event_data['assister']]

    attacker.hero.call_events('player_kill', player=attacker, victim=victim,
        assister=assister)
    victim.hero.call_events('player_death', player=victim, attacker=attacker,
        assister=assister)
    if assister:
        assister.hero.call_events('player_assist', player=assister, attacker=attacker,
            victim=victim)

@Event('player_spawn')
def _on_spawn_call_events(event_data):
    player = players[event_data['userid']]

    player.hero.call_events('player_spawn', player=player)

@Event('player_hurt')
def _on_hurt_call_events(event_data):
    if event_data['userid'] == event_data['attacker'] or event_data['attacker'] == 0:
        return

    attacker = players[event_data['attacker']]
    victim = players[event_data['userid']]

    if victim.team == attacker.team:
        attacker.hero.call_events('player_teammate_attack', player=attacker,
            victim=victim, attacker=attacker)
        victim.hero.call_events('player_teammate_victim', player=victim,
            attacker=attacker, victim=victim)
        return

    attacker.hero.call_events('player_attack', player=attacker, victim=victim,
        attacker=attacker)
    victim.hero.call_events('player_victim', player=victim, attacker=attacker,
        victim=victim)

@EntityPreHook(EntityCondition.is_player, 'on_take_damage')
def _pre_damage_call_events(args):
    take_damage_info = make_object(TakeDamageInfo, args[1])
    if not take_damage_info.attacker:
        return
    attacker = players[userid_from_index(take_damage_info.attacker)]
    victim = players[userid_from_pointer(args[0])]

    event_args = {
        'attacker': attacker,
        'victim': victim,
        'take_damage_info': take_damage_info,
    }

    if victim.team == attacker.team:
        attacker.hero.call_events('player_pre_teammate_attack', player=attacker,
            **event_args)
        victim.hero.call_events('player_pre_teammate_victim', player=victim, **event_args)
        return

    attacker.hero.call_events('player_pre_attack', player=attacker, **event_args)
    victim.hero.call_events('player_pre_victim', player=victim, **event_args)