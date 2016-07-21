## IMPORTS

from commands import CommandReturn
from commands.say import SayCommand
from events import Event
from players.entity import Player
from players.helpers import userid_from_index
from menus import ListMenu
from menus import ListOption
from menus import PagedMenu
from menus import PagedOption
from menus import Text
from messages import SayText2
from translations.strings import LangStrings

from .heroes import *
from .skills import *

from .config import WARCRAFT_KILL_EXPERIENCE
from .config import WARCRAFT_ASSIST_EXPERIENCE
from .database import load_player_data
from .database import load_hero_data
from .database import save_player_data
from .database import save_hero_data
from .database import manager

## GLOBALS

players = dict()
strings = LangStrings('warcraft')

def unload():
    manager.connection.commit()
    manager.connection.close()

## MESSAGE DEFINITION

show_experience = SayText2(message=strings['show_experience'])
give_experience = SayText2(message=strings['give_experience'])
take_experience = SayText2(message=strings['take_experience'])

## MENU DEFINITION

def _on_spend_skills_build(menu, index):
    player = players[userid_from_index(index)]
    menu.clear()
    menu.description = strings['unused'].get_string(
        amount=player.hero.unused_points(player.hero.level))
    for skill in player.hero.skills:
        menu.append(PagedOption(strings['skill'].get_string(name=skill.name,
            level=skill.level, max_level=skill.max_level), skill))

def _on_spend_skills_select(menu, index, choice):
    player = players[userid_from_index(index)]
    skill = choice.value
    if player.hero.unused_points(player.hero.level) and skill.level < skill.max_level:
        skill.give_levels(1)
    return menu

spend_skills = PagedMenu(
    title=strings['spend_skills'],
    build_callback=_on_spend_skills_build,
    select_callback=_on_spend_skills_select,
)

def _on_change_hero_build(menu, index):
    player = players[userid_from_index(index)]
    menu.clear()
    menu.description = strings['change_hero']
    for hero in Hero.get_subclasses():
        menu.append(PagedOption(strings['hero'].get_string(hero=hero.name,
            requirement=hero.requirement), hero))

def _on_change_hero_select(menu, index, choice):
    player = players[userid_from_index(index)]
    hero = choice.value
    if not hero.name == player.hero.name and hero.meets_requirements(player):
        player.client_command('kill', True)
        player.hero = hero()
        load_hero_data(player)
    return

change_hero = PagedMenu(
    title=strings['change_hero'],
    build_callback=_on_change_hero_build,
    select_callback=_on_change_hero_select,
)

## SAY REGISTERS

@SayCommand('spendskills')
def _spend_skills_say_command(command, index, team_only=None):
    spend_skills.send(index)
    return CommandReturn.BLOCK

@SayCommand('changehero')
def _change_hero_say_command(command, index, team_only=None):
    change_hero.send(index)
    return CommandReturn.BLOCK

## DATABASE MANAGMENT

@Event('player_spawn')
def _on_spawn_message(event_data):
    if not event_data['userid'] in players:
        player = players[event_data['userid']] = Player.from_userid(event_data['userid'])
        load_player_data(player)
        load_hero_data(player)

    player = players[event_data['userid']]
    show_experience.send(player.index, hero=player.hero.name, level=player.hero.level,
        experience=player.hero.experience,
        needed=player.hero.required_experience(player.hero.level))

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
    give_experience.send(attacker.index, amount=WARCRAFT_KILL_EXPERIENCE,
        reason='for killing an enemy')

    if assister:
        assister.hero.give_experience(WARCRAFT_ASSIST_EXPERIENCE)
        give_experience.send(assister.index, amount=WARCRAFT_ASSIST_EXPERIENCE,
        reason='for assisting a kill')
        

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