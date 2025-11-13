"""Temple class for healing in town."""

import pygame
import math
from caislean_gaofar.core import config


class Temple:
    """Represents a healing temple on the game map."""

    def __init__(self, grid_x: int, grid_y: int):
        """
        Initialize a temple at the given grid position.

        Args:
            grid_x: Grid x position
            grid_y: Grid y position
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.animation_time = 0.0  # For animation effect
        self.x = grid_x * config.TILE_SIZE
        self.y = grid_y * config.TILE_SIZE
        self.size = config.TILE_SIZE
        self.healing_active = False  # Track if currently healing
        self.healing_effect_time = 0.0  # Duration of healing visual effect

    def update(self, dt: float):
        """
        Update temple animation.

        Args:
            dt: Delta time since last update
        """
        self.animation_time += dt

        # Update healing effect
        if self.healing_effect_time > 0:
            self.healing_effect_time -= dt
            if self.healing_effect_time <= 0:
                self.healing_active = False

    def activate_healing(self):
        """Activate the healing visual effect."""
        self.healing_active = True
        self.healing_effect_time = 1.0  # 1 second healing effect

    def draw(self, screen: pygame.Surface):
        """
        Draw the temple with a classical architecture design.

        Args:
            screen: Pygame surface to draw on
        """
        # Update position based on grid coordinates
        self.x = self.grid_x * config.TILE_SIZE
        self.y = self.grid_y * config.TILE_SIZE

        # Temple color scheme - white marble with gold accents
        marble_color = (240, 240, 240)
        gold_color = (255, 215, 0)
        shadow_color = (180, 180, 180)

        # Base platform (3 steps)
        step_height = 3
        for i in range(3):
            step_width = self.size - (i * 4)
            step_x = self.x + (i * 2)
            step_y = self.y + self.size - (3 - i) * step_height - 15
            pygame.draw.rect(
                screen, shadow_color, (step_x, step_y, step_width, step_height)
            )

        # Main temple floor
        floor_y = self.y + self.size - 15
        pygame.draw.rect(screen, marble_color, (self.x + 6, floor_y, self.size - 12, 8))

        # Draw 4 columns
        column_width = 6
        column_height = 20
        column_positions = [self.x + 10, self.x + 18, self.x + 26, self.x + 34]

        for col_x in column_positions:
            # Column shadow
            pygame.draw.rect(
                screen,
                shadow_color,
                (col_x + 1, floor_y - column_height + 1, column_width, column_height),
            )
            # Column
            pygame.draw.rect(
                screen,
                marble_color,
                (col_x, floor_y - column_height, column_width, column_height),
            )
            # Column capital (top decoration)
            pygame.draw.rect(
                screen,
                gold_color,
                (col_x - 1, floor_y - column_height, column_width + 2, 3),
            )

        # Roof (triangular pediment)
        roof_top_y = floor_y - column_height - 8
        roof_points = [
            (self.x + self.size // 2, roof_top_y),  # Top point
            (self.x + 8, floor_y - column_height),  # Bottom left
            (self.x + self.size - 8, floor_y - column_height),  # Bottom right
        ]
        pygame.draw.polygon(screen, gold_color, roof_points)
        pygame.draw.polygon(screen, shadow_color, roof_points, 2)

        # Draw healing glow effect when active
        if self.healing_active:
            center_x = self.x + self.size // 2
            center_y = self.y + self.size // 2

            # Pulsing glow effect
            pulse = abs(math.sin(self.animation_time * 4))
            glow_radius = int(self.size * 0.6 * (1 + pulse * 0.3))

            # Multiple glow layers for soft effect
            for i in range(3):
                alpha_value = int(100 * (1 - i / 3) * pulse)
                radius = glow_radius - (i * 8)
                # Create surface with per-pixel alpha
                glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                glow_color = (50, 255, 50, alpha_value)  # Green healing glow
                pygame.draw.circle(glow_surface, glow_color, (radius, radius), radius)
                screen.blit(glow_surface, (center_x - radius, center_y - radius))

        # Draw healing cross symbol in the center
        cross_color = (255, 100, 100) if self.healing_active else (200, 50, 50)
        center_x = self.x + self.size // 2
        center_y = floor_y - 5

        # Vertical bar of cross
        pygame.draw.rect(screen, cross_color, (center_x - 2, center_y - 6, 4, 12))
        # Horizontal bar of cross
        pygame.draw.rect(screen, cross_color, (center_x - 5, center_y - 2, 10, 4))

        # Draw label below temple
        font = pygame.font.Font(None, 18)
        label_text = "Temple"
        text_surface = font.render(label_text, True, (255, 255, 255))

        # Add subtle shadow to text
        shadow_surface = font.render(label_text, True, (50, 50, 50))
        text_rect = text_surface.get_rect(center=(center_x + 1, self.y + self.size + 9))
        screen.blit(shadow_surface, text_rect)

        text_rect = text_surface.get_rect(center=(center_x, self.y + self.size + 8))
        screen.blit(text_surface, text_rect)
