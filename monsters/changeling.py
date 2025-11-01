"""Changeling monster - fairy child left in place of human baby."""

from monsters.base_monster import BaseMonster


class Changeling(BaseMonster):
    """
    Changeling - A fairy child secretly left in place of a human baby.

    Special traits:
    - Deceptively dangerous
    - Twitchy, unsettling movements
    - Moderate health and damage
    - Child-like appearance with disturbing features
    """

    # Monster stats
    HEALTH = 50
    ATTACK_DAMAGE = 14
    SPEED = 1
    CHASE_RANGE = 4
    ATTACK_RANGE = 1
    DESCRIPTION = "Fairy child - deceptively dangerous"
    MONSTER_TYPE = "changeling"

    # Future: Can override execute_turn() for unique behavior
    # For example: confuse player controls, summon fairy allies, steal items,
    # mimic player appearance, etc.
