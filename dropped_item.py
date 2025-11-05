"""Dropped item class for items on the ground."""

import pygame
from item import Item
import config


class DroppedItem:
    """Represents an item on the ground that can be picked up."""

    def __init__(self, item: Item, grid_x: int, grid_y: int):
        """
        Initialize a dropped item.

        Args:
            item: The Item object
            grid_x: Grid x position
            grid_y: Grid y position
        """
        self.item = item
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size = config.TILE_SIZE // 2  # Half tile size for visual clarity

    @property
    def x(self) -> int:
        """Get pixel x coordinate (centered in tile)."""
        return self.grid_x * config.TILE_SIZE + (config.TILE_SIZE - self.size) // 2

    @property
    def y(self) -> int:
        """Get pixel y coordinate (centered in tile)."""
        return self.grid_y * config.TILE_SIZE + (config.TILE_SIZE - self.size) // 2

    def get_rect(self) -> pygame.Rect:
        """Get the dropped item's rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen: pygame.Surface):
        """Draw the dropped item on the ground."""
        # Draw item as a smaller colored square with sparkle effect
        # Color coding by item type
        from item import ItemType

        if self.item.item_type == ItemType.WEAPON:
            color = (220, 180, 50)  # Gold/bronze for weapons
        elif self.item.item_type == ItemType.ARMOR:
            color = (180, 180, 200)  # Silver for armor
        elif self.item.item_type == ItemType.CONSUMABLE:
            color = (50, 220, 50)  # Green for consumables
        else:
            color = (220, 220, 50)  # Yellow for misc items

        # Draw main item square
        pygame.draw.rect(screen, color, self.get_rect())

        # Draw border to make it stand out
        pygame.draw.rect(screen, config.WHITE, self.get_rect(), 2)

        # Draw a small sparkle effect in the corner
        sparkle_size = 3
        sparkle_x = self.x + self.size - sparkle_size - 2
        sparkle_y = self.y + 2
        pygame.draw.circle(screen, config.WHITE, (sparkle_x, sparkle_y), sparkle_size)

        # Draw item name below (abbreviated)
        font = pygame.font.Font(None, 16)
        name = self.item.name
        if len(name) > 10:
            name = name[:8] + ".."

        text = font.render(name, True, config.WHITE)
        text_x = self.x + (self.size - text.get_width()) // 2
        text_y = self.y + self.size + 2

        # Draw text background for readability
        text_bg = pygame.Rect(
            text_x - 2, text_y - 1, text.get_width() + 4, text.get_height() + 2
        )
        pygame.draw.rect(screen, config.BLACK, text_bg)

        screen.blit(text, (text_x, text_y))
