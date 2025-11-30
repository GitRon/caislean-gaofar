"""Library class for distributing town portals."""

import pygame
import math
from caislean_gaofar.core import config


class Library:
    """Represents a library building that provides town portals to players."""

    def __init__(self, grid_x: int, grid_y: int):
        """
        Initialize a library at the given grid position.

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
        self.portal_gift_active = False  # Track if currently giving portals
        self.portal_effect_time = 0.0  # Duration of portal gift visual effect

    def update(self, dt: float):
        """
        Update library animation.

        Args:
            dt: Delta time since last update
        """
        self.animation_time += dt

        # Update portal gift effect
        if self.portal_effect_time > 0:
            self.portal_effect_time -= dt
            if self.portal_effect_time <= 0:
                self.portal_gift_active = False

    def activate_portal_gift(self):
        """Activate the portal gift visual effect."""
        self.portal_gift_active = True
        self.portal_effect_time = 1.5  # 1.5 second effect

    def get_screen_x(self, camera_offset_x: int = 0) -> int:
        """
        Get the screen pixel x coordinate with camera offset applied.

        Args:
            camera_offset_x: Camera offset in grid coordinates (default 0)

        Returns:
            Screen pixel x coordinate
        """
        return (self.grid_x - camera_offset_x) * config.TILE_SIZE

    def get_screen_y(self, camera_offset_y: int = 0) -> int:
        """
        Get the screen pixel y coordinate with camera offset applied.

        Args:
            camera_offset_y: Camera offset in grid coordinates (default 0)

        Returns:
            Screen pixel y coordinate
        """
        return (self.grid_y - camera_offset_y) * config.TILE_SIZE

    def draw(
        self,
        screen: pygame.Surface,
        camera_offset_x: int = 0,
        camera_offset_y: int = 0,
    ):
        """
        Draw the library building with a classical design.

        Args:
            screen: Pygame surface to draw on
            camera_offset_x: Camera offset in grid coordinates (default 0)
            camera_offset_y: Camera offset in grid coordinates (default 0)
        """
        # Calculate screen coordinates with camera offset
        screen_x = self.get_screen_x(camera_offset_x)
        screen_y = self.get_screen_y(camera_offset_y)

        # Library color scheme - brown wood and beige pages
        wood_color = (139, 69, 19)
        dark_wood_color = (101, 51, 13)
        book_color = (210, 180, 140)
        accent_color = (184, 134, 11)

        # Base building
        building_height = 35
        building_y = screen_y + self.size - building_height
        pygame.draw.rect(
            screen, wood_color, (screen_x + 5, building_y, self.size - 10, building_height)
        )

        # Door
        door_width = 12
        door_height = 18
        door_x = screen_x + self.size // 2 - door_width // 2
        door_y = screen_y + self.size - door_height
        pygame.draw.rect(
            screen, dark_wood_color, (door_x, door_y, door_width, door_height)
        )

        # Roof
        roof_points = [
            (screen_x + self.size // 2, building_y - 8),  # Top point
            (screen_x + 3, building_y),  # Bottom left
            (screen_x + self.size - 3, building_y),  # Bottom right
        ]
        pygame.draw.polygon(screen, dark_wood_color, roof_points)

        # Windows (book shelves visible through windows)
        window_width = 8
        window_height = 10
        left_window_x = screen_x + 8
        right_window_x = screen_x + self.size - 16
        window_y = building_y + 8

        for window_x in [left_window_x, right_window_x]:
            pygame.draw.rect(
                screen, book_color, (window_x, window_y, window_width, window_height)
            )
            # Book spines
            for i in range(3):
                spine_y = window_y + 2 + (i * 3)
                pygame.draw.line(
                    screen,
                    accent_color,
                    (window_x + 1, spine_y),
                    (window_x + window_width - 1, spine_y),
                )

        # Draw portal gift glow effect when active
        if self.portal_gift_active:
            center_x = screen_x + self.size // 2
            center_y = screen_y + self.size // 2

            # Pulsing glow effect
            pulse = abs(math.sin(self.animation_time * 5))
            glow_radius = int(self.size * 0.7 * (1 + pulse * 0.4))

            # Multiple glow layers for soft effect
            for i in range(3):
                alpha_value = int(120 * (1 - i / 3) * pulse)
                radius = glow_radius - (i * 8)
                # Create surface with per-pixel alpha
                glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                glow_color = (138, 43, 226, alpha_value)  # Purple/violet portal glow
                pygame.draw.circle(glow_surface, glow_color, (radius, radius), radius)
                screen.blit(glow_surface, (center_x - radius, center_y - radius))

        # Draw book icon above door
        book_icon_y = door_y - 8
        book_icon_x = screen_x + self.size // 2
        # Book pages
        pygame.draw.rect(
            screen, book_color, (book_icon_x - 4, book_icon_y, 8, 6)
        )
        # Book cover edges
        pygame.draw.line(
            screen,
            accent_color,
            (book_icon_x - 4, book_icon_y),
            (book_icon_x - 4, book_icon_y + 6),
            2,
        )
        pygame.draw.line(
            screen,
            accent_color,
            (book_icon_x + 4, book_icon_y),
            (book_icon_x + 4, book_icon_y + 6),
            2,
        )

        # Draw label below library
        font = pygame.font.Font(None, 18)
        label_text = "Library"
        text_surface = font.render(label_text, True, (255, 255, 255))

        # Add subtle shadow to text
        shadow_surface = font.render(label_text, True, (50, 50, 50))
        center_x = screen_x + self.size // 2
        text_rect = text_surface.get_rect(
            center=(center_x + 1, screen_y + self.size + 9)
        )
        screen.blit(shadow_surface, text_rect)

        text_rect = text_surface.get_rect(center=(center_x, screen_y + self.size + 8))
        screen.blit(text_surface, text_rect)
