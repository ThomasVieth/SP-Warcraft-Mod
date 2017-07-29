## IMPORTS

from events import Event
from players.dictionary import PlayerDictionary
from players.entity import Player
from players.helpers import index_from_userid
from filters.players import PlayerIter
from filters.weapons import WeaponClassIter

from .database import load_player_data
from .database import load_hero_data
from .database import save_player_data
from .database import save_hero_data
from .database import manager

## ALL DECLARATION

__all__ = (
    'players',
    'unload_database',
    )

## SETUP PLAYER

def setup_player(index):
    player = Player(index)
    load_player_data(player)
    load_hero_data(player)
    return player

## GLOBALS

players = PlayerDictionary(factory=setup_player)

def unload_database():
    manager.connection.commit()
    manager.connection.close()

## DATABASE MANAGMENT
@Event('player_disconnect')
def _on_disconnect_save_data(event_data):
    player = players.from_userid(event_data['userid'])
    save_player_data(player)
    save_hero_data(player)
    del players[player.index]

@Event('player_death')
def _on_death_save_data(event_data):
    player = players.from_userid(event_data['userid'])
    save_hero_data(player)
