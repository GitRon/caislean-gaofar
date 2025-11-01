"""Fear Gorta monster - spirit of hunger."""

import config
from monsters.base_monster import BaseMonster


class FearGorta(BaseMonster):
    """
    Fear Gorta - A spirit of hunger appearing as a starving beggar.

    Special traits:
    - Emaciated, skeletal appearance
    - Drains vitality from enemies
    - Moderate health and damage
    - Those who defeat him may be rewarded (future feature)
    """

    def __init__(self, grid_x: int, grid_y: int):
        """Initialize the Fear Gorta."""
        stats = config.MONSTER_STATS[config.MONSTER_TYPE_FEAR_GORTA]
        super().__init__(grid_x, grid_y, config.MONSTER_TYPE_FEAR_GORTA, stats)

    # Future: Can override execute_turn() for unique behavior
    # For example: life drain attacks, weaken player over time, hunger aura,
    # reward good fortune if player "feeds" him, etc.
