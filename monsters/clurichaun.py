"""Clurichaun monster - drunk cousin of leprechaun."""

import config
from monsters.base_monster import BaseMonster


class Clurichaun(BaseMonster):
    """
    Clurichaun - Related to leprechaun but fond of drinking wine.

    Special traits:
    - Low health and damage
    - Short chase range (guards wine cellars)
    - Unpredictable due to drunkenness
    - Red coat with wine bottle
    """

    def __init__(self, grid_x: int, grid_y: int):
        """Initialize the Clurichaun."""
        stats = config.MONSTER_STATS[config.MONSTER_TYPE_CLURICHAUN]
        super().__init__(grid_x, grid_y, config.MONSTER_TYPE_CLURICHAUN, stats)

    # Future: Can override execute_turn() for unique behavior
    # For example: random movement (drunk), throw wine bottles, berserker rage,
    # sleep randomly, defensive territory behavior, etc.
