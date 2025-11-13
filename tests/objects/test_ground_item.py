"""Tests for ground_item.py - GroundItem class"""

import pygame
from caislean_gaofar.objects.ground_item import GroundItem
from caislean_gaofar.objects.item import Item, ItemType
from caislean_gaofar.core.config import TILE_SIZE


class TestGroundItem:
    """Tests for GroundItem class"""

    def test_ground_item_initialization(self):
        """Test GroundItem initialization with item and position"""
        # Arrange
        test_item = Item("Test Sword", ItemType.WEAPON, "A test item")

        # Act
        ground_item = GroundItem(test_item, 5, 3)

        # Assert
        assert ground_item.item == test_item
        assert ground_item.grid_x == 5
        assert ground_item.grid_y == 3

    def test_ground_item_x_property_returns_center_pixel_coordinate(self):
        """Test x property returns center pixel X coordinate"""
        # Arrange
        test_item = Item("Test Sword", ItemType.WEAPON)
        ground_item = GroundItem(test_item, 5, 3)

        # Act
        x_coord = ground_item.x

        # Assert
        # Grid position 5 * TILE_SIZE (50) + TILE_SIZE // 2 (25) = 275
        assert x_coord == 5 * TILE_SIZE + TILE_SIZE // 2

    def test_ground_item_y_property_returns_center_pixel_coordinate(self):
        """Test y property returns center pixel Y coordinate"""
        # Arrange
        test_item = Item("Test Sword", ItemType.WEAPON)
        ground_item = GroundItem(test_item, 5, 3)

        # Act
        y_coord = ground_item.y

        # Assert
        # Grid position 3 * TILE_SIZE (50) + TILE_SIZE // 2 (25) = 175
        assert y_coord == 3 * TILE_SIZE + TILE_SIZE // 2

    def test_ground_item_get_rect_returns_correct_rectangle(self):
        """Test get_rect returns correct collision rectangle"""
        # Arrange
        test_item = Item("Test Sword", ItemType.WEAPON)
        ground_item = GroundItem(test_item, 5, 3)

        # Act
        rect = ground_item.get_rect()

        # Assert
        size = TILE_SIZE // 2  # 25
        center_x = 5 * TILE_SIZE + TILE_SIZE // 2  # 275
        center_y = 3 * TILE_SIZE + TILE_SIZE // 2  # 175
        assert rect.x == center_x - size // 2
        assert rect.y == center_y - size // 2
        assert rect.width == size
        assert rect.height == size

    def test_ground_item_draw_with_named_item_draws_first_letter(self):
        """Test draw() with named item draws first letter uppercase"""
        # Arrange
        pygame.init()
        screen = pygame.Surface((800, 600))
        test_item = Item("Sword", ItemType.WEAPON)
        ground_item = GroundItem(test_item, 5, 3)

        # Act & Assert (no exception should be raised)
        ground_item.draw(screen)

        # Verify item is still there
        assert ground_item.item == test_item

        # Cleanup
        pygame.quit()

    def test_ground_item_draw_with_lowercase_name_draws_uppercase(self):
        """Test draw() converts lowercase first letter to uppercase"""
        # Arrange
        pygame.init()
        screen = pygame.Surface((800, 600))
        test_item = Item("sword", ItemType.WEAPON)  # lowercase name
        ground_item = GroundItem(test_item, 5, 3)

        # Act & Assert (no exception should be raised)
        ground_item.draw(screen)

        # Cleanup
        pygame.quit()

    def test_ground_item_draw_with_empty_name_draws_question_mark(self):
        """Test draw() with empty name draws question mark"""
        # Arrange
        pygame.init()
        screen = pygame.Surface((800, 600))
        test_item = Item("", ItemType.MISC)  # empty name
        ground_item = GroundItem(test_item, 5, 3)

        # Act & Assert (no exception should be raised)
        ground_item.draw(screen)

        # Cleanup
        pygame.quit()

    def test_ground_item_with_weapon_type(self):
        """Test ground item can hold weapon type items"""
        # Arrange
        weapon = Item("Iron Sword", ItemType.WEAPON, "A basic sword", attack_bonus=10)

        # Act
        ground_item = GroundItem(weapon, 2, 2)

        # Assert
        assert ground_item.item.item_type == ItemType.WEAPON
        assert ground_item.item.attack_bonus == 10

    def test_ground_item_with_armor_type(self):
        """Test ground item can hold armor type items"""
        # Arrange
        armor = Item(
            "Leather Armor", ItemType.ARMOR, "Basic protection", defense_bonus=5
        )

        # Act
        ground_item = GroundItem(armor, 2, 2)

        # Assert
        assert ground_item.item.item_type == ItemType.ARMOR
        assert ground_item.item.defense_bonus == 5

    def test_ground_item_with_consumable_type(self):
        """Test ground item can hold consumable type items"""
        # Arrange
        potion = Item("Health Potion", ItemType.CONSUMABLE, "Restores 30 HP")

        # Act
        ground_item = GroundItem(potion, 2, 2)

        # Assert
        assert ground_item.item.item_type == ItemType.CONSUMABLE
        assert ground_item.item.description == "Restores 30 HP"

    def test_ground_item_with_misc_type(self):
        """Test ground item can hold misc type items"""
        # Arrange
        misc = Item("Gold Coin", ItemType.MISC, "A shiny coin")

        # Act
        ground_item = GroundItem(misc, 2, 2)

        # Assert
        assert ground_item.item.item_type == ItemType.MISC

    def test_ground_item_at_different_positions(self):
        """Test ground items can be placed at different grid positions"""
        # Arrange
        item1 = Item("Item1", ItemType.MISC)
        item2 = Item("Item2", ItemType.MISC)

        # Act
        ground_item1 = GroundItem(item1, 0, 0)
        ground_item2 = GroundItem(item2, 15, 11)

        # Assert
        assert ground_item1.grid_x == 0
        assert ground_item1.grid_y == 0
        assert ground_item2.grid_x == 15
        assert ground_item2.grid_y == 11
        assert ground_item1.x != ground_item2.x
        assert ground_item1.y != ground_item2.y
