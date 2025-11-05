"""
Chest System - Chests that contain random loot and can be opened by the player.
"""

import pygame
import random
from typing import Optional
from item import Item, ItemType
from config import TILE_SIZE, COLOR_CHEST, COLOR_WHITE, BROWN, GOLD
from grid import Grid


class Chest:
    """Represents a chest in the game world that opens when stepped on."""

    def __init__(self, grid_x: int, grid_y: int, item: Optional[Item] = None):
        """
        Initialize a chest.

        Args:
            grid_x: Grid X coordinate (tile position)
            grid_y: Grid Y coordinate (tile position)
            item: The item this chest contains (if None, generates random item)
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.item = item if item else self._generate_random_item()
        self.is_opened = False

    @property
    def x(self) -> int:
        """Pixel X coordinate (top-left of tile)."""
        return Grid.grid_to_pixel(self.grid_x, self.grid_y)[0]

    @property
    def y(self) -> int:
        """Pixel Y coordinate (top-left of tile)."""
        return Grid.grid_to_pixel(self.grid_x, self.grid_y)[1]

    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle for the chest."""
        return pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

    def open(self) -> Item:
        """
        Open the chest and return the item inside.

        Returns:
            The Item contained in the chest
        """
        self.is_opened = True
        return self.item

    def draw(self, screen: pygame.Surface):
        """
        Draw the chest on the screen.
        Chests appear as brown rectangles with a golden lock icon.
        """
        if self.is_opened:
            return  # Don't draw opened chests

        # Draw chest body (brown rectangle)
        chest_rect = pygame.Rect(
            self.x + TILE_SIZE // 4,
            self.y + TILE_SIZE // 4,
            TILE_SIZE // 2,
            TILE_SIZE // 2
        )
        pygame.draw.rect(screen, COLOR_CHEST, chest_rect)
        pygame.draw.rect(screen, (80, 40, 10), chest_rect, 3)  # Dark brown border

        # Draw lock (golden circle in center)
        lock_center = (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)
        pygame.draw.circle(screen, GOLD, lock_center, 6)
        pygame.draw.circle(screen, (200, 150, 0), lock_center, 6, 2)  # Darker gold border

    @staticmethod
    def _generate_random_item() -> Item:
        """
        Generate a random item for the chest.

        Returns:
            A randomly selected Item from the item pool
        """
        # Define the item pool for chest generation
        item_pool = [
            # Weapons
            Item("Iron Sword", ItemType.WEAPON, "A basic sword", attack_bonus=10),
            Item("Steel Sword", ItemType.WEAPON, "A stronger sword", attack_bonus=20),
            Item("Battle Axe", ItemType.WEAPON, "A heavy axe", attack_bonus=25),
            Item("Dagger", ItemType.WEAPON, "A quick blade", attack_bonus=8),
            Item("Mace", ItemType.WEAPON, "A blunt weapon", attack_bonus=15),

            # Armor
            Item("Leather Armor", ItemType.ARMOR, "Basic protection", defense_bonus=5, health_bonus=10),
            Item("Chain Mail", ItemType.ARMOR, "Metal armor", defense_bonus=10, health_bonus=20),
            Item("Plate Armor", ItemType.ARMOR, "Heavy armor", defense_bonus=15, health_bonus=30),
            Item("Shield", ItemType.ARMOR, "A sturdy shield", defense_bonus=8),

            # Consumables
            Item("Health Potion", ItemType.CONSUMABLE, "Restores 50 HP", health_bonus=50),
            Item("Minor Health Potion", ItemType.CONSUMABLE, "Restores 25 HP", health_bonus=25),
            Item("Greater Health Potion", ItemType.CONSUMABLE, "Restores 100 HP", health_bonus=100),

            # Misc
            Item("Gold Coin", ItemType.MISC, "A shiny coin"),
            Item("Ancient Key", ItemType.MISC, "Opens something?"),
            Item("Magic Scroll", ItemType.MISC, "Mysterious writings"),
        ]

        return random.choice(item_pool)
