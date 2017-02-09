## IMPORTS

from events import Event
from players.entity import Player
from filters.weapons import WeaponClassIter

from .database import load_player_data
from .database import load_hero_data
from .database import save_player_data
from .database import save_hero_data
from .database import manager

## ALL DECLARATION

__all__ = (
    'players',
    )

## GLOBALS

players = dict()
all_weapons = set(weapon.name for weapon in WeaponClassIter())

def unload_database():
    manager.connection.commit()
    manager.connection.close()

## PLAYER MANAGMENT    
  
@Event('player_spawn')
def _remove_restrict_on_spawn_message(event_data):
    player = players[event_data['userid']]
    if player.team in [2,3]:
        player.unrestrict_weapons(*all_weapons)   
    
## DATABASE MANAGMENT

@Event('player_spawn')
def _on_spawn_message(event_data):
    if not event_data['userid'] in players:
        player = players[event_data['userid']] = Player.from_userid(event_data['userid'])
        load_player_data(player)
        load_hero_data(player)

    player = players[event_data['userid']]

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
