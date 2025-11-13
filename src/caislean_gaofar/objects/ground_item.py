"""
Ground Item System - Items that exist in the game world and can be picked up.
"""

import pygame
from caislean_gaofar.objects.item import Item
from caislean_gaofar.core.config import TILE_SIZE, COLOR_GROUND_ITEM, COLOR_WHITE
from caislean_gaofar.utils.grid import Grid


class GroundItem:
    """Represents an item lying on the ground that can be picked up by the player."""

    def __init__(self, item: Item, grid_x: int, grid_y: int):
        """
        Initialize a ground item.

        Args:
            item: The Item object this ground item contains
            grid_x: Grid X coordinate (tile position)
            grid_y: Grid Y coordinate (tile position)
        """
        self.item = item
        self.grid_x = grid_x
        self.grid_y = grid_y

    @property
    def x(self) -> int:
        """Pixel X coordinate (center of tile)."""
        return Grid.grid_to_pixel(self.grid_x, self.grid_y)[0] + TILE_SIZE // 2

    @property
    def y(self) -> int:
        """Pixel Y coordinate (center of tile)."""
        return Grid.grid_to_pixel(self.grid_x, self.grid_y)[1] + TILE_SIZE // 2

    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle for pickup detection."""
        # Small square in center of tile
        size = TILE_SIZE // 2
        return pygame.Rect(self.x - size // 2, self.y - size // 2, size, size)

    def get_screen_x(self, camera_offset_x: int = 0) -> int:
        """
        Get the screen pixel x coordinate with camera offset applied.

        Args:
            camera_offset_x: Camera offset in grid coordinates (default 0)

        Returns:
            Screen pixel x coordinate (center of tile)
        """
        return (self.grid_x - camera_offset_x) * TILE_SIZE + TILE_SIZE // 2

    def get_screen_y(self, camera_offset_y: int = 0) -> int:
        """
        Get the screen pixel y coordinate with camera offset applied.

        Args:
            camera_offset_y: Camera offset in grid coordinates (default 0)

        Returns:
            Screen pixel y coordinate (center of tile)
        """
        return (self.grid_y - camera_offset_y) * TILE_SIZE + TILE_SIZE // 2

    def draw(
        self,
        screen: pygame.Surface,
        camera_offset_x: int = 0,
        camera_offset_y: int = 0,
    ):
        """
        Draw the ground item on the screen.
        Shows a small colored square with the first letter of the item name.

        Args:
            screen: The pygame screen surface
            camera_offset_x: Camera offset in grid coordinates (default 0)
            camera_offset_y: Camera offset in grid coordinates (default 0)
        """
        # Calculate screen coordinates with camera offset
        screen_x = self.get_screen_x(camera_offset_x)
        screen_y = self.get_screen_y(camera_offset_y)

        # Draw background square
        size = TILE_SIZE // 2
        rect = pygame.Rect(screen_x - size // 2, screen_y - size // 2, size, size)
        pygame.draw.rect(screen, COLOR_GROUND_ITEM, rect)
        pygame.draw.rect(screen, COLOR_WHITE, rect, 2)  # White border

        # Draw first letter of item name
        font = pygame.font.Font(None, 24)
        letter = self.item.name[0].upper() if self.item.name else "?"
        text_surface = font.render(letter, True, COLOR_WHITE)
        text_rect = text_surface.get_rect(center=(screen_x, screen_y))
        screen.blit(text_surface, text_rect)
