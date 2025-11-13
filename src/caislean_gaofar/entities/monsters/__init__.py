"""
Monsters package - Irish mythological creatures.

Each monster has unique stats and can have unique behaviors.
"""

from caislean_gaofar.entities.monsters.base_monster import BaseMonster
from caislean_gaofar.entities.monsters.banshee import Banshee
from caislean_gaofar.entities.monsters.leprechaun import Leprechaun
from caislean_gaofar.entities.monsters.pooka import Pooka
from caislean_gaofar.entities.monsters.selkie import Selkie
from caislean_gaofar.entities.monsters.dullahan import Dullahan
from caislean_gaofar.entities.monsters.changeling import Changeling
from caislean_gaofar.entities.monsters.clurichaun import Clurichaun
from caislean_gaofar.entities.monsters.merrow import Merrow
from caislean_gaofar.entities.monsters.fear_gorta import FearGorta
from caislean_gaofar.entities.monsters.cat_si import CatSi

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
    "banshee": Banshee,
    "leprechaun": Leprechaun,
    "pooka": Pooka,
    "selkie": Selkie,
    "dullahan": Dullahan,
    "changeling": Changeling,
    "clurichaun": Clurichaun,
    "merrow": Merrow,
    "fear_gorta": FearGorta,
    "cat_si": CatSi,
}

__all__ = [
    "BaseMonster",
    "Banshee",
    "Leprechaun",
    "Pooka",
    "Selkie",
    "Dullahan",
    "Changeling",
    "Clurichaun",
    "Merrow",
    "FearGorta",
    "CatSi",
    "ALL_MONSTER_CLASSES",
    "MONSTER_CLASSES",
]
