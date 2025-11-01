"""Combat system for handling attacks between entities."""

import pygame
from entity import Entity
import config


class CombatSystem:
    """Manages combat interactions between entities."""

    @staticmethod
    def check_attack_input(warrior: Entity, monster: Entity, current_time: int) -> bool:
        """
        Check if player wants to attack and process it.

        Args:
            warrior: The warrior entity
            monster: The monster entity
            current_time: Current game time in milliseconds

        Returns:
            True if attack was executed, False otherwise
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            # Check if warrior is in range to attack
            distance = warrior.distance_to(monster)

            if distance <= config.MONSTER_ATTACK_RANGE and warrior.can_attack(current_time):
                warrior.attack(monster, current_time)
                return True

        return False

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
        warrior_text = font.render(f"Warrior HP: {warrior.health}/{warrior.max_health}", True, config.WHITE)
        screen.blit(warrior_text, (10, 10))

        # Draw monster stats
        monster_text = font.render(f"Monster HP: {monster.health}/{monster.max_health}", True, config.WHITE)
        screen.blit(monster_text, (10, 50))

        # Draw controls hint
        small_font = pygame.font.Font(None, 24)
        controls = [
            "Controls:",
            "WASD/Arrows - Move",
            "SPACE - Attack (when close)",
            "I - Inventory"
        ]

        for i, control in enumerate(controls):
            text = small_font.render(control, True, config.GRAY)
            screen.blit(text, (config.SCREEN_WIDTH - 250, 10 + i * 25))

    @staticmethod
    def draw_attack_range_indicator(screen: pygame.Surface, warrior: Entity, monster: Entity):
        """
        Draw a visual indicator showing if warrior is in attack range.

        Args:
            screen: Pygame surface to draw on
            warrior: The warrior entity
            monster: The monster entity
        """
        distance = warrior.distance_to(monster)

        if distance <= config.MONSTER_ATTACK_RANGE:
            # Draw line connecting entities when in range
            warrior_center = warrior.get_center()
            monster_center = monster.get_center()

            pygame.draw.line(screen, config.YELLOW,
                           warrior_center, monster_center, 2)
