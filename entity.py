"""Base entity class for game objects."""

import pygame
from typing import Tuple
import config


class Entity:
    """Base class for all game entities (warriors, monsters, etc.)."""

    def __init__(self, x: float, y: float, size: int, color: Tuple[int, int, int],
                 max_health: int, speed: float, attack_damage: int, attack_cooldown: int):
        """
        Initialize an entity.

        Args:
            x: Initial x position
            y: Initial y position
            size: Size of the entity (square)
            color: RGB color tuple
            max_health: Maximum health points
            speed: Movement speed
            attack_damage: Damage dealt per attack
            attack_cooldown: Milliseconds between attacks
        """
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.max_health = max_health
        self.health = max_health
        self.speed = speed
        self.attack_damage = attack_damage
        self.attack_cooldown = attack_cooldown
        self.last_attack_time = 0
        self.is_alive = True

    def get_rect(self) -> pygame.Rect:
        """Get the entity's rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def get_center(self) -> Tuple[float, float]:
        """Get the center position of the entity."""
        return (self.x + self.size / 2, self.y + self.size / 2)

    def distance_to(self, other: 'Entity') -> float:
        """Calculate distance to another entity."""
        self_center = self.get_center()
        other_center = other.get_center()
        dx = self_center[0] - other_center[0]
        dy = self_center[1] - other_center[1]
        return (dx ** 2 + dy ** 2) ** 0.5

    def can_attack(self, current_time: int) -> bool:
        """Check if entity can attack based on cooldown."""
        return current_time - self.last_attack_time >= self.attack_cooldown

    def attack(self, target: 'Entity', current_time: int) -> bool:
        """
        Attempt to attack a target.

        Returns:
            True if attack was successful, False otherwise
        """
        if not self.can_attack(current_time):
            return False

        target.take_damage(self.attack_damage)
        self.last_attack_time = current_time
        return True

    def take_damage(self, damage: int):
        """Take damage and update health."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False

    def move(self, dx: float, dy: float):
        """Move the entity by delta x and y."""
        self.x += dx
        self.y += dy

        # Keep entity within screen bounds
        self.x = max(0, min(self.x, config.SCREEN_WIDTH - self.size))
        self.y = max(0, min(self.y, config.SCREEN_HEIGHT - self.size))

    def draw(self, screen: pygame.Surface):
        """Draw the entity on the screen."""
        # Draw entity
        pygame.draw.rect(screen, self.color, self.get_rect())

        # Draw health bar
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen: pygame.Surface):
        """Draw health bar above the entity."""
        bar_width = self.size
        bar_height = 5
        bar_x = self.x
        bar_y = self.y - 10

        # Background (red)
        pygame.draw.rect(screen, config.DARK_RED, (bar_x, bar_y, bar_width, bar_height))

        # Health (green)
        health_ratio = self.health / self.max_health
        health_width = bar_width * health_ratio
        pygame.draw.rect(screen, config.DARK_GREEN, (bar_x, bar_y, health_width, bar_height))

        # Border
        pygame.draw.rect(screen, config.WHITE, (bar_x, bar_y, bar_width, bar_height), 1)

    def update(self, dt: float):
        """Update entity state. Override in subclasses."""
        pass
