## IMPORTS

from commands import CommandReturn
from commands.say import SayCommand
from events import Event
from players.helpers import userid_from_index
from menus import ListMenu
from menus import ListOption
from menus import PagedMenu
from menus import PagedOption
from menus import Text
from messages import SayText2
from translations.strings import LangStrings

from .calls import *
from .experience import *
from .heroes import *
from .skills import *
from .players import players

## GLOBALS

strings = LangStrings('warcraft')

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

def _on_change_hero_build(menu, index):
    player = players[userid_from_index(index)]
    menu.clear()
    menu.description = strings['change_hero']
    for hero in Hero.get_subclasses():
        if not hero.meets_requirements(player):
            menu.append(PagedOption(strings['hero'].get_string(hero=hero.name,
                requirement=hero.requirement), hero, selectable=False))
        else:
            menu.append(PagedOption(strings['hero'].get_string(hero=hero.name,
                requirement='Owned'), hero, selectable=True))

def _on_change_hero_select(menu, index, choice):
    player = players[userid_from_index(index)]
    hero = choice.value
    if not hero.name == player.hero.name and hero.meets_requirements(player):
        player.client_command('kill', True)
        player.hero = hero()
        load_hero_data(player)
    return

def _on_main_menu_select(menu, index, choice):
    if choice.value in _main_menu_selections:
        return _main_menu_selections[choice.value]

main_menu = PagedMenu(
    title=strings['main_menu'],
    select_callback=_on_main_menu_select,
    data=[
    PagedOption(strings['change_hero'], 1),
    PagedOption(strings['spend_skills'], 2)
    ]
)

change_hero = PagedMenu(
    title=strings['change_hero'],
    build_callback=_on_change_hero_build,
    select_callback=_on_change_hero_select,
    parent_menu=main_menu,
)

spend_skills = PagedMenu(
    title=strings['spend_skills'],
    build_callback=_on_spend_skills_build,
    select_callback=_on_spend_skills_select,
    parent_menu=main_menu,
)

_main_menu_selections = {
    1: change_hero,
    2: spend_skills,
}

## SAY REGISTERS

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