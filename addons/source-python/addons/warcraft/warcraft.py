## IMPORTS

from events import Event
from players.dictionary import PlayerDictionary

from .config import WARCRAFT_KILL_EXPERIENCE
from .database import load_player_data
from .database import load_hero_data
from .database import save_player_data
from .database import save_hero_data

## GLOBALS

players = PlayerDictionary()

## DATABASE MANAGMENT

@Event('player_connect')
def _on_connect_load_data(event_data):
    player = players.from_userid(event_data['userid'])
    load_player_data(player)
    load_hero_data(player)

@Event('player_disconnect')
def _on_disconnect_save_data(event_data):
    player = players.from_userid(event_data['userid'])
    save_player_data(player)
    save_hero_data(player)

@Event('player_death')
def _on_death_save_data(event_data):
    player = players.from_userid(event_data['userid'])
    save_hero_data(player)

## EXPERIENCE GAIN

@Event('player_death')
def _on_kill_give_experience(event_data):
    attacker = players.from_userid(event_data['attacker'])
    attacker.hero.give_experience(WARCRAFT_KILL_EXPERIENCE)