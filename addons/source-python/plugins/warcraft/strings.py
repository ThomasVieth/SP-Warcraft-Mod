## IMPORTS

from messages import SayText2
from translations.strings import LangStrings

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

show_experience = SayText2(message=strings['show_experience'])
give_experience = SayText2(message=strings['give_experience'])
take_experience = SayText2(message=strings['take_experience'])