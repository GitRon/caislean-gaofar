"""Tests for inventory_ui.py - InventoryUI class"""

import pytest
from unittest.mock import Mock, patch
import pygame
from inventory_ui import InventoryUI
from inventory import Inventory
from item import Item, ItemType


# Initialize pygame once for all tests
pygame.init()


@pytest.fixture
def mock_screen():
    """Create a mock pygame surface"""
    screen = Mock(spec=pygame.Surface)
    screen.get_width = Mock(return_value=800)
    screen.get_height = Mock(return_value=600)
    screen.blit = Mock()
    return screen


@pytest.fixture
def inventory_ui():
    """Create an InventoryUI instance"""
    return InventoryUI()


@pytest.fixture
def inventory_with_items():
    """Create an inventory with some items"""
    inv = Inventory()
    inv.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
    inv.armor_slot = Item("Shield", ItemType.ARMOR, defense_bonus=5)
    inv.backpack_slots[0] = Item("Potion", ItemType.CONSUMABLE)
    return inv


class TestInventoryUI:
    """Tests for InventoryUI class"""

    def test_inventory_ui_initialization(self, inventory_ui):
        """Test InventoryUI initialization"""
        # Assert
        assert inventory_ui.panel_width == 500
        assert inventory_ui.panel_height == 400
        assert inventory_ui.selected_slot is None
        assert inventory_ui.hovered_slot is None
        assert inventory_ui.dragging_item is None
        assert inventory_ui.dragging_from is None
        assert inventory_ui.context_menu_slot is None
        assert inventory_ui.context_menu_pos is None
        assert inventory_ui.slot_rects == {}

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    @patch("pygame.draw.rect")
    @patch("pygame.Surface")
    def test_draw_basic(
        self, mock_surface, mock_draw_rect, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test basic drawing of inventory UI"""
        # Arrange
        inventory = Inventory()

        # Act
        inventory_ui.draw(mock_screen, inventory)

        # Assert
        assert mock_screen.blit.called

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    @patch("pygame.draw.rect")
    @patch("pygame.Surface")
    def test_draw_with_items(
        self,
        mock_surface,
        mock_draw_rect,
        mock_get_pos,
        inventory_ui,
        mock_screen,
        inventory_with_items,
    ):
        """Test drawing inventory UI with items"""
        # Act
        inventory_ui.draw(mock_screen, inventory_with_items)

        # Assert
        assert mock_screen.blit.called

    def test_selected_slot_initial_state(self, inventory_ui):
        """Test selected slot starts as None"""
        # Assert
        assert inventory_ui.selected_slot is None

    def test_hovered_slot_initial_state(self, inventory_ui):
        """Test hovered slot starts as None"""
        # Assert
        assert inventory_ui.hovered_slot is None

    def test_dragging_state_initial(self, inventory_ui):
        """Test dragging state starts empty"""
        # Assert
        assert inventory_ui.dragging_item is None
        assert inventory_ui.dragging_from is None

    def test_context_menu_state_initial(self, inventory_ui):
        """Test context menu state starts empty"""
        # Assert
        assert inventory_ui.context_menu_slot is None
        assert inventory_ui.context_menu_pos is None

    def test_slot_rects_initial_state(self, inventory_ui):
        """Test slot_rects starts empty"""
        # Assert
        assert inventory_ui.slot_rects == {}
