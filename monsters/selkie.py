"""Selkie monster - seal that transforms to human."""

import config
from monsters.base_monster import BaseMonster


class Selkie(BaseMonster):
    """
    Selkie - A seal that can shed its skin to live as a human.

    Special traits:
    - Balanced stats
    - Water-themed abilities
    - Seal-human hybrid appearance with swimming motion
    """

    def __init__(self, grid_x: int, grid_y: int):
        """Initialize the Selkie."""
        stats = config.MONSTER_STATS[config.MONSTER_TYPE_SELKIE]
        super().__init__(grid_x, grid_y, config.MONSTER_TYPE_SELKIE, stats)

    # Future: Can override execute_turn() for unique behavior
    # For example: transform between seal/human forms, water pools that slow player,
    # healing when near water, etc.
