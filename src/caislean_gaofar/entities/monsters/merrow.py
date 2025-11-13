"""Merrow monster - Irish sea being similar to mermaid."""

from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class Merrow(BaseMonster):
    """
    Merrow (Muir Óg / Muirgen) - Irish sea being similar to mermaids.

    Special traits:
    - Moderate health and damage
    - Beautiful appearance with flowing movements
    - Water-themed creature
    """

    # Monster stats
    HEALTH = 75
    ATTACK_DAMAGE = 11
    SPEED = 1
    CHASE_RANGE = 5
    ATTACK_RANGE = 1
    DESCRIPTION = "Sea being - moderate threat"
    MONSTER_TYPE = "merrow"

    # Future: Can override execute_turn() for unique behavior
    # For example: charm/enchant player, create water hazards, sing to confuse,
    # call sea creatures for help, etc.
