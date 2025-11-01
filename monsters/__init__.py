"""
Monsters package - Irish mythological creatures.

Each monster has unique stats and can have unique behaviors.
"""

from monsters.base_monster import BaseMonster
from monsters.banshee import Banshee
from monsters.leprechaun import Leprechaun
from monsters.pooka import Pooka
from monsters.selkie import Selkie
from monsters.dullahan import Dullahan
from monsters.changeling import Changeling
from monsters.clurichaun import Clurichaun
from monsters.merrow import Merrow
from monsters.fear_gorta import FearGorta
from monsters.cat_si import CatSi

# List of all available monster classes
# This is automatically discovered - just add new monster classes to the imports above!
ALL_MONSTER_CLASSES = [
    Banshee,
    Leprechaun,
    Pooka,
    Selkie,
    Dullahan,
    Changeling,
    Clurichaun,
    Merrow,
    FearGorta,
    CatSi,
]

# Dictionary for easy monster creation by type string (backward compatibility)
MONSTER_CLASSES = {
    'banshee': Banshee,
    'leprechaun': Leprechaun,
    'pooka': Pooka,
    'selkie': Selkie,
    'dullahan': Dullahan,
    'changeling': Changeling,
    'clurichaun': Clurichaun,
    'merrow': Merrow,
    'fear_gorta': FearGorta,
    'cat_si': CatSi,
}

__all__ = [
    'BaseMonster',
    'Banshee',
    'Leprechaun',
    'Pooka',
    'Selkie',
    'Dullahan',
    'Changeling',
    'Clurichaun',
    'Merrow',
    'FearGorta',
    'CatSi',
    'ALL_MONSTER_CLASSES',
    'MONSTER_CLASSES',
]
