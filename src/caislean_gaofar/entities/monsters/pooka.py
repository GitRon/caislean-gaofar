"""Pooka monster - shape-shifting creature."""

from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class Pooka(BaseMonster):
    """
    Pooka (Púca) - A shape-shifting creature of fortune and mischief.

    Special traits:
    - High health (100 HP)
    - Relentless pursuit (chase range 7)
    - Moderate damage
    - Dark horse form with pulsing shadow aura
    """

    # Monster stats
    HEALTH = 100
    ATTACK_DAMAGE = 15
    SPEED = 1
    CHASE_RANGE = 7  # Pursues relentlessly
    ATTACK_RANGE = 1
    DESCRIPTION = "Shape-shifter - high health, relentless pursuit"
    MONSTER_TYPE = "pooka"

    # Future: Can override execute_turn() for unique behavior
    # For example: shape-shift to different forms with different abilities,
    # random teleportation, curse effects, etc.
