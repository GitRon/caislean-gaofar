"""Combat system for handling attacks between entities."""

import pygame
from caislean_gaofar.entities.entity import Entity
from caislean_gaofar.core import config


class CombatSystem:
    """Manages combat interactions between entities."""

    @staticmethod
    def is_in_attack_range(entity1: Entity, entity2: Entity) -> bool:
        """
        Check if entity1 is in attack range of entity2.

        Args:
            entity1: The attacking entity
            entity2: The target entity

        Returns:
            True if in attack range, False otherwise
        """
        distance = entity1.grid_distance_to(entity2)
        # Check if entity1 has an attack_range attribute (monsters have this)
        if hasattr(entity1, "attack_range"):
            return distance <= entity1.attack_range
        # Default to melee range (1 tile) for warriors and other entities
        return distance <= 1

    @staticmethod
    def draw_combat_ui(screen: pygame.Surface, warrior: Entity, monster: Entity):
        """
        Draw combat-related UI elements.

        Args:
            screen: Pygame surface to draw on
            warrior: The warrior entity
            monster: The monster entity
        """
        # UI has been moved to HUD - this method kept for compatibility
        pass

    @staticmethod
    def draw_attack_range_indicator(
        screen: pygame.Surface, warrior: Entity, monster: Entity
    ):
        """
        Draw a visual indicator showing if warrior is in attack range.

        Args:
            screen: Pygame surface to draw on
            warrior: The warrior entity
            monster: The monster entity
        """
        if CombatSystem.is_in_attack_range(warrior, monster):
            # Draw line connecting entities when in range
            warrior_center = warrior.get_center()
            monster_center = monster.get_center()

            pygame.draw.line(screen, config.YELLOW, warrior_center, monster_center, 2)
