"""
Chest System - Chests that contain random loot and can be opened by the player.
"""

import pygame
import random
from typing import Optional
from caislean_gaofar.objects.item import Item, ItemType
from caislean_gaofar.core.config import TILE_SIZE, COLOR_CHEST, GOLD
from caislean_gaofar.utils.grid import Grid


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

    def get_screen_x(self, camera_offset_x: int = 0) -> int:
        """
        Get the screen pixel x coordinate with camera offset applied.

        Args:
            camera_offset_x: Camera offset in grid coordinates (default 0)

        Returns:
            Screen pixel x coordinate
        """
        return (self.grid_x - camera_offset_x) * TILE_SIZE

    def get_screen_y(self, camera_offset_y: int = 0) -> int:
        """
        Get the screen pixel y coordinate with camera offset applied.

        Args:
            camera_offset_y: Camera offset in grid coordinates (default 0)

        Returns:
            Screen pixel y coordinate
        """
        return (self.grid_y - camera_offset_y) * TILE_SIZE

    def open(self) -> Item:
        """
        Open the chest and return the item inside.

        Returns:
            The Item contained in the chest
        """
        self.is_opened = True
        return self.item

    def draw(
        self,
        screen: pygame.Surface,
        camera_offset_x: int = 0,
        camera_offset_y: int = 0,
    ):
        """
        Draw the chest on the screen.
        Chests appear as 3D treasure chests with lid, body, metal bands, and lock.

        Args:
            screen: The pygame screen surface
            camera_offset_x: Camera offset in grid coordinates (default 0)
            camera_offset_y: Camera offset in grid coordinates (default 0)
        """
        if self.is_opened:
            return  # Don't draw opened chests

        # Calculate screen coordinates with camera offset
        screen_x = self.get_screen_x(camera_offset_x)
        screen_y = self.get_screen_y(camera_offset_y)

        # Color palette for 3D chest
        dark_brown = (80, 40, 10)
        medium_brown = (139, 69, 19)
        light_brown = (180, 100, 40)
        very_dark_brown = (50, 25, 5)
        metal_dark = (60, 60, 70)
        metal_light = (120, 120, 140)
        lock_gold = (255, 215, 0)
        lock_gold_dark = (200, 150, 0)

        # Chest dimensions
        chest_width = TILE_SIZE * 3 // 4
        chest_height = TILE_SIZE * 3 // 4
        chest_x = screen_x + (TILE_SIZE - chest_width) // 2
        chest_y = screen_y + (TILE_SIZE - chest_height) // 2
        lid_height = chest_height // 3

        # Draw chest body (main container)
        body_rect = pygame.Rect(
            chest_x,
            chest_y + lid_height,
            chest_width,
            chest_height - lid_height,
        )
        pygame.draw.rect(screen, dark_brown, body_rect)

        # Add 3D depth to body - left shadow
        pygame.draw.rect(
            screen,
            very_dark_brown,
            (chest_x, chest_y + lid_height, 3, chest_height - lid_height),
        )

        # Add 3D depth to body - right highlight
        pygame.draw.rect(
            screen,
            medium_brown,
            (
                chest_x + chest_width - 3,
                chest_y + lid_height,
                3,
                chest_height - lid_height,
            ),
        )

        # Draw chest lid with curved top
        lid_rect = pygame.Rect(chest_x, chest_y, chest_width, lid_height)
        pygame.draw.rect(screen, medium_brown, lid_rect)

        # Add curved/rounded top to lid
        pygame.draw.ellipse(
            screen,
            light_brown,
            (chest_x, chest_y, chest_width, lid_height * 2),
            0,
        )

        # Re-draw lower part of lid to cover ellipse overflow
        pygame.draw.rect(
            screen,
            medium_brown,
            (chest_x, chest_y + lid_height // 2, chest_width, lid_height // 2),
        )

        # Add shadow under lid
        pygame.draw.line(
            screen,
            very_dark_brown,
            (chest_x, chest_y + lid_height),
            (chest_x + chest_width, chest_y + lid_height),
            2,
        )

        # Draw metal bands (horizontal reinforcement)
        band_width = 4
        # Top band on body
        pygame.draw.rect(
            screen,
            metal_dark,
            (chest_x, chest_y + lid_height + 2, chest_width, band_width),
        )
        pygame.draw.rect(
            screen,
            metal_light,
            (chest_x, chest_y + lid_height + 2, chest_width, 2),
        )

        # Bottom band on body
        pygame.draw.rect(
            screen,
            metal_dark,
            (
                chest_x,
                chest_y + chest_height - band_width - 2,
                chest_width,
                band_width,
            ),
        )
        pygame.draw.rect(
            screen,
            metal_light,
            (chest_x, chest_y + chest_height - band_width - 2, chest_width, 2),
        )

        # Draw vertical metal band in center
        center_x = chest_x + chest_width // 2
        pygame.draw.rect(
            screen,
            metal_dark,
            (center_x - 2, chest_y, 4, chest_height),
        )
        pygame.draw.rect(
            screen,
            metal_light,
            (center_x - 2, chest_y, 2, chest_height),
        )

        # Draw lock (golden rectangle with keyhole)
        lock_width = 12
        lock_height = 14
        lock_x = center_x - lock_width // 2
        lock_y = chest_y + lid_height + chest_height // 3
        lock_rect = pygame.Rect(lock_x, lock_y, lock_width, lock_height)

        # Lock body
        pygame.draw.rect(screen, lock_gold, lock_rect, 0, 3)
        pygame.draw.rect(screen, lock_gold_dark, lock_rect, 2, 3)

        # Keyhole (small black circle and vertical line)
        keyhole_center = (center_x, lock_y + 5)
        pygame.draw.circle(screen, (0, 0, 0), keyhole_center, 2)
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (center_x, lock_y + 5),
            (center_x, lock_y + lock_height - 3),
            2,
        )

        # Add corner details (metal corners)
        corner_size = 3
        corners = [
            (chest_x, chest_y + lid_height),  # Top left
            (chest_x + chest_width - corner_size, chest_y + lid_height),  # Top right
            (chest_x, chest_y + chest_height - corner_size),  # Bottom left
            (
                chest_x + chest_width - corner_size,
                chest_y + chest_height - corner_size,
            ),  # Bottom right
        ]
        for corner_x, corner_y in corners:
            pygame.draw.rect(
                screen, metal_light, (corner_x, corner_y, corner_size, corner_size)
            )

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
            Item(
                "Iron Sword",
                ItemType.WEAPON,
                "A basic sword",
                attack_bonus=10,
                gold_value=100,
            ),
            Item(
                "Steel Sword",
                ItemType.WEAPON,
                "A stronger sword",
                attack_bonus=20,
                gold_value=200,
            ),
            Item(
                "Battle Axe",
                ItemType.WEAPON,
                "A heavy axe",
                attack_bonus=25,
                gold_value=250,
            ),
            Item(
                "Dagger",
                ItemType.WEAPON,
                "A quick blade",
                attack_bonus=8,
                gold_value=80,
            ),
            Item(
                "Mace",
                ItemType.WEAPON,
                "A blunt weapon",
                attack_bonus=15,
                gold_value=150,
            ),
            # Armor
            Item(
                "Leather Armor",
                ItemType.ARMOR,
                "Basic protection",
                defense_bonus=5,
                gold_value=50,
            ),
            Item(
                "Chain Mail",
                ItemType.ARMOR,
                "Metal armor",
                defense_bonus=10,
                gold_value=100,
            ),
            Item(
                "Plate Armor",
                ItemType.ARMOR,
                "Heavy armor",
                defense_bonus=15,
                gold_value=150,
            ),
            Item(
                "Shield",
                ItemType.ARMOR,
                "A sturdy shield",
                defense_bonus=8,
                gold_value=80,
            ),
            # Consumables
            Item(
                "Health Potion",
                ItemType.CONSUMABLE,
                "Restores 30 HP",
                gold_value=30,
            ),
            Item(
                "Minor Health Potion",
                ItemType.CONSUMABLE,
                "Restores 30 HP",
                gold_value=25,
            ),
            Item(
                "Greater Health Potion",
                ItemType.CONSUMABLE,
                "Restores 30 HP",
                gold_value=50,
            ),
            # Misc
            Item("Ancient Key", ItemType.MISC, "Opens something?", gold_value=50),
            Item("Magic Scroll", ItemType.MISC, "Mysterious writings", gold_value=75),
        ]

        return random.choice(item_pool)
