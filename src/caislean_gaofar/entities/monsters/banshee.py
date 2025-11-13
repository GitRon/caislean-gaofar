"""Banshee monster - wailing spirit with ranged attacks."""

from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class Banshee(BaseMonster):
    """
    Banshee (Bean Sí) - A female spirit who wails to foretell death.

    Special traits:
    - Can attack from 2 tiles away (ranged wail)
    - Medium health, moderate damage
    - Ghostly appearance with floating animation
    """

    # Monster stats
    HEALTH = 60
    ATTACK_DAMAGE = 12
    SPEED = 1
    CHASE_RANGE = 6
    ATTACK_RANGE = 2  # Can wail from a distance
    DESCRIPTION = "Ghostly spirit - fast, ranged attacks"
    MONSTER_TYPE = "banshee"

    # Future: Can override execute_turn() for unique behavior
    # For example: teleport, fear effects, wailing that affects multiple tiles, etc.
