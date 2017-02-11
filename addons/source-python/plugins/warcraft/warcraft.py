## IMPORTS

from commands import CommandReturn
from commands.say import SayCommand
from engines.precache import Model
from entities.entity import Entity
from entities.helpers import index_from_pointer
from events import Event
from listeners.tick import Delay
from players.helpers import userid_from_index

from .calls import *
from .experience import *
from .heroes import *
from .info import *
from .listeners import HeroLevelChange
from .menus import *
from .players import *
from .strings import *

## UNLOAD PLAYERS

def unload():
    unload_database()

## SAY REGISTERS

@SayCommand(['heroinfo', 'showxp'])
def _show_xp_say_command(command, index, team_only=None):
    player = players[userid_from_index(index)]
    show_experience.send(index, hero=player.hero.name, level=player.hero.level,
        experience=player.hero.experience,
        needed=player.hero.required_experience(player.hero.level))
    return CommandReturn.BLOCK

@SayCommand('spendskills')
def _spend_skills_say_command(command, index, team_only=None):
    spend_skills.send(index)
    return CommandReturn.BLOCK

@SayCommand('changehero')
def _change_hero_say_command(command, index, team_only=None):
    change_hero.send(index)
    return CommandReturn.BLOCK

@SayCommand('warcraft')
def _change_hero_say_command(command, index, team_only=None):
    main_menu.send(index)
    return CommandReturn.BLOCK

## MESSAGE SENDING

@Event('player_spawn')
def _on_spawn_send_show_xp(event_data):
    player = players[event_data['userid']]
    show_experience.send(player.index, hero=player.hero.name, level=player.hero.level,
        experience=player.hero.experience,
        needed=player.hero.required_experience(player.hero.level))
    
## LEVEL UP

@HeroLevelChange
def _on_level_change(hero):
    player = hero.owner
    spend_skills.send(player)
    pointer = player.give_named_item('env_smokestack', 0, None, False)
    entity = Entity(index_from_pointer(pointer))

    Model('effects/yellowflare.vmt')
    for output in ('basespread 10', 'spreadspeed 60', 'initial 0', 'speed 105',
        'rate 50', 'startsize 7', 'endsize 2', 'twist 0', 'jetlength 100',
        'angles 0 0 0', 'rendermode 18', 'renderamt 100',
        'rendercolor 255 255 3', 'SmokeMaterial effects/yellowflare.vmt'):
        entity.add_output(output)

    entity.turn_on()
    entity.set_parent(player.pointer, -1)
    entity.delay(0.5, entity.turn_off)
