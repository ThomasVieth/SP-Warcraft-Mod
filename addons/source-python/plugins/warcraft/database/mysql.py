## IMPORTS

from pymysql import connect

from ..config import MYSQL_ADDRESS
from ..config import MYSQL_LOGIN
from ..config import MYSQL_PASSWORD
from ..config import MYSQL_DATABASE_NAME
from .sqlite import SQLite

## ALL DECLARATION

__all__ = (
    'MySQL',
    )

## 

class MySQL(SQLite):

    '''

    MySQL database manager. Loads
    data into <Player> instances, and
    saves data from <Player> instances
    to the database.

    '''

    def __init__(self, host=MYSQL_ADDRESS, user=MYSQL_LOGIN, pw=MYSQL_PASSWORD, db=MYSQL_DATABASE_NAME):
        self.connection = connect(host=host, user=user, password=pw, db=db)
        self.cursor = self.connection.cursor()

        self.create_tables()