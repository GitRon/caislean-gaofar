"""Dullahan monster - headless rider, omen of death."""

import config
from monsters.base_monster import BaseMonster


class Dullahan(BaseMonster):
    """
    Dullahan - A headless rider who carries his own head.

    Special traits:
    - Highest health (120 HP)
    - Highest damage (20)
    - Wide chase range (omen of death)
    - BOSS-level difficulty
    """

    def __init__(self, grid_x: int, grid_y: int):
        """Initialize the Dullahan."""
        stats = config.MONSTER_STATS[config.MONSTER_TYPE_DULLAHAN]
        super().__init__(grid_x, grid_y, config.MONSTER_TYPE_DULLAHAN, stats)

    # Future: Can override execute_turn() for unique behavior
    # For example: death mark on player, summon lesser undead, charge attacks,
    # instant kill below certain HP threshold, etc.
