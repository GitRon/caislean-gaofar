"""Base Monster class - shared logic for all monster types."""

import pygame
from entity import Entity
from grid import Grid
import config
from monster_renderer import MONSTER_RENDERERS


class BaseMonster(Entity):
    """
    Base class for all monsters with shared AI and rendering logic.

    Subclasses should override execute_turn() for unique behaviors.
    """

    def __init__(self, grid_x: int, grid_y: int, monster_type: str, stats: dict):
        """
        Initialize the base monster.

        Args:
            grid_x: Grid X position
            grid_y: Grid Y position
            monster_type: Type of monster (for rendering)
            stats: Dictionary with health, attack_damage, speed, chase_range, attack_range, description
        """
        super().__init__(
            grid_x=grid_x,
            grid_y=grid_y,
            size=config.MONSTER_SIZE,
            color=config.RED,
            max_health=stats['health'],
            speed=stats['speed'],
            attack_damage=stats['attack_damage'],
            attack_cooldown=config.MONSTER_ATTACK_COOLDOWN
        )
        self.monster_type = monster_type
        self.chase_range = stats['chase_range']
        self.attack_range = stats['attack_range']
        self.description = stats['description']
        self.frame_count = 0  # For animation

    def execute_turn(self, target: Entity):
        """
        Execute one turn of monster AI behavior.

        Default behavior: chase and attack when in range.
        Subclasses can override this for unique behaviors.

        Args:
            target: The entity to chase/attack (usually the warrior)
        """
        if not self.is_alive or not target.is_alive:
            return

        distance = self.grid_distance_to(target)

        # Check if target is in chase range
        if distance <= self.chase_range:
            # Check if in attack range
            if distance <= self.attack_range:
                # Try to attack
                self.attack(target)
            else:
                # Move towards target
                self._move_towards_target(target)

    def _move_towards_target(self, target: Entity):
        """
        Move one tile towards the target.

        This is the default pathfinding behavior.
        Subclasses can override for unique movement patterns.

        Args:
            target: The entity to move towards
        """
        dx = 0
        dy = 0

        if target.grid_x < self.grid_x:
            dx = -1
        elif target.grid_x > self.grid_x:
            dx = 1

        if target.grid_y < self.grid_y:
            dy = -1
        elif target.grid_y > self.grid_y:
            dy = 1

        # Try to move (prioritize direction with larger distance)
        if abs(target.grid_x - self.grid_x) > abs(target.grid_y - self.grid_y):
            # Prioritize horizontal movement
            if dx != 0 and not self.move(dx, 0):
                # If blocked, try vertical
                self.move(0, dy)
        else:
            # Prioritize vertical movement
            if dy != 0 and not self.move(0, dy):
                # If blocked, try horizontal
                self.move(dx, 0)

    def draw(self, screen: pygame.Surface):
        """Draw the monster using its specific renderer."""
        # Increment frame counter for animations
        self.frame_count += 1

        # Get the appropriate rendering function for this monster type
        renderer = MONSTER_RENDERERS.get(self.monster_type)

        if renderer:
            # Use custom renderer - pass center position of entity
            center_x = int(self.x + self.size / 2)
            center_y = int(self.y + self.size / 2)
            renderer(screen, center_x, center_y, self.size, self.frame_count)
        else:
            # Fallback to original simple rectangle + eyes if type not found
            super().draw(screen)
            eye_size = 6
            left_eye_x = int(self.x + self.size * 0.3)
            right_eye_x = int(self.x + self.size * 0.7)
            eye_y = int(self.y + self.size * 0.3)
            pygame.draw.circle(screen, config.YELLOW, (left_eye_x, eye_y), eye_size)
            pygame.draw.circle(screen, config.YELLOW, (right_eye_x, eye_y), eye_size)
            pygame.draw.circle(screen, config.BLACK, (left_eye_x, eye_y), eye_size // 2)
            pygame.draw.circle(screen, config.BLACK, (right_eye_x, eye_y), eye_size // 2)

        # Draw health bar on top of custom render
        self.draw_health_bar(screen)
