"""Clurichaun monster - drunk cousin of leprechaun."""

from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class Clurichaun(BaseMonster):
    """
    Clurichaun - Related to leprechaun but fond of drinking wine.

    Special traits:
    - Low health and damage
    - Short chase range (guards wine cellars)
    - Unpredictable due to drunkenness
    - Red coat with wine bottle
    """

    # Monster stats
    HEALTH = 45
    ATTACK_DAMAGE = 9
    SPEED = 1  # Drunk, slower reactions
    CHASE_RANGE = 3  # Short chase (guards wine cellars)
    ATTACK_RANGE = 1
    DESCRIPTION = "Drunken fairy - weak but unpredictable"
    MONSTER_TYPE = "clurichaun"

    # Future: Can override execute_turn() for unique behavior
    # For example: random movement (drunk), throw wine bottles, berserker rage,
    # sleep randomly, defensive territory behavior, etc.
