## IMPORTS

from players.helpers import userid_from_index
from menus import ListMenu
from menus import ListOption
from menus import PagedMenu
from menus import PagedOption
from menus import Text

from .database import load_hero_data
from .database import get_player_level
from .heroes import Hero
from .players import players
from .strings import strings

## ALL DECLARATION

__all__ = (
    'spend_skills',
    'change_hero',
    'main_menu',
    'hero_info',
    'current_hero',
    'player_info',
    )

## MENU DEFINITION

#
#   SPENDSKILLS
#

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

#
#   HEROINFO
#

def _on_hero_info_build(menu, index):
    player = players[userid_from_index(index)]
    menu.clear()
    menu.description = strings['hero_info']
    for hero in Hero.get_subclasses():
        menu.append(PagedOption(hero.name, hero, selectable=True))

def _on_hero_info_select(menu, index, choice):
    return HeroInfoMenu(choice.value, parent_menu=hero_info)


class HeroInfoMenu(ListMenu):
    """A menu class for displaying individual hero's information."""

    def __init__(self, hero, *args, **kwargs):
        """Initialize the hero info menu with a hero."""
        super().__init__(*args, **kwargs)
        self.hero = hero
        self.items_per_page = 5
        self.build_callback = self._build_callback

    @staticmethod
    def _build_callback(menu, player_index):
        """Build the menu."""
        menu.clear()
        menu.description = menu.hero.name
        for skill in menu.hero._skills:
            menu.append(PagedOption(strings['passive'].get_string(name=skill.name, description=skill.description), skill))

#
#   PLAYERINFO
#

def _on_player_info_build(menu, index):
    menu.clear()
    for player in players.values():
        if player.steamid != 'BOT':
            menu.append(PagedOption(player.name, player))

def _on_player_info_select(menu, index, choice):
    return PlayerInfoMenu(choice.value, parent_menu=player_info)


class PlayerInfoMenu(ListMenu):
    """A menu class for displaying individual hero's information."""

    def __init__(self, player, *args, **kwargs):
        """Initialize the hero info menu with a hero."""
        super().__init__(*args, **kwargs)
        self.player = player
        self.items_per_page = 6
        self.build_callback = self._build_callback

    @staticmethod
    def _build_callback(menu, player_index):
        """Build the menu."""
        level = get_player_level(menu.player)
        menu.clear()
        menu.title = strings['player_info']
        menu.description = menu.player.name
        menu.append(strings['hero_level'].get_string(name=menu.player.hero.name, info=menu.player.hero.hero_info))
        menu.append(strings['player_level'].get_string(level=level))
        menu.append(' ')
        menu.append(strings['health'].get_string(health=menu.player.health))
        menu.append(strings['speed'].get_string(speed=str(round(menu.player.speed*100))))
        menu.append(strings['gravity'].get_string(gravity=str(round(menu.player.gravity*100))))


#
#   CURRENTHERO
#

def _on_current_hero_build(menu, index):
    player = g_players[userid_from_index(index)]
    menu.clear()
    menu.description = 'Level : ' + player.hero.hero_info
    for skill in player.hero.skills:
        if skill.max_level == 0:
            menu.append(PagedOption(strings['passive'].get_string(name=skill.name, description=skill.description), skill))
        else:
            menu.append(PagedOption(strings['skill_info'].get_string(name=skill.name,
            level=skill.level, max_level=skill.max_level, description=skill.description), skill))

def _on_current_hero_select(menu, index):
    return menu

#
#   CHANGEHERO
#

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


#
#   MAIN
#

def _on_main_menu_select(menu, index, choice):
    if choice.value in _main_menu_selections:
        return _main_menu_selections[choice.value]

main_menu = PagedMenu(
    title=strings['main_menu'],
    select_callback=_on_main_menu_select,
    data=[
    PagedOption(strings['change_hero'], 1),
    PagedOption(strings['spend_skills'], 2),
    PagedOption(strings['hero_info'], 3),
    PagedOption(strings['current_hero'], 4),
    PagedOption(strings['player_info'], 5)
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

hero_info = PagedMenu(
    title=strings['hero_info'],
    build_callback=_on_hero_info_build,
    select_callback=_on_hero_info_select,
    parent_menu=main_menu,
)

current_hero = PagedMenu(
    title=strings['current_hero'],
    build_callback=_on_current_hero_build,
    select_callback=_on_current_hero_select,
    parent_menu=main_menu,
)

player_info = PagedMenu(
    title=strings['player_info'],
    build_callback=_on_player_info_build,
    select_callback=_on_player_info_select,
    parent_menu=main_menu,
)


_main_menu_selections = {
    1: change_hero,
    2: spend_skills,
    3: hero_info,
    4: current_hero,
    5: player_info,
}
