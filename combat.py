"""Combat system for handling attacks between entities."""

import pygame
from entity import Entity
import config


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
        font = pygame.font.Font(None, 36)

        # Draw warrior stats
        warrior_text = font.render(
            f"Warrior HP: {warrior.health}/{warrior.max_health}", True, config.WHITE
        )
        screen.blit(warrior_text, (10, 10))

        # Draw monster stats with type
        if hasattr(monster, "monster_type"):
            # Format monster type name nicely (capitalize and replace underscores)
            monster_name = monster.monster_type.replace("_", " ").title()
            monster_text = font.render(
                f"{monster_name}: {monster.health}/{monster.max_health}",
                True,
                config.WHITE,
            )
            screen.blit(monster_text, (10, 50))

            # Draw monster description
            if hasattr(monster, "description"):
                desc_font = pygame.font.Font(None, 20)
                desc_text = desc_font.render(monster.description, True, config.GRAY)
                screen.blit(desc_text, (10, 85))
        else:
            monster_text = font.render(
                f"Monster HP: {monster.health}/{monster.max_health}", True, config.WHITE
            )
            screen.blit(monster_text, (10, 50))

        # Draw controls hint
        small_font = pygame.font.Font(None, 24)
        controls = [
            "Controls:",
            "WASD/Arrows - Move",
            "SPACE - Attack",
            "I - Inventory",
        ]

        for i, control in enumerate(controls):
            text = small_font.render(control, True, config.GRAY)
            screen.blit(text, (config.SCREEN_WIDTH - 220, 10 + i * 25))

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
