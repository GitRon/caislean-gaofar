"""Pooka monster - shape-shifting creature."""

import config
from monsters.base_monster import BaseMonster


class Pooka(BaseMonster):
    """
    Pooka (Púca) - A shape-shifting creature of fortune and mischief.

    Special traits:
    - High health (100 HP)
    - Relentless pursuit (chase range 7)
    - Moderate damage
    - Dark horse form with pulsing shadow aura
    """

    def __init__(self, grid_x: int, grid_y: int):
        """Initialize the Pooka."""
        stats = config.MONSTER_STATS[config.MONSTER_TYPE_POOKA]
        super().__init__(grid_x, grid_y, config.MONSTER_TYPE_POOKA, stats)

    # Future: Can override execute_turn() for unique behavior
    # For example: shape-shift to different forms with different abilities,
    # random teleportation, curse effects, etc.
