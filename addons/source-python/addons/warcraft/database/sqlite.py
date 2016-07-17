## IMPORTS

from sqlite3 import connect

from ..config import SQLITE_LOCATION
from ..config import WARCRAFT_DEFAULT_HERO

## ALL DECLARATION

__all__ = (
    'SQLite',
    )

## 

class SQLite:

    '''

    SQLite database manager. Loads
    data into <Player> instances, and
    saves data from <Player> instances
    to the database.

    '''

    def __init__(self, location):
    def __init__(self, location=SQLITE_LOCATION):
        self.connection = connect(location)
        self.cursor = self.connection.cursor()

        self.create_tables()
        
    def execute(self, statement, *args):
        if not isinstance(statement, str):
            raise TypeError('<SQLite>.execute requires a string statement.')

        self.cursor.execute(statement, *args)

    def create_tables(self):
        self.execute('''CREATE TABLE IF NOT EXISTS Players (
            SteamID Text PRIMARY KEY,
            Hero Text,
            Name Text
        )''')

        self.execute('''CREATE TABLE IF NOT EXISTS Heroes (
            SteamID Text,
            Name Text,
            Experience INTEGER,
            Level INTEGER,
            PRIMARY KEY (SteamID, Name)
        )''')

        self.execute('''CREATE TABLE IF NOT EXISTS Skills (
            SteamID Text,
            Hero Text,
            Name Text,
            Level INTEGER,
            PRIMARY KEY (SteamID, Hero, Name)
        )''')

    '''

    Adding rows to the database, for
    players, and heroes. Heroes must be
    supplied as a <class> and not an
    <object> when adding data.

    '''

    def add_player(self, player):
        self.execute('INSERT INTO Players (SteamID, Hero, Name) VALUES (?, ?, ?)',
            (player.steamid, WARCRAFT_DEFAULT_HERO.__name__, player.name))
        self.add_hero(player, WARCRAFT_DEFAULT_HERO())

    def add_hero(self, player, hero):
        self.execute('INSERT INTO Heroes (SteamID, Name, Experience, Level) VALUES (?, ?, ?, ?)',
            (player.steamid, hero.__class__.__name__, 0, 0))
        for skill in hero.skills:
            self.add_skill(player, hero, skill)

    def add_skill(self, player, hero, skill):
        self.execute('INSERT INTO Skills (SteamID, Hero, Name, Level) VALUES (?, ?, ?, ?)',
            (player.steamid, hero.__class__.__name__, skill.__class__.__name__, 0))

    '''

    Retrievable data from tables, please
    supply <object>s to these methods.

    '''

    def get_player_hero(self, player):
        self.execute('SELECT Hero FROM Players WHERE SteamID=?',
            (player.steamid, ))
        fetched_data = self.cursor.fetchone()
        if fetched_data is None:
            return None
        return fetched_data[0]

    def get_player_name(self, steamid):
        self.execute('SELECT Name FROM Players WHERE SteamID=?',
            (steamid, ))
        fetched_data = self.cursor.fetchone()
        if fetched_data is None:
            return None
        return fetched_data[0]

    def get_player_hero_data(self, player):
        self.execute('SELECT Experience, Level FROM Heroes WHERE SteamID=? AND Name=?', 
            (player.steamid, player.hero.__class__.__name__))
        return self.cursor.fetchone()

    def get_player_skill_level(self, player, hero, skill):
        self.execute('SELECT Level FROM Skills WHERE SteamID=? AND Hero=? AND Skill=?', 
            (player.steamid, hero.__class__.__name__, skill.__class__.__name__))
        fetched_data = self.cursor.fetchone()
        if fetched_data is None:
            return None
        return fetched_data[0]

    '''

    Save data to tables from <Player>,
    <Hero> or <Skill> instances.

    '''

    def set_player_hero(self, player):
        self.execute('UPDATE Players SET Hero=? WHERE SteamID=?',
            (player.hero.__class__.__name__, player.steamid))

    def set_player_name(self, player):
        self.execute('UPDATE Players SET Name=? WHERE SteamID=?',
            (player.name, player.steamid))

    def set_player_hero_data(self, player, hero):
        self.execute('UPDATE Heroes SET Experience=?, Level=? WHERE SteamID=? AND Name=?',
            (hero.experience, hero.level,
                player.steamid, hero.__class__.__name__))

    def set_player_skill_level(self, player, hero, skill):
        self.execute('UPDATE Skills SET Level=? WHERE SteamID=? AND Hero=? AND Name=?',
            (skill.level, player.steamid, hero.__class__.__name__, skill.__class__.__name__))