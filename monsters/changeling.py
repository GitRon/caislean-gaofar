"""Changeling monster - fairy child left in place of human baby."""

import config
from monsters.base_monster import BaseMonster


class Changeling(BaseMonster):
    """
    Changeling - A fairy child secretly left in place of a human baby.

    Special traits:
    - Deceptively dangerous
    - Twitchy, unsettling movements
    - Moderate health and damage
    - Child-like appearance with disturbing features
    """

    def __init__(self, grid_x: int, grid_y: int):
        """Initialize the Changeling."""
        stats = config.MONSTER_STATS[config.MONSTER_TYPE_CHANGELING]
        super().__init__(grid_x, grid_y, config.MONSTER_TYPE_CHANGELING, stats)

    # Future: Can override execute_turn() for unique behavior
    # For example: confuse player controls, summon fairy allies, steal items,
    # mimic player appearance, etc.
