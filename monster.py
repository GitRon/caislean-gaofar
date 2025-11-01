"""Monster class - AI controlled enemy."""

import pygame
from entity import Entity
import config


class Monster(Entity):
    """AI-controlled monster enemy."""

    def __init__(self, x: float, y: float):
        """Initialize the monster at the given position."""
        super().__init__(
            x=x,
            y=y,
            size=config.MONSTER_SIZE,
            color=config.RED,
            max_health=config.MONSTER_MAX_HEALTH,
            speed=config.MONSTER_SPEED,
            attack_damage=config.MONSTER_ATTACK_DAMAGE,
            attack_cooldown=config.MONSTER_ATTACK_COOLDOWN
        )

    def update(self, dt: float, target: Entity, current_time: int):
        """
        Update monster AI behavior.

        Args:
            dt: Delta time since last update
            target: The entity to chase/attack (usually the warrior)
            current_time: Current game time in milliseconds
        """
        if not self.is_alive or not target.is_alive:
            return

        distance = self.distance_to(target)

        # Check if target is in chase range
        if distance <= config.MONSTER_CHASE_RANGE:
            # Move towards target
            self_center = self.get_center()
            target_center = target.get_center()

            dx = target_center[0] - self_center[0]
            dy = target_center[1] - self_center[1]

            # Normalize direction
            if distance > 0:
                dx /= distance
                dy /= distance

            # Check if in attack range
            if distance <= config.MONSTER_ATTACK_RANGE:
                # Try to attack
                self.attack(target, current_time)
            else:
                # Move towards target
                self.move(dx * self.speed, dy * self.speed)

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
