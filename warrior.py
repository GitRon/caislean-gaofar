"""Warrior class - player controlled character."""

import pygame
from entity import Entity
from inventory import Inventory
import config


class Warrior(Entity):
    """Player-controlled warrior character."""

    def __init__(self, x: float, y: float):
        """Initialize the warrior at the given position."""
        super().__init__(
            x=x,
            y=y,
            size=config.WARRIOR_SIZE,
            color=config.BLUE,
            max_health=config.WARRIOR_MAX_HEALTH,
            speed=config.WARRIOR_SPEED,
            attack_damage=config.WARRIOR_ATTACK_DAMAGE,
            attack_cooldown=config.WARRIOR_ATTACK_COOLDOWN
        )
        self.inventory = Inventory()
        self.base_attack_damage = config.WARRIOR_ATTACK_DAMAGE

    def get_effective_attack_damage(self) -> int:
        """Get total attack damage including inventory bonuses."""
        return self.base_attack_damage + self.inventory.get_total_attack_bonus()

    def attack(self, target: 'Entity', current_time: int) -> bool:
        """
        Attempt to attack a target with effective damage.

        Returns:
            True if attack was successful, False otherwise
        """
        if not self.can_attack(current_time):
            return False

        effective_damage = self.get_effective_attack_damage()
        target.take_damage(effective_damage)
        self.last_attack_time = current_time
        return True

    def handle_input(self, keys: pygame.key.ScancodeWrapper):
        """
        Handle player input for movement.

        Args:
            keys: Pygame key state
        """
        dx, dy = 0, 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707

        self.move(dx, dy)

    def draw(self, screen: pygame.Surface):
        """Draw the warrior with special styling."""
        # Draw the entity
        super().draw(screen)

        # Draw a cross pattern to make it look like a warrior
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2

        # Vertical line
        pygame.draw.line(screen, config.WHITE,
                        (center_x, self.y + 5),
                        (center_x, self.y + self.size - 5), 2)

        # Horizontal line
        pygame.draw.line(screen, config.WHITE,
                        (self.x + 5, center_y),
                        (self.x + self.size - 5, center_y), 2)
