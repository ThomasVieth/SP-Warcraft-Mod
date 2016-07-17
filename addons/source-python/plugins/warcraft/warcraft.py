## IMPORTS

from events import Event
from players.entity import Player
from messages import SayText2

from .config import WARCRAFT_KILL_EXPERIENCE
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
def _on_kill_give_experience(event_data):
    attacker = players[event_data['attacker']]
    attacker.hero.give_experience(WARCRAFT_KILL_EXPERIENCE)