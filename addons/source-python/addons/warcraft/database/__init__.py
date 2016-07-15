## IMPORTS

from ..config import DATABASE_TYPE
from ..debug import log
from .sqlite import SQLite

## ALL DECLARATION

__all__ = (
    'manager',
    )

## DATABASE CHOICE

if DATABASE_TYPE == 1:
    manager = SQLite()
else:
    log(2, 'Cannot load database. Config files states only types 1 or 2.')