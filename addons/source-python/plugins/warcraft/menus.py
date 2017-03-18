## IMPORTS

from players.helpers import userid_from_index
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
    )

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

def _on_rank_build(menu, index):
    menu.clear()
    ranks = list(get_rank_list())
    length = len(ranks)
    for num in range(0, length):
          player_data = ranks[num]
        name = player_data[2]
        menu.append(PagedOption('{} - {}'.format(num+1, name), player_data))
    
def _on_rank_select(menu, index, choice):
    steamid, hero, name, total = choice.value
    player_rank = ListMenu(title=name, description='Total Level: {}'.format(total))
    player_rank.append(ListOption('Current Hero: {}'.format(hero)))
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
    PagedOption(strings['warcraft_rank'], 3)
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
}
