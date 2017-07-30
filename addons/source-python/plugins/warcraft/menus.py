## IMPORTS

from menus import ListMenu
from menus import ListOption
from menus import PagedMenu
from menus import PagedOption
from menus import Text

from .database import load_hero_data
from .database import get_rank_list
from .heroes import Hero
from .players import players
from .strings import strings

## ALL DECLARATION

__all__ = (
    'spend_skills',
    'change_hero',
    'warcraft_rank',
    'main_menu',
    'player_info',
    )

## MENU DEFINITION

def _on_spend_skills_build(menu, index):
    player = players[index]
    menu.clear()
    menu.description = strings['unused'].get_string(
        amount=player.hero.unused_points(player.hero.level))
    for skill in player.hero.skills:
        menu.append(PagedOption(strings['skill'].get_string(name=skill.name,
            level=skill.level, max_level=skill.max_level), skill))

def _on_spend_skills_select(menu, index, choice):
    player = players[index]
    skill = choice.value
    if player.hero.unused_points(player.hero.level) and skill.level < skill.max_level:
        skill.give_levels(1)
    if player.hero.unused_points(player.hero.level) > 0:
        return menu

def _on_player_info_build(menu, index):
    menu.clear()
    for player in players.values():
        menu.append(PagedOption(player.name, player))

def _on_player_info_select(menu, index, choice):
    player = choice.value
    player_info_menu = ListMenu(title=player.name, parent_menu=menu)
    player_info_menu.append(Text(player.hero.name))
    player_info_menu.append(Text(' '))
    for skill in player.hero.skills:
        player_info_menu.append(Text('{} ({}/{})'.format(skill.name, skill.level,
            skill.max_level)))
    return player_info_menu

def _on_change_hero_build(menu, index):
    player = players[index]
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
    player = players[index]
    hero = choice.value
    if not hero.name == player.hero.name and hero.meets_requirements(player):
        player.client_command('kill', True)
        player.hero = hero()
        load_hero_data(player)
    return

def _on_rank_build(menu, index):
    menu.clear()
    ranks = list(get_rank_list())
    length = len(ranks)
    for num in range(0, length):
        player_data = ranks[num]
        name = player_data[2]
        menu.append(PagedOption('{} - {}'.format(num+1, name), player_data))
    
def _on_rank_select(menu, index, choice):
    steamid, hero_name, player_name, total = choice.value
    hero = Hero.get_subclass_dict()[hero_name]
    player_rank = ListMenu(title=player_name, description='Total Level: {}'.format(total),
        parent_menu=menu)
    player_rank.append(ListOption('Steam ID: {}'.format(steamid)))
    player_rank.append(Text(' '))
    player_rank.append(ListOption('Current Hero: {}'.format(hero.name)))
    return player_rank

def _on_main_menu_select(menu, index, choice):
    if choice.value in _main_menu_selections:
        return _main_menu_selections[choice.value]    
    
main_menu = PagedMenu(
    title=strings['main_menu'],
    select_callback=_on_main_menu_select,
    data=[
    PagedOption(strings['change_hero'], 1),
    PagedOption(strings['spend_skills'], 2),
    PagedOption(strings['warcraft_rank'], 3),
    PagedOption(strings['player_info'], 4)
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

player_info = PagedMenu(
    title=strings['player_info'],
    build_callback=_on_player_info_build,
    select_callback=_on_player_info_select,
    parent_menu=main_menu,
)
    
warcraft_rank = PagedMenu(
    title=strings['warcraft_rank'],
    build_callback=_on_rank_build,
    select_callback=_on_rank_select,
    parent_menu=main_menu,
)

_main_menu_selections = {
    1: change_hero,
    2: spend_skills,
    3: warcraft_rank,
    4: player_info,
}
