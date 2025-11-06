"""Tests for chest.py - Chest class"""

import pygame
from unittest import mock
from chest import Chest
from item import Item, ItemType
from config import TILE_SIZE


class TestChest:
    """Tests for Chest class"""

    def test_chest_initialization_with_item(self):
        """Test Chest initialization with provided item"""
        # Arrange
        test_item = Item("Test Sword", ItemType.WEAPON, "A test item")

        # Act
        chest = Chest(5, 3, test_item)

        # Assert
        assert chest.grid_x == 5
        assert chest.grid_y == 3
        assert chest.item == test_item
        assert chest.is_opened is False

    def test_chest_initialization_without_item_generates_random(self):
        """Test Chest initialization without item generates random item"""
        # Arrange & Act
        chest = Chest(5, 3)

        # Assert
        assert chest.grid_x == 5
        assert chest.grid_y == 3
        assert chest.item is not None
        assert isinstance(chest.item, Item)
        assert chest.is_opened is False

    def test_chest_x_property_returns_pixel_coordinate(self):
        """Test x property returns correct pixel X coordinate"""
        # Arrange
        test_item = Item("Test Sword", ItemType.WEAPON)
        chest = Chest(5, 3, test_item)

        # Act
        x_coord = chest.x

        # Assert
        # Grid position 5 * TILE_SIZE (50) = 250
        assert x_coord == 5 * TILE_SIZE

    def test_chest_y_property_returns_pixel_coordinate(self):
        """Test y property returns correct pixel Y coordinate"""
        # Arrange
        test_item = Item("Test Sword", ItemType.WEAPON)
        chest = Chest(5, 3, test_item)

        # Act
        y_coord = chest.y

        # Assert
        # Grid position 3 * TILE_SIZE (50) = 150
        assert y_coord == 3 * TILE_SIZE

    def test_chest_get_rect_returns_correct_rectangle(self):
        """Test get_rect returns correct collision rectangle"""
        # Arrange
        test_item = Item("Test Sword", ItemType.WEAPON)
        chest = Chest(5, 3, test_item)

        # Act
        rect = chest.get_rect()

        # Assert
        assert rect.x == 5 * TILE_SIZE
        assert rect.y == 3 * TILE_SIZE
        assert rect.width == TILE_SIZE
        assert rect.height == TILE_SIZE

    def test_chest_open_returns_item_and_marks_opened(self):
        """Test open() returns item and marks chest as opened"""
        # Arrange
        test_item = Item("Test Sword", ItemType.WEAPON)
        chest = Chest(5, 3, test_item)

        # Act
        returned_item = chest.open()

        # Assert
        assert returned_item == test_item
        assert chest.is_opened is True

    def test_chest_draw_when_not_opened_draws_chest(self):
        """Test draw() when chest is not opened draws the chest"""
        # Arrange
        pygame.init()
        screen = pygame.Surface((800, 600))
        test_item = Item("Test Sword", ItemType.WEAPON)
        chest = Chest(5, 3, test_item)

        # Act & Assert (no exception should be raised)
        chest.draw(screen)

        # Verify it's still not opened
        assert chest.is_opened is False

        # Cleanup
        pygame.quit()

    def test_chest_draw_when_opened_returns_early(self):
        """Test draw() when chest is opened returns early without drawing"""
        # Arrange
        pygame.init()
        screen = pygame.Surface((800, 600))
        test_item = Item("Test Sword", ItemType.WEAPON)
        chest = Chest(5, 3, test_item)
        chest.is_opened = True

        # Act
        with mock.patch("pygame.draw.rect") as mock_rect:
            chest.draw(screen)

            # Assert - pygame.draw.rect should not be called since chest is opened
            mock_rect.assert_not_called()

        # Cleanup
        pygame.quit()

    def test_generate_random_item_returns_item_from_pool(self):
        """Test _generate_random_item returns an Item from the item pool"""
        # Arrange & Act
        item = Chest._generate_random_item()

        # Assert
        assert isinstance(item, Item)
        assert item.name in [
            "Iron Sword",
            "Steel Sword",
            "Battle Axe",
            "Dagger",
            "Mace",
            "Leather Armor",
            "Chain Mail",
            "Plate Armor",
            "Shield",
            "Health Potion",
            "Minor Health Potion",
            "Greater Health Potion",
            "Gold Coin",
            "Ancient Key",
            "Magic Scroll",
        ]

    def test_generate_random_item_returns_weapon_type(self):
        """Test _generate_random_item can return weapon type items"""
        # Arrange
        weapon_item = Item(
            "Iron Sword", ItemType.WEAPON, "A basic sword", attack_bonus=10
        )

        # Act
        with mock.patch("random.choice", return_value=weapon_item):
            item = Chest._generate_random_item()

        # Assert
        assert item.item_type == ItemType.WEAPON
        assert item == weapon_item

    def test_generate_random_item_returns_armor_type(self):
        """Test _generate_random_item can return armor type items"""
        # Arrange
        armor_item = Item(
            "Leather Armor",
            ItemType.ARMOR,
            "Basic protection",
            defense_bonus=5,
            health_bonus=10,
        )

        # Act
        with mock.patch("random.choice", return_value=armor_item):
            item = Chest._generate_random_item()

        # Assert
        assert item.item_type == ItemType.ARMOR
        assert item == armor_item

    def test_generate_random_item_returns_consumable_type(self):
        """Test _generate_random_item can return consumable type items"""
        # Arrange
        consumable_item = Item(
            "Health Potion", ItemType.CONSUMABLE, "Restores 50 HP", health_bonus=50
        )

        # Act
        with mock.patch("random.choice", return_value=consumable_item):
            item = Chest._generate_random_item()

        # Assert
        assert item.item_type == ItemType.CONSUMABLE
        assert item == consumable_item

    def test_generate_random_item_returns_misc_type(self):
        """Test _generate_random_item can return misc type items"""
        # Arrange
        misc_item = Item("Gold Coin", ItemType.MISC, "A shiny coin")

        # Act
        with mock.patch("random.choice", return_value=misc_item):
            item = Chest._generate_random_item()

        # Assert
        assert item.item_type == ItemType.MISC
        assert item == misc_item
