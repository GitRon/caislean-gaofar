"""Base entity class for game objects."""

import pygame
from typing import Tuple
import config
from grid import Grid


class Entity:
    """Base class for all game entities (warriors, monsters, etc.)."""

    def __init__(self, grid_x: int, grid_y: int, size: int, color: Tuple[int, int, int],
                 max_health: int, speed: int, attack_damage: int, attack_cooldown: int):
        """
        Initialize an entity.

        Args:
            grid_x: Initial grid x position
            grid_y: Initial grid y position
            size: Size of the entity (square)
            color: RGB color tuple
            max_health: Maximum health points
            speed: Movement speed in tiles per turn
            attack_damage: Damage dealt per attack
            attack_cooldown: Turns between attacks
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size = size
        self.color = color
        self.max_health = max_health
        self.health = max_health
        self.speed = speed
        self.attack_damage = attack_damage
        self.attack_cooldown = attack_cooldown
        self.turns_since_last_attack = attack_cooldown  # Can attack immediately
        self.is_alive = True

    @property
    def x(self) -> int:
        """Get pixel x coordinate."""
        return self.grid_x * config.TILE_SIZE

    @property
    def y(self) -> int:
        """Get pixel y coordinate."""
        return self.grid_y * config.TILE_SIZE

    def get_rect(self) -> pygame.Rect:
        """Get the entity's rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def get_center(self) -> Tuple[float, float]:
        """Get the center position of the entity in pixels."""
        return (self.x + self.size / 2, self.y + self.size / 2)

    def grid_distance_to(self, other: 'Entity') -> int:
        """Calculate Manhattan distance to another entity in tiles."""
        return Grid.manhattan_distance(self.grid_x, self.grid_y,
                                      other.grid_x, other.grid_y)

    def can_attack(self) -> bool:
        """Check if entity can attack based on turn cooldown."""
        return self.turns_since_last_attack >= self.attack_cooldown

    def attack(self, target: 'Entity') -> bool:
        """
        Attempt to attack a target.

        Returns:
            True if attack was successful, False otherwise
        """
        if not self.can_attack():
            return False

        target.take_damage(self.attack_damage)
        self.turns_since_last_attack = 0
        return True

    def take_damage(self, damage: int):
        """Take damage and update health."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False

    def move(self, dx: int, dy: int) -> bool:
        """
        Move the entity by delta grid tiles.

        Args:
            dx: Delta x in tiles
            dy: Delta y in tiles

        Returns:
            True if move was successful, False if blocked
        """
        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy

        # Check if new position is valid
        if Grid.is_valid_position(new_grid_x, new_grid_y):
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y
            return True
        return False

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

    def on_turn_start(self):
        """Called at the start of the entity's turn."""
        self.turns_since_last_attack += 1

    def update(self):
        """Update entity state. Override in subclasses."""
        pass
