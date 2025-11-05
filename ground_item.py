"""
Ground Item System - Items that exist in the game world and can be picked up.
"""

import pygame
from item import Item
from config import TILE_SIZE, COLOR_GROUND_ITEM, COLOR_WHITE
from grid import Grid


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
        return pygame.Rect(
            self.x - size // 2,
            self.y - size // 2,
            size,
            size
        )

    def draw(self, screen: pygame.Surface):
        """
        Draw the ground item on the screen.
        Shows a small colored square with the first letter of the item name.
        """
        # Draw background square
        rect = self.get_rect()
        pygame.draw.rect(screen, COLOR_GROUND_ITEM, rect)
        pygame.draw.rect(screen, COLOR_WHITE, rect, 2)  # White border

        # Draw first letter of item name
        font = pygame.font.Font(None, 24)
        letter = self.item.name[0].upper() if self.item.name else "?"
        text_surface = font.render(letter, True, COLOR_WHITE)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)
