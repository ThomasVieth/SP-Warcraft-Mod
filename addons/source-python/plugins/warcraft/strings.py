## IMPORTS

from translations.strings import LangStrings

from .config import MESSAGE_TYPE

## ALL DECLARATION

__all__ = (
    'strings',
    'show_experience',
    'give_experience',
    'take_experience',
    )

## GLOBALS

strings = LangStrings('warcraft')

## MESSAGE DEFINITION

show_experience = MESSAGE_TYPE(message=strings['show_experience'])
give_experience = MESSAGE_TYPE(message=strings['give_experience'])
take_experience = MESSAGE_TYPE(message=strings['take_experience'])