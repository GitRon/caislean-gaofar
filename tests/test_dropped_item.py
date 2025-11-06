"""Tests for dropped_item.py - DroppedItem class"""

import pygame
from unittest.mock import Mock, patch
from dropped_item import DroppedItem
from item import Item, ItemType
import config


class TestDroppedItem:
    """Tests for DroppedItem class"""

    def test_dropitem_initialization(self):
        """Test DroppedItem initialization"""
        # Arrange
        item = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        grid_x = 5
        grid_y = 3

        # Act
        dropped = DroppedItem(item, grid_x, grid_y)

        # Assert
        assert dropped.item == item
        assert dropped.grid_x == 5
        assert dropped.grid_y == 3
        assert dropped.size == config.TILE_SIZE // 2

    def test_dropitem_x_property(self):
        """Test DroppedItem x property calculates pixel position"""
        # Arrange
        item = Item("Sword", ItemType.WEAPON)
        dropped = DroppedItem(item, 4, 2)

        # Act
        pixel_x = dropped.x

        # Assert
        expected_x = 4 * config.TILE_SIZE + (config.TILE_SIZE - dropped.size) // 2
        assert pixel_x == expected_x

    def test_dropitem_y_property(self):
        """Test DroppedItem y property calculates pixel position"""
        # Arrange
        item = Item("Shield", ItemType.ARMOR)
        dropped = DroppedItem(item, 2, 6)

        # Act
        pixel_y = dropped.y

        # Assert
        expected_y = 6 * config.TILE_SIZE + (config.TILE_SIZE - dropped.size) // 2
        assert pixel_y == expected_y

    def test_dropitem_get_rect(self):
        """Test DroppedItem get_rect returns correct pygame.Rect"""
        # Arrange
        item = Item("Potion", ItemType.CONSUMABLE)
        dropped = DroppedItem(item, 3, 4)

        # Act
        rect = dropped.get_rect()

        # Assert
        assert isinstance(rect, pygame.Rect)
        assert rect.x == dropped.x
        assert rect.y == dropped.y
        assert rect.width == dropped.size
        assert rect.height == dropped.size

    @patch("pygame.draw.rect")
    @patch("pygame.draw.circle")
    @patch("pygame.font.Font")
    def test_dropitem_draw_weapon_color(self, mock_font, mock_circle, mock_rect):
        """Test DroppedItem draw with WEAPON item type uses correct color"""
        # Arrange
        pygame.init()
        screen = Mock(spec=pygame.Surface)
        mock_text = Mock()
        mock_text.get_width.return_value = 40
        mock_text.get_height.return_value = 10
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = mock_text
        mock_font.return_value = mock_font_instance

        item = Item("Sword", ItemType.WEAPON)
        dropped = DroppedItem(item, 1, 1)

        # Act
        dropped.draw(screen)

        # Assert
        # First call to rect should be the item color (gold/bronze for weapon)
        first_call_color = mock_rect.call_args_list[0][0][1]
        assert first_call_color == (220, 180, 50)

        pygame.quit()

    @patch("pygame.draw.rect")
    @patch("pygame.draw.circle")
    @patch("pygame.font.Font")
    def test_dropitem_draw_armor_color(self, mock_font, mock_circle, mock_rect):
        """Test DroppedItem draw with ARMOR item type uses correct color"""
        # Arrange
        pygame.init()
        screen = Mock(spec=pygame.Surface)
        mock_text = Mock()
        mock_text.get_width.return_value = 40
        mock_text.get_height.return_value = 10
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = mock_text
        mock_font.return_value = mock_font_instance

        item = Item("Shield", ItemType.ARMOR)
        dropped = DroppedItem(item, 1, 1)

        # Act
        dropped.draw(screen)

        # Assert
        # First call should be the item color (silver for armor)
        first_call_color = mock_rect.call_args_list[0][0][1]
        assert first_call_color == (180, 180, 200)

        pygame.quit()

    @patch("pygame.draw.rect")
    @patch("pygame.draw.circle")
    @patch("pygame.font.Font")
    def test_dropitem_draw_consumable_color(self, mock_font, mock_circle, mock_rect):
        """Test DroppedItem draw with CONSUMABLE item type uses correct color"""
        # Arrange
        pygame.init()
        screen = Mock(spec=pygame.Surface)
        mock_text = Mock()
        mock_text.get_width.return_value = 40
        mock_text.get_height.return_value = 10
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = mock_text
        mock_font.return_value = mock_font_instance

        item = Item("Potion", ItemType.CONSUMABLE)
        dropped = DroppedItem(item, 1, 1)

        # Act
        dropped.draw(screen)

        # Assert
        # First call should be the item color (green for consumable)
        first_call_color = mock_rect.call_args_list[0][0][1]
        assert first_call_color == (50, 220, 50)

        pygame.quit()

    @patch("pygame.draw.rect")
    @patch("pygame.draw.circle")
    @patch("pygame.font.Font")
    def test_dropitem_draw_misc_color(self, mock_font, mock_circle, mock_rect):
        """Test DroppedItem draw with MISC item type uses correct color"""
        # Arrange
        pygame.init()
        screen = Mock(spec=pygame.Surface)
        mock_text = Mock()
        mock_text.get_width.return_value = 40
        mock_text.get_height.return_value = 10
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = mock_text
        mock_font.return_value = mock_font_instance

        item = Item("Key", ItemType.MISC)
        dropped = DroppedItem(item, 1, 1)

        # Act
        dropped.draw(screen)

        # Assert
        # First call should be the item color (yellow for misc)
        first_call_color = mock_rect.call_args_list[0][0][1]
        assert first_call_color == (220, 220, 50)

        pygame.quit()

    @patch("pygame.draw.rect")
    @patch("pygame.draw.circle")
    @patch("pygame.font.Font")
    def test_dropitem_draw_short_name(self, mock_font, mock_circle, mock_rect):
        """Test DroppedItem draw with short name (no truncation)"""
        # Arrange
        pygame.init()
        screen = Mock(spec=pygame.Surface)
        mock_text = Mock()
        mock_text.get_width.return_value = 40
        mock_text.get_height.return_value = 10
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = mock_text
        mock_font.return_value = mock_font_instance

        item = Item("Sword", ItemType.WEAPON)
        dropped = DroppedItem(item, 1, 1)

        # Act
        dropped.draw(screen)

        # Assert
        # Verify screen.blit was called (text rendering)
        assert screen.blit.called
        # Verify name was not truncated
        mock_font_instance.render.assert_called_once()
        rendered_text = mock_font_instance.render.call_args[0][0]
        assert rendered_text == "Sword"

        pygame.quit()

    @patch("pygame.draw.rect")
    @patch("pygame.draw.circle")
    @patch("pygame.font.Font")
    def test_dropitem_draw_long_name(self, mock_font, mock_circle, mock_rect):
        """Test DroppedItem draw with long name (with truncation)"""
        # Arrange
        pygame.init()
        screen = Mock(spec=pygame.Surface)
        mock_text = Mock()
        mock_text.get_width.return_value = 40
        mock_text.get_height.return_value = 10
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = mock_text
        mock_font.return_value = mock_font_instance

        item = Item("Very Long Item Name", ItemType.WEAPON)
        dropped = DroppedItem(item, 1, 1)

        # Act
        dropped.draw(screen)

        # Assert
        # Verify screen.blit was called (text rendering)
        assert screen.blit.called
        # Verify name was truncated (should be "Very Lon..")
        mock_font_instance.render.assert_called_once()
        rendered_text = mock_font_instance.render.call_args[0][0]
        assert rendered_text == "Very Lon.."

        pygame.quit()
