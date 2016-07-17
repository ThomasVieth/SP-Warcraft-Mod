## IMPORTS

from events import Event
from players.entity import Player
from messages import SayText2

from .config import WARCRAFT_KILL_EXPERIENCE
from .config import WARCRAFT_ASSIST_EXPERIENCE
from .database import load_player_data
from .database import load_hero_data
from .database import save_player_data
from .database import save_hero_data
from .database import manager
from .heroes import *
from .skills import *

## GLOBALS

players = dict()

def unload():
    manager.connection.commit()
    manager.connection.close()

## DATABASE MANAGMENT

@Event('player_spawn')
def _on_spawn_message(event_data):
    if not event_data['userid'] in players:
        player = players[event_data['userid']] = Player.from_userid(event_data['userid'])
        load_player_data(player)
        load_hero_data(player)

    player = players[event_data['userid']]
    SayText2('Playing {} LV {}, XP {}/{}'.format(
        player.hero.name, player.hero.level,
        player.hero.experience, player.hero.required_experience(player.hero.level)
        )).send(player.index)

@Event('player_disconnect')
def _on_disconnect_save_data(event_data):
    player = players[event_data['userid']]
    save_player_data(player)
    save_hero_data(player)
    del players[event_data['userid']]

@Event('player_death')
def _on_death_save_data(event_data):
    player = players[event_data['userid']]
    save_hero_data(player)

## EXPERIENCE GAIN

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

    if assister:
        assister.hero.give_experience(WARCRAFT_ASSIST_EXPERIENCE)
        

## CALL EVENTS

@Event('player_death')
def _on_kill_assist_call_events(event_data):
    if event_data['userid'] == event_data['attacker']:
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