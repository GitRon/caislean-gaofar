"""Portal class for town portal visual representation."""

import pygame
import math
import config


class Portal:
    """Represents a visible portal on the game map."""

    def __init__(self, grid_x: int, grid_y: int, is_return_portal: bool = False):
        """
        Initialize a portal at the given grid position.

        Args:
            grid_x: Grid x position
            grid_y: Grid y position
            is_return_portal: True if this is a return portal in town
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.is_return_portal = is_return_portal
        self.animation_time = 0.0  # For animation effect
        self.x = grid_x * config.TILE_SIZE
        self.y = grid_y * config.TILE_SIZE
        self.size = config.TILE_SIZE

    def update(self, dt: float):
        """
        Update portal animation.

        Args:
            dt: Delta time since last update
        """
        self.animation_time += dt

    def draw(self, screen: pygame.Surface):
        """
        Draw the portal with a glowing swirling effect.

        Args:
            screen: Pygame surface to draw on
        """
        # Update position based on grid coordinates
        self.x = self.grid_x * config.TILE_SIZE
        self.y = self.grid_y * config.TILE_SIZE

        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2

        # Calculate pulsing effect
        pulse = abs(math.sin(self.animation_time * 2))

        # Draw multiple circles for depth effect
        max_radius = int(self.size * 0.45)

        # Outer glow
        outer_radius = int(max_radius * (1 + pulse * 0.2))
        glow_color = (
            int(config.PORTAL_GLOW[0] * (0.5 + pulse * 0.5)),
            int(config.PORTAL_GLOW[1] * (0.5 + pulse * 0.5)),
            int(config.PORTAL_GLOW[2] * (0.5 + pulse * 0.5)),
        )
        pygame.draw.circle(screen, glow_color, (center_x, center_y), outer_radius, 3)

        # Middle ring
        middle_radius = int(max_radius * 0.75)
        pygame.draw.circle(
            screen, config.PORTAL_COLOR, (center_x, center_y), middle_radius, 2
        )

        # Inner swirl (simplified as circles)
        inner_radius = int(max_radius * 0.5)
        inner_color = (
            min(255, config.PORTAL_COLOR[0] + 50),
            min(255, config.PORTAL_COLOR[1] + 50),
            min(255, config.PORTAL_COLOR[2] + 50),
        )
        pygame.draw.circle(screen, inner_color, (center_x, center_y), inner_radius)

        # Draw swirl effect with rotating lines
        num_swirls = 6
        for i in range(num_swirls):
            angle = (self.animation_time * 2 + i * (2 * math.pi / num_swirls)) % (
                2 * math.pi
            )
            start_x = center_x + int(inner_radius * 0.5 * math.cos(angle))
            start_y = center_y + int(inner_radius * 0.5 * math.sin(angle))
            end_x = center_x + int(max_radius * 0.7 * math.cos(angle))
            end_y = center_y + int(max_radius * 0.7 * math.sin(angle))
            pygame.draw.line(
                screen,
                config.PORTAL_GLOW,
                (start_x, start_y),
                (end_x, end_y),
                2,
            )

        # Add central core
        core_radius = int(max_radius * 0.2 * (1 + pulse * 0.3))
        core_color = (255, 255, 255)  # Bright white center
        pygame.draw.circle(screen, core_color, (center_x, center_y), core_radius)

        # Draw label below portal
        font = pygame.font.Font(None, 20)
        label = "Return Portal" if self.is_return_portal else "Town Portal"
        text_surface = font.render(label, True, config.WHITE)
        text_rect = text_surface.get_rect(center=(center_x, self.y + self.size + 10))
        screen.blit(text_surface, text_rect)
