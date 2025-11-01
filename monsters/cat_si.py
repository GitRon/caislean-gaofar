"""Cat Sí monster - large black fairy cat that steals souls."""

import config
from monsters.base_monster import BaseMonster


class CatSi(BaseMonster):
    """
    Cat Sí (Cat Sidhe) - A large black fairy cat with white chest spot.

    Special traits:
    - Fast like a cat (speed 2)
    - High damage (16)
    - Steals souls before they pass to afterlife
    - Prowling movements with swishing tail
    """

    def __init__(self, grid_x: int, grid_y: int):
        """Initialize the Cat Sí."""
        stats = config.MONSTER_STATS[config.MONSTER_TYPE_CAT_SI]
        super().__init__(grid_x, grid_y, config.MONSTER_TYPE_CAT_SI, stats)

    # Future: Can override execute_turn() for unique behavior
    # For example: pounce attacks with extra range, steal player souls/experience,
    # nine lives (multiple deaths), invisibility/stealth, etc.
