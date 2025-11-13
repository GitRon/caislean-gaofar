"""Fear Gorta monster - spirit of hunger."""

from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class FearGorta(BaseMonster):
    """
    Fear Gorta - A spirit of hunger appearing as a starving beggar.

    Special traits:
    - Emaciated, skeletal appearance
    - Drains vitality from enemies
    - Moderate health and damage
    - Those who defeat him may be rewarded (future feature)
    """

    # Monster stats
    HEALTH = 55
    ATTACK_DAMAGE = 13
    SPEED = 1
    CHASE_RANGE = 6
    ATTACK_RANGE = 1
    DESCRIPTION = "Hunger spirit - drains vitality"
    MONSTER_TYPE = "fear_gorta"

    # Future: Can override execute_turn() for unique behavior
    # For example: life drain attacks, weaken player over time, hunger aura,
    # reward good fortune if player "feeds" him, etc.
