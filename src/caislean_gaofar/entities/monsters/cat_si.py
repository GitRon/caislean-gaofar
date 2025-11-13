"""Cat Sí monster - large black fairy cat that steals souls."""

from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class CatSi(BaseMonster):
    """
    Cat Sí (Cat Sidhe) - A large black fairy cat with white chest spot.

    Special traits:
    - Fast like a cat (speed 2)
    - High damage (16)
    - Steals souls before they pass to afterlife
    - Prowling movements with swishing tail
    """

    # Monster stats
    HEALTH = 65
    ATTACK_DAMAGE = 16
    SPEED = 2  # Fast like a cat
    CHASE_RANGE = 5
    ATTACK_RANGE = 1
    DESCRIPTION = "Fairy cat - fast and deadly"
    MONSTER_TYPE = "cat_si"

    # Future: Can override execute_turn() for unique behavior
    # For example: pounce attacks with extra range, steal player souls/experience,
    # nine lives (multiple deaths), invisibility/stealth, etc.
