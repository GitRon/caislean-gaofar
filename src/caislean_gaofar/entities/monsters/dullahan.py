"""Dullahan monster - headless rider, omen of death."""

from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class Dullahan(BaseMonster):
    """
    Dullahan - A headless rider who carries his own head.

    Special traits:
    - Highest health (120 HP)
    - Highest damage (20)
    - Wide chase range (omen of death)
    - BOSS-level difficulty
    """

    # Monster stats
    HEALTH = 120
    ATTACK_DAMAGE = 20
    SPEED = 1
    CHASE_RANGE = 8  # Omen of death, wide chase range
    ATTACK_RANGE = 1
    DESCRIPTION = "Headless rider - very powerful, deadly"
    MONSTER_TYPE = "dullahan"

    # Future: Can override execute_turn() for unique behavior
    # For example: death mark on player, summon lesser undead, charge attacks,
    # instant kill below certain HP threshold, etc.
