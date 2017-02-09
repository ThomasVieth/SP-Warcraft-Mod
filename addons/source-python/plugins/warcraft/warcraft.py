## IMPORTS

from commands import CommandReturn
from commands.say import SayCommand
from events import Event
from players.helpers import userid_from_index

from .calls import *
from .experience import *
from .heroes import *
from .info import *
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