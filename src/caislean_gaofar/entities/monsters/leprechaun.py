"""Leprechaun monster - fast and tricky fairy."""

from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class Leprechaun(BaseMonster):
    """
    Leprechaun - A small, mischievous fairy known for tricks.

    Special traits:
    - Very fast (speed 2)
    - Low health and damage
    - Short chase range (guards his gold)
    - Green appearance with bouncing animation
    """

    # Monster stats
    HEALTH = 40
    ATTACK_DAMAGE = 8
    SPEED = 2  # Very fast and tricky
    CHASE_RANGE = 4
    ATTACK_RANGE = 1
    DESCRIPTION = "Mischievous fairy - weak but very fast"
    MONSTER_TYPE = "leprechaun"

    # Future: Can override execute_turn() for unique behavior
    # For example: teleport away when hit, leave gold traps, confusion effects, etc.
