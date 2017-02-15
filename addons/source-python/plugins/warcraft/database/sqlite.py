## IMPORTS

from sqlite3 import connect

from ..config import SQLITE_LOCATION
from ..config import WARCRAFT_DEFAULT_HERO
from ..heroes import Hero

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

    def __init__(self, location=SQLITE_LOCATION):
        self.connection = connect(location)
        self.cursor = self.connection.cursor()

        self.create_tables()
        
    def execute(self, statement, *args):
        if not isinstance(statement, str):
            raise TypeError('<{}>.execute requires a string statement.'.format(self.__class__.__name__))

        self.cursor.execute(statement, *args)

    def create_tables(self):
        self.execute('''CREATE TABLE IF NOT EXISTS Players (
            SteamID VARCHAR(32) PRIMARY KEY,
            Hero VARCHAR(32),
            Name VARCHAR(255)
        )''')

        self.execute('''CREATE TABLE IF NOT EXISTS Heroes (
            SteamID VARCHAR(32),
            Name VARCHAR(32),
            Experience INTEGER,
            Level INTEGER
        )''')

        self.execute('''CREATE TABLE IF NOT EXISTS Skills (
            SteamID VARCHAR(32),
            Hero VARCHAR(32),
            Name VARCHAR(32),
            Level INTEGER
        )''')

    # Adding rows to the database, for
    # players, and heroes.

    def add_player(self, player):
        self.execute("INSERT INTO Players (SteamID, Hero, Name) VALUES ('{}', '{}', '{}')".format(
            player.uniqueid, WARCRAFT_DEFAULT_HERO, player.name))
        self.add_hero(player, Hero.get_subclass_dict()[WARCRAFT_DEFAULT_HERO]())

    def add_hero(self, player, hero):
        self.execute("INSERT INTO Heroes (SteamID, Name, Experience, Level) VALUES ('{}', '{}', {}, {})".format(
            player.uniqueid, hero.__class__.__name__, 0, 0))
        for skill in hero.skills:
            self.add_skill(player, hero, skill)

    def add_skill(self, player, hero, skill):
        self.execute("INSERT INTO Skills (SteamID, Hero, Name, Level) VALUES ('{}', '{}', '{}', {})".format(
            player.uniqueid, hero.__class__.__name__, skill.__class__.__name__, 0))


    # Retrievable data from tables, please
    # supply <Player>s to these methods.


    def get_player_hero(self, player):
        self.execute("SELECT Hero FROM Players WHERE SteamID='{}'".format(
            player.uniqueid, ))
        fetched_data = self.cursor.fetchone()
        if fetched_data is None:
            return None
        return fetched_data[0]

    def get_player_name(self, uniqueid):
        self.execute("SELECT Name FROM Players WHERE SteamID='{}'".format(
            uniqueid, ))
        fetched_data = self.cursor.fetchone()
        if fetched_data is None:
            return None
        return fetched_data[0]

    def get_player_hero_data(self, player):
        self.execute("SELECT Experience, Level FROM Heroes WHERE SteamID='{}' AND Name='{}'".format(
            player.uniqueid, player.hero.__class__.__name__))
        return self.cursor.fetchone()

    def get_player_skill_level(self, player, hero, skill):
        self.execute("SELECT Level FROM Skills WHERE SteamID='{}' AND Hero='{}' AND Name='{}'".format(
            player.uniqueid, hero.__class__.__name__, skill.__class__.__name__))
        fetched_data = self.cursor.fetchone()
        if fetched_data is None:
            return None
        return fetched_data[0]

    def get_total_level(self, player):
        self.execute("SELECT SUM(Level) FROM Heroes WHERE SteamID='{}'".format(
            player.uniqueid))
        fetched_data = self.cursor.fetchone()
        if fetched_data is None:
            return None
        return fetched_data[0]
    
    def get_rank_list(self):
        self.execute("""SELECT P.*, SUM(H.Level) as total_level
            FROM Players P, Heroes H
            WHERE P.SteamID = H.SteamID
            AND P.SteamID NOT LIKE 'BOT%'
            GROUP BY P.SteamID
            ORDER BY total_level DESC
        """)
        fetched_data = self.cursor.fetchall()
        if fetched_data is None:
            return None
        return fetched_data
    

    # Save data to tables from <Player>,
    # <Hero> or <Skill> instances.


    def set_player_hero(self, player):
        self.execute("UPDATE Players SET Hero='{}' WHERE SteamID='{}'".format(
            player.hero.__class__.__name__, player.uniqueid))

    def set_player_name(self, player):
        self.execute("UPDATE Players SET Name='{}' WHERE SteamID='{}'".format(
            player.name, player.uniqueid))

    def set_player_hero_data(self, player, hero):
        self.execute("UPDATE Heroes SET Experience={}, Level={} WHERE SteamID='{}' AND Name='{}'".format(
            hero.experience, hero.level, player.uniqueid, hero.__class__.__name__))

    def set_player_skill_level(self, player, hero, skill):
        self.execute("UPDATE Skills SET Level={} WHERE SteamID='{}' AND Hero='{}' AND Name='{}'".format(
            skill.level, player.uniqueid, hero.__class__.__name__, skill.__class__.__name__))
