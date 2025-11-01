"""Selkie monster - seal that transforms to human."""

from monsters.base_monster import BaseMonster


class Selkie(BaseMonster):
    """
    Selkie - A seal that can shed its skin to live as a human.

    Special traits:
    - Balanced stats
    - Water-themed abilities
    - Seal-human hybrid appearance with swimming motion
    """

    # Monster stats
    HEALTH = 70
    ATTACK_DAMAGE = 10
    SPEED = 1
    CHASE_RANGE = 5
    ATTACK_RANGE = 1
    DESCRIPTION = "Seal-human hybrid - balanced stats"
    MONSTER_TYPE = "selkie"

    # Future: Can override execute_turn() for unique behavior
    # For example: transform between seal/human forms, water pools that slow player,
    # healing when near water, etc.
