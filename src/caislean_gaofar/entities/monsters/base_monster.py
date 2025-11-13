"""Base Monster class - shared logic for all monster types."""

import pygame
from entity import Entity
import config


class BaseMonster(Entity):
    """
    Base class for all monsters with shared AI and rendering logic.

    Subclasses should define class attributes for their stats:
    - HEALTH: Maximum health points
    - ATTACK_DAMAGE: Damage dealt per attack
    - SPEED: Movement speed in tiles per turn
    - CHASE_RANGE: How far (in tiles) the monster will pursue
    - ATTACK_RANGE: How far (in tiles) the monster can attack
    - DESCRIPTION: Short description of monster traits
    - MONSTER_TYPE: String identifier for rendering
    """

    # Default stats (should be overridden by subclasses)
    HEALTH = 50
    ATTACK_DAMAGE = 10
    SPEED = 1
    CHASE_RANGE = 5
    ATTACK_RANGE = 1
    DESCRIPTION = "Unknown creature"
    MONSTER_TYPE = "banshee"  # Default fallback
    XP_VALUE = 50  # Experience points awarded when defeated

    def __init__(self, grid_x: int, grid_y: int):
        """
        Initialize the base monster.

        Args:
            grid_x: Grid X position
            grid_y: Grid Y position
        """
        super().__init__(
            grid_x=grid_x,
            grid_y=grid_y,
            size=config.MONSTER_SIZE,
            color=config.RED,
            max_health=self.HEALTH,
            speed=self.SPEED,
            attack_damage=self.ATTACK_DAMAGE,
            attack_cooldown=config.MONSTER_ATTACK_COOLDOWN,
        )
        self.monster_type = self.MONSTER_TYPE
        self.chase_range = self.CHASE_RANGE
        self.attack_range = self.ATTACK_RANGE
        self.description = self.DESCRIPTION
        self.xp_value = self.XP_VALUE
        self.frame_count = 0  # For animation

    def execute_turn(self, target: Entity, world_map=None):
        """
        Execute one turn of monster AI behavior.

        Default behavior: chase and attack when in range.
        Subclasses can override this for unique behaviors.

        Args:
            target: The entity to chase/attack (usually the warrior)
            world_map: Optional WorldMap object for movement validation
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
                self._move_towards_target(target, world_map)

    def _move_towards_target(self, target: Entity, world_map=None):
        """
        Move one tile towards the target.

        This is the default pathfinding behavior.
        Subclasses can override for unique movement patterns.

        Args:
            target: The entity to move towards
            world_map: Optional WorldMap object for movement validation
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
            if dx != 0 and not self.move(dx, 0, world_map):
                # If blocked, try vertical
                self.move(0, dy, world_map)
        else:
            # Prioritize vertical movement
            if dy != 0 and not self.move(0, dy, world_map):
                # If blocked, try horizontal
                self.move(dx, 0, world_map)

    def draw(
        self,
        screen: pygame.Surface,
        camera_offset_x: int = 0,
        camera_offset_y: int = 0,
    ):
        """
        Draw the monster using template method pattern.

        This orchestrates the rendering process by calling:
        1. draw_body() - for main body rendering (override in subclasses)
        2. draw_details() - for additional details (override in subclasses)
        3. draw_health_bar() - for health display (inherited from Entity)

        Args:
            screen: The pygame screen surface
            camera_offset_x: Camera offset in grid coordinates (default 0)
            camera_offset_y: Camera offset in grid coordinates (default 0)
        """
        # Increment frame counter for animations
        self.frame_count += 1

        # Calculate screen coordinates with camera offset
        screen_x = self.get_screen_x(camera_offset_x)
        screen_y = self.get_screen_y(camera_offset_y)

        # Calculate center position for rendering
        center_x = int(screen_x + self.size / 2)
        center_y = int(screen_y + self.size / 2)

        # Template method calls (subclasses override these)
        self.draw_body(screen, center_x, center_y)
        self.draw_details(screen, center_x, center_y)

        # Draw health bar on top of custom render
        self.draw_health_bar(screen, camera_offset_x, camera_offset_y)

    def draw_body(self, screen: pygame.Surface, center_x: int, center_y: int):
        """
        Draw the main body of the monster.

        This is a template method that should be overridden by subclasses.
        Default implementation draws a simple rectangle with eyes.

        Args:
            screen: pygame surface to draw on
            center_x: center x position (in screen/pixel coordinates)
            center_y: center y position (in screen/pixel coordinates)
        """
        # Calculate top-left from center for default drawing
        top_left_x = center_x - self.size // 2
        top_left_y = center_y - self.size // 2

        # Fallback to simple rectangle + eyes if not overridden
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(top_left_x, top_left_y, self.size, self.size),
        )

        eye_size = 6
        left_eye_x = int(top_left_x + self.size * 0.3)
        right_eye_x = int(top_left_x + self.size * 0.7)
        eye_y = int(top_left_y + self.size * 0.3)
        pygame.draw.circle(screen, config.YELLOW, (left_eye_x, eye_y), eye_size)
        pygame.draw.circle(screen, config.YELLOW, (right_eye_x, eye_y), eye_size)
        pygame.draw.circle(screen, config.BLACK, (left_eye_x, eye_y), eye_size // 2)
        pygame.draw.circle(screen, config.BLACK, (right_eye_x, eye_y), eye_size // 2)

    def draw_details(self, screen: pygame.Surface, center_x: int, center_y: int):
        """
        Draw additional details on top of the body.

        This is a template method that can be overridden by subclasses
        for effects like auras, glows, particles, etc.

        Default implementation does nothing.

        Args:
            screen: pygame surface to draw on
            center_x: center x position (in screen/pixel coordinates)
            center_y: center y position (in screen/pixel coordinates)
        """
        pass  # Subclasses can override to add details
