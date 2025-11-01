"""Leprechaun monster - fast and tricky fairy."""

import config
from monsters.base_monster import BaseMonster


class Leprechaun(BaseMonster):
    """
    Leprechaun - A small, mischievous fairy known for tricks.

    Special traits:
    - Very fast (speed 2)
    - Low health and damage
    - Short chase range (guards his gold)
    - Green appearance with bouncing animation
    """

    def __init__(self, grid_x: int, grid_y: int):
        """Initialize the Leprechaun."""
        stats = config.MONSTER_STATS[config.MONSTER_TYPE_LEPRECHAUN]
        super().__init__(grid_x, grid_y, config.MONSTER_TYPE_LEPRECHAUN, stats)

    # Future: Can override execute_turn() for unique behavior
    # For example: teleport away when hit, leave gold traps, confusion effects, etc.
