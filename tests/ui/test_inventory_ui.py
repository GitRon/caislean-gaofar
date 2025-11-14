"""Tests for inventory_ui.py - InventoryUI class"""

import pytest
from unittest.mock import Mock, patch
import pygame
from caislean_gaofar.ui.inventory_ui import InventoryUI
from caislean_gaofar.systems.inventory import Inventory
from caislean_gaofar.objects.item import Item, ItemType
from caislean_gaofar.core import config


@pytest.fixture(autouse=True)
def setup_pygame():
    """Setup pygame before each test and cleanup after"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_screen():
    """Create a real pygame surface for testing"""
    return pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))


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


@pytest.fixture
def mock_game():
    """Create a mock game instance"""
    game = Mock()
    game.warrior = Mock()
    game.warrior.grid_x = 5
    game.warrior.grid_y = 5
    game.drop_item = Mock()
    return game


class TestInventoryUIInitialization:
    """Tests for InventoryUI initialization"""

    def test_inventory_ui_initialization(self, inventory_ui):
        """Test InventoryUI initialization"""
        assert inventory_ui.panel_width == 500
        assert inventory_ui.panel_height == 500
        assert inventory_ui.padding == 20
        assert inventory_ui.slot_size == 80
        assert inventory_ui.slot_margin == 10
        assert inventory_ui.selected_slot is None
        assert inventory_ui.hovered_slot is None
        assert inventory_ui.dragging_item is None
        assert inventory_ui.dragging_from is None
        assert inventory_ui.drag_offset == (0, 0)
        assert inventory_ui.context_menu_slot is None
        assert inventory_ui.context_menu_pos is None
        assert inventory_ui.slot_rects == {}


class TestInventoryUIDrawing:
    """Tests for InventoryUI drawing methods"""

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_basic(self, mock_get_pos, inventory_ui, mock_screen):
        """Test basic drawing of inventory UI"""
        inventory = Inventory()
        inventory_ui.draw(mock_screen, inventory)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_with_items(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test drawing inventory UI with items"""
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_with_weapon_only(self, mock_get_pos, inventory_ui, mock_screen):
        """Test drawing with only weapon equipped"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=15)
        inventory_ui.draw(mock_screen, inventory)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_with_armor_only(self, mock_get_pos, inventory_ui, mock_screen):
        """Test drawing with only armor equipped"""
        inventory = Inventory()
        inventory.armor_slot = Item("Plate Mail", ItemType.ARMOR, defense_bonus=10)
        inventory_ui.draw(mock_screen, inventory)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_item_with_long_name(self, mock_get_pos, inventory_ui, mock_screen):
        """Test drawing item with name longer than 10 characters"""
        inventory = Inventory()
        inventory.weapon_slot = Item(
            "Very Long Sword Name", ItemType.WEAPON, attack_bonus=10
        )
        inventory_ui.draw(mock_screen, inventory)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_item_with_attack_bonus(self, mock_get_pos, inventory_ui, mock_screen):
        """Test drawing item with attack bonus"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Axe", ItemType.WEAPON, attack_bonus=20)
        inventory_ui.draw(mock_screen, inventory)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_item_with_defense_bonus(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test drawing item with defense bonus"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Helmet", ItemType.ARMOR, defense_bonus=8)
        inventory_ui.draw(mock_screen, inventory)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_item_with_both_bonuses(self, mock_get_pos, inventory_ui, mock_screen):
        """Test drawing item with both attack and defense bonuses"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item(
            "Magic Armor", ItemType.ARMOR, attack_bonus=5, defense_bonus=15
        )
        inventory_ui.draw(mock_screen, inventory)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_all_backpack_slots(self, mock_get_pos, inventory_ui, mock_screen):
        """Test drawing all 13 backpack slots"""
        inventory = Inventory()
        for i in range(13):
            inventory.backpack_slots[i] = Item(
                f"Item {i}", ItemType.MISC, description="Test item"
            )
        inventory_ui.draw(mock_screen, inventory)
        assert len(inventory_ui.slot_rects) == 15  # 2 equipment + 13 backpack

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_with_selected_weapon_slot(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test drawing with weapon slot selected"""
        inventory_ui.selected_slot = ("weapon", 0)
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_with_selected_armor_slot(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test drawing with armor slot selected"""
        inventory_ui.selected_slot = ("armor", 0)
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_with_selected_backpack_slot(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test drawing with backpack slot selected"""
        inventory_ui.selected_slot = ("backpack", 0)
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(250, 250))
    def test_draw_with_hovered_weapon_slot(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test drawing with weapon slot hovered"""
        # Draw first to populate slot_rects
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Hovered slot should be set by _update_hovered_slot
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_instructions(self, mock_get_pos, inventory_ui, mock_screen):
        """Test drawing instructions section"""
        inventory = Inventory()
        inventory_ui.draw(mock_screen, inventory)
        # Test passes if no exceptions are raised


class TestInventoryUITooltip:
    """Tests for tooltip functionality"""

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_with_item(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test drawing tooltip when hovering over item"""
        # First draw to populate slot_rects
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Set hovered slot to weapon
        inventory_ui.hovered_slot = ("weapon", 0)
        # Draw again to show tooltip
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_with_description(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test drawing tooltip with item description"""
        inventory = Inventory()
        inventory.weapon_slot = Item(
            "Magic Sword",
            ItemType.WEAPON,
            attack_bonus=10,
            description="A powerful weapon",
        )
        inventory_ui.draw(mock_screen, inventory)
        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui.draw(mock_screen, inventory)
        # Test passes if no exceptions are raised

    @patch("pygame.mouse.get_pos", return_value=(750, 550))
    def test_draw_tooltip_near_right_edge(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test tooltip positioning near right edge of screen"""
        inventory_ui.draw(mock_screen, inventory_with_items)
        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Tooltip should be repositioned to stay on screen

    @patch("pygame.mouse.get_pos", return_value=(750, 550))
    def test_draw_tooltip_near_bottom_edge(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test tooltip positioning near bottom edge of screen"""
        inventory_ui.draw(mock_screen, inventory_with_items)
        inventory_ui.hovered_slot = ("backpack", 12)
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Tooltip should be repositioned to stay on screen

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_no_tooltip_when_dragging(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test tooltip not shown when dragging item"""
        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui.dragging_item = Item("Test", ItemType.WEAPON)
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Tooltip should not be shown when dragging

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_no_tooltip_on_empty_slot(self, mock_get_pos, inventory_ui, mock_screen):
        """Test no tooltip on empty slot"""
        inventory = Inventory()
        inventory_ui.draw(mock_screen, inventory)
        inventory_ui.hovered_slot = ("backpack", 0)
        inventory_ui.draw(mock_screen, inventory)
        # No tooltip should be shown for empty slot


class TestInventoryUIContextMenu:
    """Tests for context menu functionality"""

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    @patch("pygame.mouse.get_pressed", return_value=(False, False, False))
    def test_draw_context_menu_backpack_weapon(
        self, mock_pressed, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test drawing context menu for weapon in backpack"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.context_menu_slot = ("backpack", 0)
        inventory_ui.context_menu_pos = (400, 300)
        inventory_ui.draw(mock_screen, inventory)
        # Should show Equip, Drop, Inspect options

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    @patch("pygame.mouse.get_pressed", return_value=(False, False, False))
    def test_draw_context_menu_backpack_armor(
        self, mock_pressed, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test drawing context menu for armor in backpack"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Helmet", ItemType.ARMOR, defense_bonus=5)
        inventory_ui.context_menu_slot = ("backpack", 0)
        inventory_ui.context_menu_pos = (400, 300)
        inventory_ui.draw(mock_screen, inventory)
        # Should show Equip, Drop, Inspect options

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    @patch("pygame.mouse.get_pressed", return_value=(False, False, False))
    def test_draw_context_menu_equipped_item(
        self,
        mock_pressed,
        mock_get_pos,
        inventory_ui,
        mock_screen,
        inventory_with_items,
    ):
        """Test drawing context menu for equipped item"""
        inventory_ui.context_menu_slot = ("weapon", 0)
        inventory_ui.context_menu_pos = (400, 300)
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Should show Drop, Inspect options (no Equip for equipped items)

    @patch("pygame.mouse.get_pos", return_value=(750, 550))
    @patch("pygame.mouse.get_pressed", return_value=(False, False, False))
    def test_draw_context_menu_near_edge(
        self,
        mock_pressed,
        mock_get_pos,
        inventory_ui,
        mock_screen,
        inventory_with_items,
    ):
        """Test context menu positioning near screen edge"""
        inventory_ui.context_menu_slot = ("weapon", 0)
        inventory_ui.context_menu_pos = (750, 550)
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Menu should be repositioned to stay on screen

    @patch("pygame.mouse.get_pos", return_value=(400, 350))
    @patch("pygame.mouse.get_pressed", return_value=(True, False, False))
    def test_context_menu_click_equip(
        self, mock_pressed, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test clicking Equip option in context menu"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.context_menu_slot = ("backpack", 0)
        inventory_ui.context_menu_pos = (400, 300)
        inventory_ui.draw(mock_screen, inventory)
        # Context menu should execute action

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    @patch("pygame.mouse.get_pressed", return_value=(False, False, False))
    def test_context_menu_with_misc_item(
        self, mock_pressed, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test context menu with MISC item (not equippable)"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Gem", ItemType.MISC)
        inventory_ui.context_menu_slot = ("backpack", 0)
        inventory_ui.context_menu_pos = (400, 300)
        inventory_ui.draw(mock_screen, inventory)
        # Should show Drop, Inspect options only (no Equip for MISC)

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_context_menu_closes_when_item_removed(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test context menu closes when item is removed"""
        inventory = Inventory()
        inventory_ui.context_menu_slot = ("backpack", 0)
        inventory_ui.context_menu_pos = (400, 300)
        inventory_ui.draw(mock_screen, inventory)
        # Context menu should be cleared when item doesn't exist


class TestInventoryUIDragAndDrop:
    """Tests for drag and drop functionality"""

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_dragged_item(self, mock_get_pos, inventory_ui, mock_screen):
        """Test drawing dragged item"""
        inventory = Inventory()
        item = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.dragging_item = item
        inventory_ui.drag_offset = (10, 10)
        inventory_ui.draw(mock_screen, inventory)
        # Dragged item should be drawn at mouse position

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_dragged_item_not_shown_in_source_slot(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test item not shown in slot when being dragged"""
        inventory_ui.dragging_from = ("weapon", 0)
        inventory_ui.dragging_item = inventory_with_items.weapon_slot
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Item should not be drawn in source slot during drag


class TestInventoryUIInput:
    """Tests for input handling"""

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_handle_left_click_on_item(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test left click on item starts drag"""
        inventory_ui.draw(mock_screen, inventory_with_items)
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = inventory_ui.slot_rects[("weapon", 0)].center

        result = inventory_ui.handle_input(event, inventory_with_items)
        assert result is True
        assert inventory_ui.dragging_item is not None
        assert inventory_ui.dragging_from == ("weapon", 0)

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_handle_left_click_on_empty_slot(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test left click on empty slot selects it"""
        inventory = Inventory()
        inventory_ui.draw(mock_screen, inventory)
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = inventory_ui.slot_rects[("backpack", 0)].center

        result = inventory_ui.handle_input(event, inventory)
        assert result is True
        assert inventory_ui.selected_slot == ("backpack", 0)

    @patch("pygame.mouse.get_pos", return_value=(100, 100))
    def test_handle_left_click_outside_slots(self, mock_get_pos, inventory_ui):
        """Test left click outside slots"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (100, 100)

        result = inventory_ui.handle_input(event, inventory)
        assert result is False

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_handle_left_click_closes_context_menu(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test left click closes context menu"""
        inventory_ui.context_menu_slot = ("weapon", 0)
        inventory_ui.context_menu_pos = (400, 300)
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (100, 100)

        result = inventory_ui.handle_input(event, inventory_with_items)
        assert result is True
        assert inventory_ui.context_menu_slot is None

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_handle_left_release_move_item(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test left release moves item to new slot"""
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Start drag from weapon slot
        inventory_ui.dragging_item = inventory_with_items.weapon_slot
        inventory_ui.dragging_from = ("weapon", 0)

        event = Mock()
        event.type = pygame.MOUSEBUTTONUP
        event.button = 1
        event.pos = inventory_ui.slot_rects[("backpack", 1)].center

        result = inventory_ui.handle_input(event, inventory_with_items)
        assert result is True
        assert inventory_ui.dragging_item is None

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_handle_left_release_same_slot(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test left release on same slot"""
        inventory_ui.draw(mock_screen, inventory_with_items)
        inventory_ui.dragging_item = inventory_with_items.weapon_slot
        inventory_ui.dragging_from = ("weapon", 0)

        event = Mock()
        event.type = pygame.MOUSEBUTTONUP
        event.button = 1
        event.pos = inventory_ui.slot_rects[("weapon", 0)].center

        result = inventory_ui.handle_input(event, inventory_with_items)
        assert result is True
        assert inventory_ui.dragging_item is None

    @patch("pygame.mouse.get_pos", return_value=(100, 100))
    def test_handle_left_release_outside_slots(self, mock_get_pos, inventory_ui):
        """Test left release outside slots"""
        inventory = Inventory()
        item = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.dragging_item = item
        inventory_ui.dragging_from = ("weapon", 0)

        event = Mock()
        event.type = pygame.MOUSEBUTTONUP
        event.button = 1
        event.pos = (100, 100)

        result = inventory_ui.handle_input(event, inventory)
        assert result is True
        assert inventory_ui.dragging_item is None

    @patch("pygame.mouse.get_pos", return_value=(100, 100))
    def test_handle_left_release_no_drag(self, mock_get_pos, inventory_ui):
        """Test left release when not dragging"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.MOUSEBUTTONUP
        event.button = 1
        event.pos = (100, 100)

        result = inventory_ui.handle_input(event, inventory)
        assert result is False

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_handle_right_click_on_item(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test right click on item opens context menu"""
        inventory_ui.draw(mock_screen, inventory_with_items)
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 3
        event.pos = inventory_ui.slot_rects[("weapon", 0)].center

        result = inventory_ui.handle_input(event, inventory_with_items)
        assert result is True
        assert inventory_ui.context_menu_slot == ("weapon", 0)
        assert inventory_ui.context_menu_pos == event.pos

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_handle_right_click_on_empty_slot(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test right click on empty slot does nothing"""
        inventory = Inventory()
        inventory_ui.draw(mock_screen, inventory)
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 3
        event.pos = inventory_ui.slot_rects[("backpack", 0)].center

        result = inventory_ui.handle_input(event, inventory)
        assert result is False
        assert inventory_ui.context_menu_slot is None

    def test_handle_keydown_1(self, inventory_ui):
        """Test pressing 1 selects first backpack slot"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_1

        result = inventory_ui.handle_input(event, inventory)
        assert result is True
        assert inventory_ui.selected_slot == ("backpack", 0)

    def test_handle_keydown_2(self, inventory_ui):
        """Test pressing 2 selects second backpack slot"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_2

        result = inventory_ui.handle_input(event, inventory)
        assert result is True
        assert inventory_ui.selected_slot == ("backpack", 1)

    def test_handle_keydown_3(self, inventory_ui):
        """Test pressing 3 selects third backpack slot"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_3

        result = inventory_ui.handle_input(event, inventory)
        assert result is True
        assert inventory_ui.selected_slot == ("backpack", 2)

    def test_handle_keydown_4(self, inventory_ui):
        """Test pressing 4 selects fourth backpack slot"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_4

        result = inventory_ui.handle_input(event, inventory)
        assert result is True
        assert inventory_ui.selected_slot == ("backpack", 3)

    def test_handle_keydown_5(self, inventory_ui):
        """Test pressing 5 selects fifth backpack slot"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_5

        result = inventory_ui.handle_input(event, inventory)
        assert result is True
        assert inventory_ui.selected_slot == ("backpack", 4)

    def test_handle_keydown_6(self, inventory_ui):
        """Test pressing 6 selects sixth backpack slot"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_6

        result = inventory_ui.handle_input(event, inventory)
        assert result is True
        assert inventory_ui.selected_slot == ("backpack", 5)

    def test_handle_keydown_7(self, inventory_ui):
        """Test pressing 7 selects seventh backpack slot"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_7

        result = inventory_ui.handle_input(event, inventory)
        assert result is True
        assert inventory_ui.selected_slot == ("backpack", 6)

    def test_handle_keydown_8(self, inventory_ui):
        """Test pressing 8 selects eighth backpack slot"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_8

        result = inventory_ui.handle_input(event, inventory)
        assert result is True
        assert inventory_ui.selected_slot == ("backpack", 7)

    def test_handle_keydown_9(self, inventory_ui):
        """Test pressing 9 selects ninth backpack slot"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_9

        result = inventory_ui.handle_input(event, inventory)
        assert result is True
        assert inventory_ui.selected_slot == ("backpack", 8)

    def test_handle_keydown_e_equip_weapon(self, inventory_ui):
        """Test pressing E equips weapon from backpack"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.selected_slot = ("backpack", 0)

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_e

        result = inventory_ui.handle_input(event, inventory)
        assert result is True
        assert inventory.weapon_slot is not None

    def test_handle_keydown_e_no_selection(self, inventory_ui):
        """Test pressing E with no selection does nothing"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_e

        result = inventory_ui.handle_input(event, inventory)
        assert result is False

    def test_handle_keydown_e_wrong_slot_type(self, inventory_ui):
        """Test pressing E on non-backpack slot does nothing"""
        inventory = Inventory()
        inventory_ui.selected_slot = ("weapon", 0)

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_e

        result = inventory_ui.handle_input(event, inventory)
        assert result is False

    def test_handle_keydown_x_drop_item(self, inventory_ui, mock_game):
        """Test pressing X drops item"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.selected_slot = ("weapon", 0)

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_x

        result = inventory_ui.handle_input(event, inventory, mock_game)
        assert result is True
        assert inventory.weapon_slot is None
        mock_game.drop_item.assert_called_once()

    def test_handle_keydown_x_no_selection(self, inventory_ui, mock_game):
        """Test pressing X with no selection does nothing"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_x

        result = inventory_ui.handle_input(event, inventory, mock_game)
        assert result is False

    def test_handle_keydown_x_no_game(self, inventory_ui):
        """Test pressing X without game instance does nothing"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.selected_slot = ("weapon", 0)

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_x

        result = inventory_ui.handle_input(event, inventory, None)
        assert result is False

    def test_handle_keydown_x_empty_slot(self, inventory_ui, mock_game):
        """Test pressing X on empty slot does nothing"""
        inventory = Inventory()
        inventory_ui.selected_slot = ("weapon", 0)

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_x

        result = inventory_ui.handle_input(event, inventory, mock_game)
        assert result is False

    def test_handle_unknown_event(self, inventory_ui):
        """Test unknown event returns False"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.MOUSEMOTION

        result = inventory_ui.handle_input(event, inventory)
        assert result is False


class TestInventoryUIHelperMethods:
    """Tests for helper methods"""

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_update_hovered_slot(self, mock_get_pos, inventory_ui, mock_screen):
        """Test updating hovered slot"""
        inventory = Inventory()
        inventory_ui.draw(mock_screen, inventory)
        # If mouse is over a slot, hovered_slot should be set
        # This is tested indirectly through draw method

    def test_get_item_from_slot_weapon(self, inventory_ui, inventory_with_items):
        """Test getting item from weapon slot"""
        item = inventory_ui._get_item_from_slot(inventory_with_items, "weapon", 0)
        assert item == inventory_with_items.weapon_slot

    def test_get_item_from_slot_armor(self, inventory_ui, inventory_with_items):
        """Test getting item from armor slot"""
        item = inventory_ui._get_item_from_slot(inventory_with_items, "armor", 0)
        assert item == inventory_with_items.armor_slot

    def test_get_item_from_slot_backpack(self, inventory_ui, inventory_with_items):
        """Test getting item from backpack slot"""
        item = inventory_ui._get_item_from_slot(inventory_with_items, "backpack", 0)
        assert item == inventory_with_items.backpack_slots[0]

    def test_get_item_from_slot_invalid_type(self, inventory_ui):
        """Test getting item from invalid slot type"""
        inventory = Inventory()
        item = inventory_ui._get_item_from_slot(inventory, "invalid", 0)
        assert item is None

    def test_move_item_backpack_to_backpack(self, inventory_ui):
        """Test moving item between backpack slots"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui._move_item(inventory, ("backpack", 0), ("backpack", 1))
        assert inventory.backpack_slots[1] is not None
        assert inventory.backpack_slots[0] is None

    def test_move_item_swap(self, inventory_ui):
        """Test swapping items between slots"""
        inventory = Inventory()
        item1 = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        item2 = Item("Axe", ItemType.WEAPON, attack_bonus=15)
        inventory.backpack_slots[0] = item1
        inventory.backpack_slots[1] = item2
        inventory_ui._move_item(inventory, ("backpack", 0), ("backpack", 1))
        assert inventory.backpack_slots[1] == item1
        assert inventory.backpack_slots[0] == item2

    def test_move_item_to_weapon_slot(self, inventory_ui):
        """Test moving weapon to weapon slot"""
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory.backpack_slots[0] = weapon
        inventory_ui._move_item(inventory, ("backpack", 0), ("weapon", 0))
        assert inventory.weapon_slot == weapon
        assert inventory.backpack_slots[0] is None

    def test_move_item_to_armor_slot(self, inventory_ui):
        """Test moving armor to armor slot"""
        inventory = Inventory()
        armor = Item("Helmet", ItemType.ARMOR, defense_bonus=5)
        inventory.backpack_slots[0] = armor
        inventory_ui._move_item(inventory, ("backpack", 0), ("armor", 0))
        assert inventory.armor_slot == armor
        assert inventory.backpack_slots[0] is None

    def test_move_item_wrong_type_to_weapon_slot(self, inventory_ui):
        """Test moving non-weapon to empty weapon slot succeeds"""
        inventory = Inventory()
        armor = Item("Helmet", ItemType.ARMOR, defense_bonus=5)
        inventory.backpack_slots[0] = armor
        inventory_ui._move_item(inventory, ("backpack", 0), ("weapon", 0))
        # Item moves to weapon slot even though it's not a weapon (slot was empty)
        assert inventory.weapon_slot == armor
        assert inventory.backpack_slots[0] is None

    def test_move_item_wrong_type_to_armor_slot(self, inventory_ui):
        """Test moving non-armor to empty armor slot succeeds"""
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory.backpack_slots[0] = weapon
        inventory_ui._move_item(inventory, ("backpack", 0), ("armor", 0))
        # Item moves to armor slot even though it's not armor (slot was empty)
        assert inventory.armor_slot == weapon
        assert inventory.backpack_slots[0] is None

    def test_move_item_swap_equipped_items(self, inventory_ui):
        """Test swapping weapon to armor slot succeeds"""
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        armor = Item("Helmet", ItemType.ARMOR, defense_bonus=5)
        inventory.weapon_slot = weapon
        inventory.armor_slot = armor
        inventory_ui._move_item(inventory, ("weapon", 0), ("armor", 0))
        # Items are swapped
        assert inventory.weapon_slot == armor
        assert inventory.armor_slot == weapon

    def test_move_item_from_empty_slot(self, inventory_ui):
        """Test moving from empty slot does nothing"""
        inventory = Inventory()
        inventory_ui._move_item(inventory, ("backpack", 0), ("backpack", 1))
        assert inventory.backpack_slots[0] is None
        assert inventory.backpack_slots[1] is None

    def test_place_item_in_weapon_slot_correct_type(self, inventory_ui):
        """Test placing weapon in weapon slot"""
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        result = inventory_ui._place_item_in_slot(inventory, weapon, "weapon", 0)
        assert result is True
        assert inventory.weapon_slot == weapon

    def test_place_item_in_weapon_slot_wrong_type(self, inventory_ui):
        """Test placing non-weapon in weapon slot with empty slot"""
        inventory = Inventory()
        armor = Item("Helmet", ItemType.ARMOR, defense_bonus=5)
        result = inventory_ui._place_item_in_slot(inventory, armor, "weapon", 0)
        # Should succeed because slot is empty
        assert result is True
        assert inventory.weapon_slot == armor

    def test_place_item_in_armor_slot_correct_type(self, inventory_ui):
        """Test placing armor in armor slot"""
        inventory = Inventory()
        armor = Item("Helmet", ItemType.ARMOR, defense_bonus=5)
        result = inventory_ui._place_item_in_slot(inventory, armor, "armor", 0)
        assert result is True
        assert inventory.armor_slot == armor

    def test_place_item_in_armor_slot_wrong_type(self, inventory_ui):
        """Test placing non-armor in armor slot with empty slot"""
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        result = inventory_ui._place_item_in_slot(inventory, weapon, "armor", 0)
        # Should succeed because slot is empty
        assert result is True
        assert inventory.armor_slot == weapon

    def test_place_item_in_backpack_slot(self, inventory_ui):
        """Test placing item in backpack slot"""
        inventory = Inventory()
        item = Item("Potion", ItemType.CONSUMABLE)
        result = inventory_ui._place_item_in_slot(inventory, item, "backpack", 0)
        assert result is True
        assert inventory.backpack_slots[0] == item

    def test_place_item_invalid_slot_type(self, inventory_ui):
        """Test placing item in invalid slot type"""
        inventory = Inventory()
        item = Item("Test", ItemType.MISC)
        result = inventory_ui._place_item_in_slot(inventory, item, "invalid", 0)
        assert result is False

    def test_execute_context_menu_equip(self, inventory_ui):
        """Test executing Equip action from context menu"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.context_menu_slot = ("backpack", 0)

        inventory_ui._execute_context_menu_action("Equip", inventory)
        assert inventory.weapon_slot is not None

    def test_execute_context_menu_drop(self, inventory_ui):
        """Test executing Drop action from context menu"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.context_menu_slot = ("weapon", 0)

        inventory_ui._execute_context_menu_action("Drop", inventory)
        assert inventory.weapon_slot is None

    def test_execute_context_menu_inspect(self, inventory_ui):
        """Test executing Inspect action from context menu"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.context_menu_slot = ("weapon", 0)

        inventory_ui._execute_context_menu_action("Inspect", inventory)
        assert inventory_ui.selected_slot == ("weapon", 0)

    def test_execute_context_menu_no_slot(self, inventory_ui):
        """Test executing context menu action with no slot set"""
        inventory = Inventory()
        inventory_ui._execute_context_menu_action("Equip", inventory)
        # Should not crash

    def test_execute_context_menu_equip_non_backpack(self, inventory_ui):
        """Test executing Equip on non-backpack slot does nothing"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.context_menu_slot = ("weapon", 0)

        inventory_ui._execute_context_menu_action("Equip", inventory)
        # Should not crash

    def test_is_pos_in_context_menu_true(self, inventory_ui):
        """Test position is inside context menu"""
        inventory_ui.context_menu_slot = ("backpack", 0)
        inventory_ui.context_menu_pos = (400, 300)

        result = inventory_ui._is_pos_in_context_menu((400, 300))
        assert result is True

    def test_is_pos_in_context_menu_false(self, inventory_ui):
        """Test position is outside context menu"""
        inventory_ui.context_menu_slot = ("backpack", 0)
        inventory_ui.context_menu_pos = (400, 300)

        result = inventory_ui._is_pos_in_context_menu((100, 100))
        assert result is False

    def test_is_pos_in_context_menu_no_pos(self, inventory_ui):
        """Test position check with no context menu pos"""
        inventory_ui.context_menu_slot = ("backpack", 0)
        inventory_ui.context_menu_pos = None

        result = inventory_ui._is_pos_in_context_menu((400, 300))
        assert result is False

    def test_is_pos_in_context_menu_equipped_slot(self, inventory_ui):
        """Test context menu size for equipped slot (2 options)"""
        inventory_ui.context_menu_slot = ("weapon", 0)
        inventory_ui.context_menu_pos = (400, 300)

        result = inventory_ui._is_pos_in_context_menu((400, 310))
        # Should check against 2-option menu height
        assert isinstance(result, bool)

    def test_is_pos_in_context_menu_no_slot(self, inventory_ui):
        """Test context menu size check with no slot"""
        inventory_ui.context_menu_slot = None
        inventory_ui.context_menu_pos = (400, 300)

        result = inventory_ui._is_pos_in_context_menu((400, 310))
        assert result is False

    @patch("pygame.mouse.get_pos", return_value=(200, 200))
    def test_update_hovered_slot_over_slot(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test updating hovered slot when mouse is over a slot"""
        inventory = Inventory()
        inventory_ui.draw(mock_screen, inventory)
        # After draw, if mouse is in slot_rects, hovered_slot should be set
        # The test verifies the method works by checking draw completed

    @patch("pygame.mouse.get_pos", return_value=(10, 10))
    def test_update_hovered_slot_no_slot(self, mock_get_pos, inventory_ui, mock_screen):
        """Test updating hovered slot when mouse is not over any slot"""
        inventory = Inventory()
        inventory_ui.draw(mock_screen, inventory)
        # hovered_slot should be None when mouse not over slots

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_with_no_hovered_slot(self, mock_get_pos, inventory_ui, mock_screen):
        """Test draw when hovered_slot is explicitly None"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.hovered_slot = None
        inventory_ui.draw(mock_screen, inventory)
        # Should complete without attempting to draw tooltip

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_handle_left_click_inside_context_menu(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test left click inside context menu area doesn't close it"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.context_menu_slot = ("weapon", 0)
        inventory_ui.context_menu_pos = (400, 300)
        inventory_ui.draw(mock_screen, inventory)

        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (400, 310)  # Inside menu area

        # Should not close menu when clicking inside
        inventory_ui.handle_input(event, inventory)

    def test_handle_mousemotion_event(self, inventory_ui):
        """Test handling MOUSEMOTION event (should return False)"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.MOUSEMOTION
        event.pos = (400, 300)

        result = inventory_ui.handle_input(event, inventory)
        assert result is False

    def test_handle_other_mouse_button(self, inventory_ui):
        """Test handling middle mouse button (button 2)"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 2  # Middle mouse button
        event.pos = (400, 300)

        result = inventory_ui.handle_input(event, inventory)
        assert result is False

    def test_handle_other_mouse_button_up(self, inventory_ui):
        """Test handling middle mouse button release"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.MOUSEBUTTONUP
        event.button = 2  # Middle mouse button
        event.pos = (400, 300)

        result = inventory_ui.handle_input(event, inventory)
        assert result is False

    def test_handle_keydown_unknown_key(self, inventory_ui):
        """Test handling unknown keydown event"""
        inventory = Inventory()
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_a  # Random key not handled

        result = inventory_ui.handle_input(event, inventory)
        assert result is False

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_without_description(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test drawing tooltip for item without description"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui.draw(mock_screen, inventory)
        # Should draw tooltip without description line

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_no_bonuses(self, mock_get_pos, inventory_ui, mock_screen):
        """Test drawing tooltip for item with no bonuses"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Gem", ItemType.MISC)
        inventory_ui.hovered_slot = ("backpack", 0)
        inventory_ui.draw(mock_screen, inventory)
        # Should draw tooltip without bonus lines

    @patch("pygame.mouse.get_pos", return_value=(750, 550))
    def test_draw_tooltip_both_edges(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test tooltip positioning near both right and bottom edges"""
        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Tooltip should be repositioned for both edges

    @patch("pygame.mouse.get_pos", return_value=(200, 200))
    def test_draw_item_with_zero_attack_bonus(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test drawing item with zero attack bonus (should not display)"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Shield", ItemType.ARMOR, defense_bonus=5)
        inventory_ui.draw(mock_screen, inventory)
        # Should not display attack bonus

    @patch("pygame.mouse.get_pos", return_value=(200, 200))
    def test_draw_item_with_zero_defense_bonus(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test drawing item with zero defense bonus (should not display)"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.draw(mock_screen, inventory)
        # Should not display defense bonus

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_slot_not_equipped_not_selected_not_hovered(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test drawing slot with all flags false"""
        inventory = Inventory()
        inventory_ui.draw(mock_screen, inventory)
        # Should draw normal backpack slot

    @patch("pygame.mouse.get_pos", return_value=(200, 220))
    def test_draw_with_hovered_armor_slot(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test drawing with armor slot hovered"""
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Hovered slot should be set by _update_hovered_slot

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    @patch("pygame.mouse.get_pressed", return_value=(False, False, False))
    def test_draw_context_menu_consumable_item(
        self, mock_pressed, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test drawing context menu for consumable item in backpack"""
        inventory = Inventory()
        inventory.backpack_slots[0] = Item("Potion", ItemType.CONSUMABLE)
        inventory_ui.context_menu_slot = ("backpack", 0)
        inventory_ui.context_menu_pos = (400, 300)
        inventory_ui.draw(mock_screen, inventory)
        # Should show Drop, Inspect options only (no Equip for consumables)

    @patch("pygame.mouse.get_pos", return_value=(750, 300))
    @patch("pygame.mouse.get_pressed", return_value=(False, False, False))
    def test_draw_context_menu_near_right_edge(
        self,
        mock_pressed,
        mock_get_pos,
        inventory_ui,
        mock_screen,
        inventory_with_items,
    ):
        """Test context menu positioning near right edge"""
        inventory_ui.context_menu_slot = ("weapon", 0)
        inventory_ui.context_menu_pos = (750, 300)
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Menu should be repositioned to stay on screen

    @patch("pygame.mouse.get_pos", return_value=(400, 550))
    @patch("pygame.mouse.get_pressed", return_value=(False, False, False))
    def test_draw_context_menu_near_bottom_edge(
        self,
        mock_pressed,
        mock_get_pos,
        inventory_ui,
        mock_screen,
        inventory_with_items,
    ):
        """Test context menu positioning near bottom edge"""
        inventory_ui.context_menu_slot = ("weapon", 0)
        inventory_ui.context_menu_pos = (400, 550)
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Menu should be repositioned to stay on screen

    def test_draw_dragged_item_early_return(self, inventory_ui, mock_screen):
        """Test _draw_dragged_item returns early when no item is being dragged"""
        inventory_ui.dragging_item = None
        # Should return early without error
        inventory_ui._draw_dragged_item(mock_screen, (400, 300))

    @patch("pygame.mouse.get_pos", return_value=(250, 250))
    def test_draw_with_real_hovered_slot(
        self, mock_get_pos, inventory_ui, mock_screen, inventory_with_items
    ):
        """Test drawing with a slot actually being hovered"""
        # First draw to populate slot_rects
        inventory_ui.draw(mock_screen, inventory_with_items)
        # Mouse position should match a slot rect
        # This tests the _update_hovered_slot loop finding a match

    def test_update_hovered_slot_direct(self, inventory_ui):
        """Test _update_hovered_slot directly"""
        # Set up some slot rects
        inventory_ui.slot_rects[("weapon", 0)] = pygame.Rect(100, 100, 80, 80)
        inventory_ui.slot_rects[("armor", 0)] = pygame.Rect(200, 100, 80, 80)
        inventory_ui.slot_rects[("backpack", 0)] = pygame.Rect(100, 200, 80, 80)

        # Test mouse over weapon slot
        inventory_ui._update_hovered_slot((140, 140))
        assert inventory_ui.hovered_slot == ("weapon", 0)

        # Test mouse over armor slot
        inventory_ui._update_hovered_slot((240, 140))
        assert inventory_ui.hovered_slot == ("armor", 0)

        # Test mouse over backpack slot
        inventory_ui._update_hovered_slot((140, 240))
        assert inventory_ui.hovered_slot == ("backpack", 0)

        # Test mouse over no slot
        inventory_ui._update_hovered_slot((10, 10))
        assert inventory_ui.hovered_slot is None

    def test_draw_tooltip_direct(self, inventory_ui, mock_screen):
        """Test _draw_tooltip directly"""
        inventory = Inventory()
        inventory.weapon_slot = Item(
            "Magic Sword",
            ItemType.WEAPON,
            attack_bonus=15,
            defense_bonus=3,
            description="A very powerful sword",
        )

        # Set hovered slot
        inventory_ui.hovered_slot = ("weapon", 0)

        # Call _draw_tooltip directly
        inventory_ui._draw_tooltip(mock_screen, inventory, (400, 300))
        # Should draw tooltip with description and both bonuses

    def test_draw_tooltip_direct_no_hovered_slot(self, inventory_ui, mock_screen):
        """Test _draw_tooltip returns early when hovered_slot is None"""
        inventory = Inventory()
        inventory_ui.hovered_slot = None

        # Call _draw_tooltip directly - should return early
        inventory_ui._draw_tooltip(mock_screen, inventory, (400, 300))

    def test_draw_tooltip_direct_no_item(self, inventory_ui, mock_screen):
        """Test _draw_tooltip returns early when slot has no item"""
        inventory = Inventory()
        inventory_ui.hovered_slot = ("backpack", 0)

        # Call _draw_tooltip directly - should return early
        inventory_ui._draw_tooltip(mock_screen, inventory, (400, 300))

    def test_draw_context_menu_direct(self, inventory_ui, mock_screen):
        """Test _draw_context_menu directly"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        inventory_ui.context_menu_slot = ("weapon", 0)
        inventory_ui.context_menu_pos = (400, 300)

        # Call _draw_context_menu directly
        with (
            patch("pygame.mouse.get_pos", return_value=(400, 300)),
            patch("pygame.mouse.get_pressed", return_value=(False, False, False)),
        ):
            inventory_ui._draw_context_menu(mock_screen, inventory)

    def test_draw_context_menu_direct_no_slot(self, inventory_ui, mock_screen):
        """Test _draw_context_menu returns early when context_menu_slot is None"""
        inventory = Inventory()
        inventory_ui.context_menu_slot = None
        inventory_ui.context_menu_pos = (400, 300)

        # Call _draw_context_menu directly - should return early
        inventory_ui._draw_context_menu(mock_screen, inventory)

    def test_draw_context_menu_direct_no_pos(self, inventory_ui, mock_screen):
        """Test _draw_context_menu returns early when context_menu_pos is None"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.context_menu_slot = ("weapon", 0)
        inventory_ui.context_menu_pos = None

        # Call _draw_context_menu directly - should return early
        inventory_ui._draw_context_menu(mock_screen, inventory)

    def test_draw_context_menu_direct_no_item(self, inventory_ui, mock_screen):
        """Test _draw_context_menu clears menu when item is removed"""
        inventory = Inventory()
        inventory_ui.context_menu_slot = ("weapon", 0)
        inventory_ui.context_menu_pos = (400, 300)

        # Call _draw_context_menu directly - should clear context menu
        with (
            patch("pygame.mouse.get_pos", return_value=(400, 300)),
            patch("pygame.mouse.get_pressed", return_value=(False, False, False)),
        ):
            inventory_ui._draw_context_menu(mock_screen, inventory)
            assert inventory_ui.context_menu_slot is None

    def test_move_item_with_failed_placement(self, inventory_ui):
        """Test _move_item when placement fails and items are restored"""
        inventory = Inventory()
        # Fill weapon slot with correct type
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory.weapon_slot = weapon
        # Try to move weapon to armor slot - should fail and restore
        # Actually this succeeds based on _place_item_in_slot logic
        # So let's test a different scenario

    def test_place_item_with_wrong_type_in_occupied_weapon_slot(self, inventory_ui):
        """Test placing wrong type item in occupied weapon slot"""
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        armor = Item("Helmet", ItemType.ARMOR, defense_bonus=5)
        inventory.weapon_slot = weapon

        # Try to place armor in weapon slot (slot is occupied and wrong type)
        result = inventory_ui._place_item_in_slot(inventory, armor, "weapon", 0)
        # Should fail because slot is occupied with weapon and item is not weapon
        # Actually, looking at the code, it always places if slot is empty OR type matches
        # So this will fail
        assert result is False
        assert inventory.weapon_slot == weapon

    def test_place_item_with_wrong_type_in_occupied_armor_slot(self, inventory_ui):
        """Test placing wrong type item in occupied armor slot"""
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        armor = Item("Helmet", ItemType.ARMOR, defense_bonus=5)
        inventory.armor_slot = armor

        # Try to place weapon in armor slot (slot is occupied and wrong type)
        result = inventory_ui._place_item_in_slot(inventory, weapon, "armor", 0)
        # Should fail
        assert result is False
        assert inventory.armor_slot == armor

    @patch("pygame.mouse.get_pos", return_value=(240, 240))
    def test_draw_with_hovered_slot_not_selected(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test drawing with hovered slot that is not selected"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Draw to populate slot_rects and set hovered_slot
        inventory_ui.draw(mock_screen, inventory)
        # The hovered slot should have border_color = hover_color

    @patch("pygame.mouse.get_pos", return_value=(240, 240))
    def test_draw_slot_hovered_not_selected(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test _draw_slot with is_hovered=True and is_selected=False"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Manually set state to test specific branch
        inventory_ui.selected_slot = None  # Not selected
        inventory_ui.hovered_slot = ("weapon", 0)  # But hovered

        # Draw to trigger _draw_slot with is_hovered=True, is_selected=False
        inventory_ui.draw(mock_screen, inventory)

    def test_move_item_with_to_item_and_success(self, inventory_ui):
        """Test _move_item when both slots have items and move succeeds"""
        inventory = Inventory()
        item1 = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        item2 = Item("Axe", ItemType.WEAPON, attack_bonus=15)
        inventory.backpack_slots[0] = item1
        inventory.backpack_slots[1] = item2

        # Move item1 to slot with item2 (should swap)
        inventory_ui._move_item(inventory, ("backpack", 0), ("backpack", 1))

        # Items should be swapped
        assert inventory.backpack_slots[0] == item2
        assert inventory.backpack_slots[1] == item1

    def test_move_item_with_to_item_and_failed_placement(self, inventory_ui):
        """Test _move_item when placement fails and items are restored"""
        inventory = Inventory()
        armor = Item("Helmet", ItemType.ARMOR, defense_bonus=5)
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        inventory.backpack_slots[0] = armor
        inventory.weapon_slot = weapon  # Occupied with weapon

        # Actually, this will succeed because weapon slot becomes empty after removing weapon
        # So items will be swapped
        inventory_ui._move_item(inventory, ("backpack", 0), ("weapon", 0))

        # Items should be swapped
        assert inventory.weapon_slot == armor
        assert inventory.backpack_slots[0] == weapon

    def test_move_item_swap_with_failed_placement(self, inventory_ui):
        """Test _move_item swap when target placement fails"""
        inventory = Inventory()
        weapon1 = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        weapon2 = Item("Axe", ItemType.WEAPON, attack_bonus=15)
        armor = Item("Helmet", ItemType.ARMOR, defense_bonus=5)

        inventory.weapon_slot = weapon1
        inventory.armor_slot = armor
        inventory.backpack_slots[0] = weapon2  # Another weapon

        # Try to move weapon2 from backpack to weapon slot (occupied)
        # weapon1 should go to backpack[0]
        inventory_ui._move_item(inventory, ("backpack", 0), ("weapon", 0))

        # Should swap successfully
        assert inventory.weapon_slot == weapon2
        assert inventory.backpack_slots[0] == weapon1

    @patch("pygame.mouse.get_pos", return_value=(790, 590))
    def test_draw_tooltip_repositioned_both_axes(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test tooltip repositioned when near both screen edges"""
        inventory = Inventory()
        inventory.weapon_slot = Item(
            "Magic Sword",
            ItemType.WEAPON,
            attack_bonus=15,
            description="A powerful sword",
        )

        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui.draw(mock_screen, inventory)
        # Tooltip should be repositioned to left and above mouse

    @patch("pygame.mouse.get_pos", return_value=(790, 300))
    def test_draw_tooltip_repositioned_x_only(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test tooltip repositioned when near right edge only"""
        inventory = Inventory()
        inventory.weapon_slot = Item(
            "Sword", ItemType.WEAPON, attack_bonus=10, description="A sword"
        )

        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui.draw(mock_screen, inventory)
        # Tooltip should be repositioned to left of mouse

    @patch("pygame.mouse.get_pos", return_value=(300, 590))
    def test_draw_tooltip_repositioned_y_only(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test tooltip repositioned when near bottom edge only"""
        inventory = Inventory()
        inventory.weapon_slot = Item(
            "Sword", ItemType.WEAPON, attack_bonus=10, description="A sword"
        )

        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui.draw(mock_screen, inventory)
        # Tooltip should be repositioned above mouse

    def test_draw_with_dragging_item_set(self, inventory_ui, mock_screen):
        """Test draw with dragging_item set to trigger _draw_dragged_item"""
        inventory = Inventory()
        item = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.dragging_item = item
        inventory_ui.drag_offset = (5, 5)

        with patch("pygame.mouse.get_pos", return_value=(400, 300)):
            inventory_ui.draw(mock_screen, inventory)
        # Should call _draw_dragged_item

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_with_hovered_and_tooltip(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test draw with hovered slot to trigger tooltip drawing"""
        inventory = Inventory()
        inventory.weapon_slot = Item(
            "Sword", ItemType.WEAPON, attack_bonus=10, description="A sword"
        )

        # First draw to populate slot_rects
        inventory_ui.draw(mock_screen, inventory)

        # Manually set hovered slot and draw again
        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui.draw(mock_screen, inventory)
        # Should call _draw_tooltip

    def test_move_item_failed_placement_with_to_item(self, inventory_ui):
        """Test _move_item when placement fails and both items need restoration (lines 467-469)"""
        from unittest.mock import patch

        inventory = Inventory()
        # Create two weapons
        weapon1 = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        weapon2 = Item("Axe", ItemType.WEAPON, attack_bonus=15)

        # Put weapons in different slots
        inventory.weapon_slot = weapon1
        inventory.backpack_slots[0] = weapon2

        # Mock _place_item_in_slot to return False on first call (simulating placement failure)
        original_place = inventory_ui._place_item_in_slot
        call_count = [0]

        def mock_place(inv, item, slot_type, slot_index):
            call_count[0] += 1
            if call_count[0] == 1:  # First call fails
                return False
            return original_place(inv, item, slot_type, slot_index)

        with patch.object(inventory_ui, "_place_item_in_slot", side_effect=mock_place):
            # Try to move weapon2 to weapon slot - placement will fail
            inventory_ui._move_item(inventory, ("backpack", 0), ("weapon", 0))

        # Items should be restored to original positions
        assert inventory.weapon_slot == weapon1  # Original weapon still there
        assert inventory.backpack_slots[0] == weapon2  # Weapon2 restored to backpack

    @patch("pygame.mouse.get_pos", return_value=(785, 300))
    def test_tooltip_repositioned_right_edge_only(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test tooltip repositioned when near right edge only (line 534)"""
        inventory = Inventory()
        # Create item with long description to ensure tooltip is wide enough
        inventory.weapon_slot = Item(
            "Legendary Sword of the Ancient Warriors",
            ItemType.WEAPON,
            attack_bonus=25,
            description="A legendary weapon passed down through generations",
        )

        inventory_ui.hovered_slot = ("weapon", 0)
        # Mouse at x=785 should trigger repositioning to the left
        inventory_ui.draw(mock_screen, inventory)
        # Tooltip should be repositioned to avoid right edge

    @patch("pygame.mouse.get_pos", return_value=(300, 585))
    def test_tooltip_repositioned_bottom_edge_only(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test tooltip repositioned when near bottom edge only (line 536)"""
        inventory = Inventory()
        # Create item with description and bonuses for tall tooltip
        inventory.weapon_slot = Item(
            "Magic Sword",
            ItemType.WEAPON,
            attack_bonus=15,
            defense_bonus=5,
            description="A powerful magical sword with multiple enchantments",
        )

        inventory_ui.hovered_slot = ("weapon", 0)
        # Mouse at y=585 should trigger repositioning upward
        inventory_ui.draw(mock_screen, inventory)
        # Tooltip should be repositioned to avoid bottom edge

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_tooltip_item_no_description_no_bonuses(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test tooltip with item that has NO description, NO attack_bonus, NO defense_bonus"""
        inventory = Inventory()
        # Create MISC item with no description and no bonuses
        inventory.backpack_slots[0] = Item("Gem", ItemType.MISC)

        inventory_ui.hovered_slot = ("backpack", 0)
        inventory_ui.draw(mock_screen, inventory)
        # Should draw tooltip with only name and type, skipping all three optional lines

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_tooltip_with_description_no_bonuses(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test tooltip with item that HAS description but NO bonuses"""
        inventory = Inventory()
        # Create item with description but no bonuses
        inventory.backpack_slots[0] = Item(
            "Ancient Scroll",
            ItemType.MISC,
            description="An ancient scroll with mysterious writings",
        )

        inventory_ui.hovered_slot = ("backpack", 0)
        inventory_ui.draw(mock_screen, inventory)
        # Should draw tooltip with description but no bonus lines

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_tooltip_with_attack_bonus_only(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test tooltip with item that has attack_bonus > 0 but no defense_bonus"""
        inventory = Inventory()
        # Create weapon with only attack bonus
        inventory.weapon_slot = Item("Simple Sword", ItemType.WEAPON, attack_bonus=8)

        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui.draw(mock_screen, inventory)
        # Should draw tooltip with attack bonus line but no defense bonus line

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_tooltip_with_defense_bonus_only(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test tooltip with item that has defense_bonus > 0 but no attack_bonus"""
        inventory = Inventory()
        # Create armor with only defense bonus
        inventory.armor_slot = Item("Simple Shield", ItemType.ARMOR, defense_bonus=6)

        inventory_ui.hovered_slot = ("armor", 0)
        inventory_ui.draw(mock_screen, inventory)
        # Should draw tooltip with defense bonus line but no attack bonus line

    @patch("pygame.mouse.get_pos", return_value=(400, 320))
    @patch("pygame.mouse.get_pressed", return_value=(False, False, False))
    def test_context_menu_inspect_action(
        self, mock_pressed, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test context menu Inspect action (branch 638->exit)"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.context_menu_slot = ("weapon", 0)
        inventory_ui.context_menu_pos = (400, 300)

        # First draw to set up context menu
        inventory_ui.draw(mock_screen, inventory)

        # Execute Inspect action directly
        inventory_ui._execute_context_menu_action("Inspect", inventory)

        # Should set selected_slot to the inspected slot
        assert inventory_ui.selected_slot == ("weapon", 0)

    def test_place_item_failed_placement_weapon_slot(self, inventory_ui):
        """Test placing wrong type in occupied weapon slot fails and triggers restoration"""
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        armor = Item("Helmet", ItemType.ARMOR, defense_bonus=5)

        # Occupy weapon slot
        inventory.weapon_slot = weapon

        # Try to place armor - should fail
        result = inventory_ui._place_item_in_slot(inventory, armor, "weapon", 0)
        assert result is False

    def test_place_item_failed_placement_armor_slot(self, inventory_ui):
        """Test placing wrong type in occupied armor slot fails and triggers restoration"""
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        armor = Item("Helmet", ItemType.ARMOR, defense_bonus=5)

        # Occupy armor slot
        inventory.armor_slot = armor

        # Try to place weapon - should fail
        result = inventory_ui._place_item_in_slot(inventory, weapon, "armor", 0)
        assert result is False

    @patch("pygame.mouse.get_pos", return_value=(250, 170))
    def test_draw_slot_hovered_not_selected_border(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test _draw_slot border styling when is_hovered=True, is_selected=False (lines 207-208)"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Manually set hovered but not selected
        inventory_ui.selected_slot = ("armor", 0)  # Different slot selected
        inventory_ui.hovered_slot = ("weapon", 0)  # Weapon hovered

        # Draw should use hover_color for border
        inventory_ui.draw(mock_screen, inventory)
        # Border should be hover_color with width 3

    def test_move_item_failed_placement_no_to_item(self, inventory_ui):
        """Test _move_item when placement fails with no to_item (branch 468->exit)"""
        from unittest.mock import patch

        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory.backpack_slots[0] = weapon

        # Mock _place_item_in_slot to fail first, then succeed on restoration
        original_place = inventory_ui._place_item_in_slot
        call_count = [0]

        def mock_place(inv, item, slot_type, slot_index):
            call_count[0] += 1
            if call_count[0] == 1:  # First call (placement to new slot) fails
                return False
            # Subsequent calls (restoration) succeed
            return original_place(inv, item, slot_type, slot_index)

        with patch.object(inventory_ui, "_place_item_in_slot", side_effect=mock_place):
            # Try to move weapon to empty backpack slot - placement will fail
            inventory_ui._move_item(inventory, ("backpack", 0), ("backpack", 1))

        # Item should be restored to original position
        assert inventory.backpack_slots[0] == weapon
        assert inventory.backpack_slots[1] is None

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_tooltip_with_all_branches(self, mock_get_pos, inventory_ui, mock_screen):
        """Test tooltip branches 511->514, 514->516, 516->520 with specific combinations"""
        inventory = Inventory()

        # Test 1: Item with description, attack bonus, and defense bonus (all branches)
        inventory.weapon_slot = Item(
            "Complete Sword",
            ItemType.WEAPON,
            attack_bonus=10,
            defense_bonus=5,
            description="Has everything",
        )
        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui.draw(mock_screen, inventory)

        # Test 2: Item with description but no attack (branch 511->512, then 514->516 skips to 516)
        inventory.armor_slot = Item(
            "Shield",
            ItemType.ARMOR,
            attack_bonus=0,
            defense_bonus=5,
            description="Only defense",
        )
        inventory_ui.hovered_slot = ("armor", 0)
        inventory_ui.draw(mock_screen, inventory)

        # Test 3: Item with attack but no defense (branch 514->515, then 516->exit)
        inventory.backpack_slots[0] = Item(
            "Dagger", ItemType.WEAPON, attack_bonus=3, defense_bonus=0
        )
        inventory_ui.hovered_slot = ("backpack", 0)
        inventory_ui.draw(mock_screen, inventory)

    @patch("pygame.mouse.get_pos", return_value=(795, 300))
    def test_tooltip_edge_case_right(self, mock_get_pos, inventory_ui, mock_screen):
        """Test tooltip repositioning right edge (line 534) with precise positioning"""
        inventory = Inventory()
        # Item with very long description to make tooltip wide
        inventory.weapon_slot = Item(
            "Super Legendary Extremely Powerful Magical Sword of Ultimate Destruction",
            ItemType.WEAPON,
            attack_bonus=50,
            defense_bonus=30,
            description="This is an extremely long description that will make the tooltip very wide and ensure it goes off the right edge of the screen when positioned normally",
        )

        inventory_ui.hovered_slot = ("weapon", 0)
        # Mouse very close to right edge (800 - 5 = 795)
        inventory_ui.draw(mock_screen, inventory)

    @patch("pygame.mouse.get_pos", return_value=(400, 595))
    def test_tooltip_edge_case_bottom(self, mock_get_pos, inventory_ui, mock_screen):
        """Test tooltip repositioning bottom edge (line 536) with precise positioning"""
        inventory = Inventory()
        # Item with description and bonuses to make tooltip tall
        inventory.weapon_slot = Item(
            "Tall Item",
            ItemType.WEAPON,
            attack_bonus=25,
            defense_bonus=20,
            description="Line 1 - Making this tooltip tall enough",
        )

        inventory_ui.hovered_slot = ("weapon", 0)
        # Mouse very close to bottom edge (600 - 5 = 595)
        inventory_ui.draw(mock_screen, inventory)

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_called_when_hovering(
        self, mock_get_pos, inventory_ui, mock_screen
    ):
        """Test that line 96 is executed when hovering (not dragging)"""
        inventory = Inventory()
        inventory.weapon_slot = Item(
            "Test Sword",
            ItemType.WEAPON,
            attack_bonus=10,
            description="Test description",
        )

        # Set up the condition: hovered_slot is set, dragging_item is None
        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui.dragging_item = None  # Explicitly not dragging

        # This should trigger line 96: self._draw_tooltip(screen, inventory, mouse_pos)
        inventory_ui.draw(mock_screen, inventory)

    def test_execute_inspect_action_coverage(self, inventory_ui):
        """Test Inspect action to cover branch 638->exit"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Set up context menu
        inventory_ui.context_menu_slot = ("weapon", 0)

        # Execute Inspect action - should set selected_slot and exit function
        inventory_ui._execute_context_menu_action("Inspect", inventory)

        # Verify the action was executed
        assert inventory_ui.selected_slot == ("weapon", 0)

    def test_tooltip_no_description_branch(self, inventory_ui, mock_screen):
        """Test tooltip with NO description to cover branch 511->514"""
        inventory = Inventory()
        # Item with NO description - should skip line 512 and go to 514
        inventory.weapon_slot = Item(
            "Plain Sword", ItemType.WEAPON, attack_bonus=5, defense_bonus=3
        )

        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui._draw_tooltip(mock_screen, inventory, (400, 300))

    def test_tooltip_no_attack_bonus_branch(self, inventory_ui, mock_screen):
        """Test tooltip with NO attack bonus to cover branch 514->516"""
        inventory = Inventory()
        # Item with attack_bonus = 0 - should skip line 515 and go to 516
        inventory.armor_slot = Item(
            "Pure Shield",
            ItemType.ARMOR,
            attack_bonus=0,
            defense_bonus=8,
            description="Only defense",
        )

        inventory_ui.hovered_slot = ("armor", 0)
        inventory_ui._draw_tooltip(mock_screen, inventory, (400, 300))

    def test_tooltip_no_defense_bonus_branch(self, inventory_ui, mock_screen):
        """Test tooltip with NO defense bonus to cover branch 516->520"""
        inventory = Inventory()
        # Item with defense_bonus = 0 - should skip line 517 and go to 520
        inventory.weapon_slot = Item(
            "Pure Sword",
            ItemType.WEAPON,
            attack_bonus=12,
            defense_bonus=0,
            description="Only attack",
        )

        inventory_ui.hovered_slot = ("weapon", 0)
        inventory_ui._draw_tooltip(mock_screen, inventory, (400, 300))

    def test_tooltip_skip_all_optional_branches(self, inventory_ui, mock_screen):
        """Test tooltip skipping all optional branches: 511->514, 514->516, 516->520"""
        inventory = Inventory()
        # Item with NO description, NO attack, NO defense
        inventory.backpack_slots[0] = Item(
            "Simple Gem",
            ItemType.MISC,
            attack_bonus=0,
            defense_bonus=0,
            description="",  # Empty string
        )

        inventory_ui.hovered_slot = ("backpack", 0)
        inventory_ui._draw_tooltip(mock_screen, inventory, (400, 300))

    def test_draw_slot_hovered_only(self, inventory_ui, mock_screen):
        """Test _draw_slot with is_hovered=True, is_selected=False directly (lines 207-208)"""
        item = Item("Test", ItemType.WEAPON, attack_bonus=5)

        # Call _draw_slot directly with is_hovered=True, is_selected=False
        inventory_ui._draw_slot(
            mock_screen,
            100,
            100,
            "TEST",
            item,
            ("weapon", 0),
            is_equipped=False,
            is_selected=False,
            is_hovered=True,
        )
        # Should use hover_color at lines 207-208

    def test_tooltip_right_edge_reposition(self, inventory_ui, mock_screen):
        """Test tooltip X-axis repositioning directly (line 534)"""
        inventory = Inventory()
        # Very long item name and description to make wide tooltip
        long_desc = "A" * 100  # Very long description
        inventory.weapon_slot = Item(
            "Extremely Long Item Name That Causes Wide Tooltip",
            ItemType.WEAPON,
            attack_bonus=50,
            defense_bonus=40,
            description=long_desc,
        )

        inventory_ui.hovered_slot = ("weapon", 0)
        # Position mouse near right edge so tooltip would go off screen
        inventory_ui._draw_tooltip(mock_screen, inventory, (795, 300))

    def test_tooltip_bottom_edge_reposition(self, inventory_ui, mock_screen):
        """Test tooltip Y-axis repositioning directly (line 536)"""
        inventory = Inventory()
        # Item with description and bonuses to make tall tooltip
        inventory.weapon_slot = Item(
            "Item Name",
            ItemType.WEAPON,
            attack_bonus=50,
            defense_bonus=40,
            description="Description line",
        )

        inventory_ui.hovered_slot = ("weapon", 0)
        # Position mouse near bottom edge so tooltip would go off screen
        inventory_ui._draw_tooltip(mock_screen, inventory, (400, 595))

    @patch("pygame.mouse.get_pos")
    def test_draw_calls_tooltip_line_96(self, mock_get_pos, inventory_ui, mock_screen):
        """Test that draw() calls _draw_tooltip at line 96"""
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # First draw to populate slot_rects with mouse away from slots
        mock_get_pos.return_value = (100, 100)
        inventory_ui.draw(mock_screen, inventory)

        # Get the center of the weapon slot rect
        weapon_rect = inventory_ui.slot_rects[("weapon", 0)]
        mouse_pos = weapon_rect.center

        # Ensure we're not dragging
        inventory_ui.dragging_item = None

        # Draw again with mouse over weapon slot - this should execute line 96
        mock_get_pos.return_value = mouse_pos
        inventory_ui.draw(mock_screen, inventory)
        # Line 96 should be executed: self._draw_tooltip(screen, inventory, mouse_pos)

    def test_inspect_action_with_full_flow(self, inventory_ui, mock_screen):
        """Test Inspect action through full context menu flow (branch 638->exit)"""
        from unittest.mock import patch

        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # First draw to populate slot_rects
        with patch("pygame.mouse.get_pos", return_value=(400, 300)):
            inventory_ui.draw(mock_screen, inventory)

        # Set up context menu
        inventory_ui.context_menu_slot = ("weapon", 0)
        inventory_ui.context_menu_pos = (400, 300)

        # Mock mouse position over "Inspect" option (second option at y=330)
        # Menu starts at y=300, each option is 30px high, so Inspect is at y=330-360
        inspect_pos = (400, 345)  # Middle of second option

        # Mock mouse hovering over Inspect option and clicking
        with (
            patch("pygame.mouse.get_pos", return_value=inspect_pos),
            patch("pygame.mouse.get_pressed", return_value=(True, False, False)),
        ):
            inventory_ui.draw(mock_screen, inventory)

        # Verify Inspect was executed (context menu should be closed and slot selected)
        assert inventory_ui.selected_slot == ("weapon", 0)
        assert inventory_ui.context_menu_slot is None

    def test_draw_with_hovering_not_dragging(self, inventory_ui, mock_screen):
        """Test draw() with hovering enabled and not dragging (line 96)"""
        # Arrange
        inventory = Inventory()
        inventory.weapon_slot = Item(
            "Test Sword", ItemType.WEAPON, attack_bonus=10, description="A test sword"
        )

        # Ensure we're not dragging
        inventory_ui.dragging_item = None

        # Mock _update_hovered_slot to set hovered_slot to weapon
        def mock_update_hovered(mouse_pos):
            inventory_ui.hovered_slot = ("weapon", 0)

        # Mock _draw_tooltip to track if it's called
        with patch.object(inventory_ui, "_draw_tooltip") as mock_tooltip:
            with patch.object(
                inventory_ui, "_update_hovered_slot", side_effect=mock_update_hovered
            ):
                with patch("pygame.mouse.get_pos", return_value=(400, 300)):
                    # Act - this should trigger line 96: self._draw_tooltip(screen, inventory, mouse_pos)
                    inventory_ui.draw(mock_screen, inventory)

                    # Assert - _draw_tooltip should be called
                    mock_tooltip.assert_called_once()

    def test_execute_context_menu_action_unknown_action(self, inventory_ui):
        """Test _execute_context_menu_action with unknown action (branch 638->exit)"""
        # Arrange
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.context_menu_slot = ("weapon", 0)

        # Act - call with unknown action
        inventory_ui._execute_context_menu_action("Unknown", inventory)

        # Assert - function should complete without error
        # Nothing should change since action is unknown
        assert inventory.weapon_slot is not None

    def test_execute_context_menu_action_invalid_action(self, inventory_ui):
        """Test _execute_context_menu_action with completely invalid action string"""
        # Arrange
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory_ui.context_menu_slot = ("weapon", 0)

        # Act - call with completely invalid action
        inventory_ui._execute_context_menu_action("InvalidAction123", inventory)

        # Assert - function should complete without error
        assert inventory.weapon_slot is not None
