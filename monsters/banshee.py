"""Banshee monster - wailing spirit with ranged attacks."""

import config
from monsters.base_monster import BaseMonster


class Banshee(BaseMonster):
    """
    Banshee (Bean Sí) - A female spirit who wails to foretell death.

    Special traits:
    - Can attack from 2 tiles away (ranged wail)
    - Medium health, moderate damage
    - Ghostly appearance with floating animation
    """

    def __init__(self, grid_x: int, grid_y: int):
        """Initialize the Banshee."""
        stats = config.MONSTER_STATS[config.MONSTER_TYPE_BANSHEE]
        super().__init__(grid_x, grid_y, config.MONSTER_TYPE_BANSHEE, stats)

    # Future: Can override execute_turn() for unique behavior
    # For example: teleport, fear effects, wailing that affects multiple tiles, etc.
