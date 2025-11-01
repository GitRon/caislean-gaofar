"""Monster class - AI controlled enemy."""

import pygame
from entity import Entity
from grid import Grid
import config


class Monster(Entity):
    """AI-controlled monster enemy."""

    def __init__(self, grid_x: int, grid_y: int):
        """Initialize the monster at the given grid position."""
        super().__init__(
            grid_x=grid_x,
            grid_y=grid_y,
            size=config.MONSTER_SIZE,
            color=config.RED,
            max_health=config.MONSTER_MAX_HEALTH,
            speed=config.MONSTER_SPEED,
            attack_damage=config.MONSTER_ATTACK_DAMAGE,
            attack_cooldown=config.MONSTER_ATTACK_COOLDOWN
        )

    def execute_turn(self, target: Entity):
        """
        Execute one turn of monster AI behavior.

        Args:
            target: The entity to chase/attack (usually the warrior)
        """
        if not self.is_alive or not target.is_alive:
            return

        distance = self.grid_distance_to(target)

        # Check if target is in chase range
        if distance <= config.MONSTER_CHASE_RANGE:
            # Check if in attack range
            if distance <= config.MONSTER_ATTACK_RANGE:
                # Try to attack
                self.attack(target)
            else:
                # Move towards target (one tile at a time)
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
        """Draw the monster with special styling."""
        # Draw the entity
        super().draw(screen)

        # Draw eyes to make it look like a monster
        eye_size = 6
        left_eye_x = int(self.x + self.size * 0.3)
        right_eye_x = int(self.x + self.size * 0.7)
        eye_y = int(self.y + self.size * 0.3)

        pygame.draw.circle(screen, config.YELLOW, (left_eye_x, eye_y), eye_size)
        pygame.draw.circle(screen, config.YELLOW, (right_eye_x, eye_y), eye_size)
        pygame.draw.circle(screen, config.BLACK, (left_eye_x, eye_y), eye_size // 2)
        pygame.draw.circle(screen, config.BLACK, (right_eye_x, eye_y), eye_size // 2)
