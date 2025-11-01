"""Merrow monster - Irish sea being similar to mermaid."""

import config
from monsters.base_monster import BaseMonster


class Merrow(BaseMonster):
    """
    Merrow (Muir Óg / Muirgen) - Irish sea being similar to mermaids.

    Special traits:
    - Moderate health and damage
    - Beautiful appearance with flowing movements
    - Water-themed creature
    """

    def __init__(self, grid_x: int, grid_y: int):
        """Initialize the Merrow."""
        stats = config.MONSTER_STATS[config.MONSTER_TYPE_MERROW]
        super().__init__(grid_x, grid_y, config.MONSTER_TYPE_MERROW, stats)

    # Future: Can override execute_turn() for unique behavior
    # For example: charm/enchant player, create water hazards, sing to confuse,
    # call sea creatures for help, etc.
