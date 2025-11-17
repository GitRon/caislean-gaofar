"""Tests to cover edge cases and reach 100% branch coverage."""

import pygame
import pytest
from caislean_gaofar.ui.inventory_ui import InventoryUI
from caislean_gaofar.ui.inventory_renderer import InventoryRenderer
from caislean_gaofar.ui.inventory_state import InventoryState
from caislean_gaofar.ui.shop_ui import ShopUI
from caislean_gaofar.ui.shop_state import ShopState
from caislean_gaofar.systems.inventory import Inventory
from caislean_gaofar.objects.item import Item, ItemType
from caislean_gaofar.objects.shop import Shop, ShopItem
from caislean_gaofar.entities.warrior import Warrior
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


class TestInventoryRendererEdgeCases:
    """Tests for inventory renderer edge cases"""

    def test_renderer_draw_direct_call(self, mock_screen):
        """Test calling renderer.draw() directly (covers main draw method)"""
        renderer = InventoryRenderer()
        state = InventoryState()
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Call renderer.draw() directly
        renderer.draw(mock_screen, inventory, state)
        # Should not crash

    def test_renderer_draw_with_tooltip(self, mock_screen):
        """Test renderer.draw() with tooltip (line 70)"""
        renderer = InventoryRenderer()
        state = InventoryState()
        inventory = Inventory()
        inventory.weapon_slot = Item(
            "Sword", ItemType.WEAPON, attack_bonus=10, description="A sword"
        )

        # Set up hovered slot (so tooltip is drawn)
        state.hovered_slot = ("weapon", 0)
        state.dragging_item = None  # Not dragging

        # Call renderer.draw() directly
        renderer.draw(mock_screen, inventory, state)
        # Should not crash

    def test_renderer_draw_with_context_menu(self, mock_screen):
        """Test renderer.draw() with context menu (line 74)"""
        renderer = InventoryRenderer()
        state = InventoryState()
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Set up context menu
        state.context_menu_slot = ("weapon", 0)
        state.context_menu_pos = (400, 300)

        # Call renderer.draw() directly
        renderer.draw(mock_screen, inventory, state)
        # Should not crash

    def test_renderer_draw_with_dragging(self, mock_screen):
        """Test renderer.draw() with dragging (line 78)"""
        renderer = InventoryRenderer()
        state = InventoryState()
        inventory = Inventory()

        # Set up dragging
        item = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        state.dragging_item = item
        state.dragging_from = ("weapon", 0)
        state.drag_offset = (0, 0)

        # Call renderer.draw() directly
        renderer.draw(mock_screen, inventory, state)
        # Should not crash

    def test_get_context_menu_rects_no_context_menu(self, mock_screen):
        """Test get_context_menu_rects when no context menu is open (line 449)"""
        renderer = InventoryRenderer()
        state = InventoryState()
        inventory = Inventory()

        # No context menu
        result = renderer.get_context_menu_rects(state, inventory)
        assert result == []

    def test_get_context_menu_rects_no_item(self, mock_screen):
        """Test get_context_menu_rects when slot has no item (line 455)"""
        renderer = InventoryRenderer()
        state = InventoryState()
        inventory = Inventory()

        # Open context menu on empty slot
        state.context_menu_slot = ("weapon", 0)
        state.context_menu_pos = (400, 300)

        result = renderer.get_context_menu_rects(state, inventory)
        assert result == []

    def test_get_context_menu_rects_off_screen_right(self, mock_screen):
        """Test get_context_menu_rects when menu goes off right edge (line 481)"""
        renderer = InventoryRenderer()
        state = InventoryState()
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Context menu near right edge
        state.context_menu_slot = ("weapon", 0)
        state.context_menu_pos = (790, 300)  # Near right edge (screen is 800px)

        result = renderer.get_context_menu_rects(state, inventory)
        assert len(result) > 0  # Should have options
        # Menu should be repositioned to fit on screen

    def test_get_context_menu_rects_off_screen_bottom(self, mock_screen):
        """Test get_context_menu_rects when menu goes off bottom edge (line 483)"""
        renderer = InventoryRenderer()
        state = InventoryState()
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Context menu near bottom edge
        state.context_menu_slot = ("weapon", 0)
        state.context_menu_pos = (400, 590)  # Near bottom edge (screen is 600px)

        result = renderer.get_context_menu_rects(state, inventory)
        assert len(result) > 0  # Should have options

    def test_get_context_menu_rects_consumable_item(self, mock_screen):
        """Test get_context_menu_rects with consumable item (line 462->464)"""
        renderer = InventoryRenderer()
        state = InventoryState()
        inventory = Inventory()

        # Consumable item in backpack (should NOT have Equip option)
        inventory.backpack_slots[0] = Item("Potion", ItemType.CONSUMABLE)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 300)

        result = renderer.get_context_menu_rects(state, inventory)
        # Should have Drop option only (no Equip, no Inspect)
        assert len(result) == 1

    def test_get_item_from_slot_invalid_type(self):
        """Test _get_item_from_slot with invalid slot type (line 442)"""
        renderer = InventoryRenderer()
        inventory = Inventory()

        # Invalid slot type
        result = renderer._get_item_from_slot(inventory, "invalid", 0)
        assert result is None


class TestInventoryInputHandlerEdgeCases:
    """Tests for inventory input handler edge cases"""

    def test_right_click_on_context_menu_option(self, mock_screen):
        """Test right-clicking on context menu option (lines 130-139)"""
        ui = InventoryUI()
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # First draw to populate slot_rects
        ui.draw(mock_screen, inventory)

        # Get the weapon slot rect position
        weapon_slot_rect = ui.state.slot_rects[("weapon", 0)]

        # Position context menu so it overlaps with the weapon slot
        # Context menu is 120px wide, 90px tall (3 options * 30px each)
        # Position it so the first option overlaps with the slot
        overlap_pos = (weapon_slot_rect.left, weapon_slot_rect.top)

        ui.state.context_menu_slot = ("weapon", 0)
        ui.state.context_menu_pos = overlap_pos

        # Get context menu option rects with this position
        option_rects = ui.renderer.get_context_menu_rects(ui.state, inventory)

        # Find a position that's on both the slot AND a context menu option
        # Use the center of the first option
        first_option_rect, first_option_text = option_rects[0]

        # Find overlap between slot and first option
        overlap_x = max(weapon_slot_rect.left, first_option_rect.left) + 10
        overlap_y = max(weapon_slot_rect.top, first_option_rect.top) + 10

        click_pos = (overlap_x, overlap_y)

        # Verify the position is on both the slot and the context menu option
        assert weapon_slot_rect.collidepoint(click_pos), "Click must be on weapon slot"
        assert first_option_rect.collidepoint(click_pos), (
            "Click must be on context menu option"
        )

        from unittest.mock import Mock

        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 3  # Right click
        event.pos = click_pos

        # Handle the right-click
        result = ui.handle_input(event, inventory)

        # Should have executed the action (Drop or Inspect depending on which option)
        assert result is True
        assert ui.state.context_menu_slot is None  # Context menu should be closed

    def test_right_click_on_slot_with_context_menu_miss(self, mock_screen):
        """Test right-clicking on slot with context menu but NOT on option (lines 133->142)"""
        ui = InventoryUI()
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # First draw to populate slot_rects
        ui.draw(mock_screen, inventory)

        # Get the weapon slot rect position
        weapon_slot_rect = ui.state.slot_rects[("weapon", 0)]

        # Open context menu away from the slot
        ui.state.context_menu_slot = ("weapon", 0)
        ui.state.context_menu_pos = (600, 500)  # Far from slot

        # Right-click on the slot center (which won't be on any context menu option)
        click_pos = weapon_slot_rect.center

        from unittest.mock import Mock

        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 3  # Right click
        event.pos = click_pos

        # Handle the right-click
        result = ui.handle_input(event, inventory)

        # Should have opened a new context menu (line 142)
        assert result is True
        assert ui.state.context_menu_slot == ("weapon", 0)  # Context menu re-opened


class TestInventoryUIBackwardCompatibility:
    """Tests for backward compatibility paths in InventoryUI"""

    def test_draw_tooltip_without_mouse_pos(self, mock_screen):
        """Test _draw_tooltip when mouse_pos is None (line 127)"""
        ui = InventoryUI()
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Call without mouse_pos
        ui._draw_tooltip(mock_screen, inventory)
        # Should not crash

    def test_draw_dragged_item_without_mouse_pos(self, mock_screen):
        """Test _draw_dragged_item when mouse_pos is None (line 137)"""
        ui = InventoryUI()
        ui.state.dragging_item = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Call without mouse_pos
        ui._draw_dragged_item(mock_screen)
        # Should not crash

    def test_context_menu_click_no_match(self, mock_screen):
        """Test context menu immediate-mode click detection with no match (line 186->exit)"""
        ui = InventoryUI()
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Open context menu
        ui.state.context_menu_slot = ("weapon", 0)
        ui.state.context_menu_pos = (400, 300)

        # Mock mouse click outside context menu
        from unittest.mock import patch

        with patch("pygame.mouse.get_pos", return_value=(100, 100)):
            with patch("pygame.mouse.get_pressed", return_value=(True, False, False)):
                ui.draw(mock_screen, inventory)
                # Context menu should still be open (click missed)
                assert ui.state.context_menu_slot is not None


class TestShopUIEdgeCases:
    """Tests for shop UI edge cases"""

    def test_execute_buy_delegation(self, mock_screen):
        """Test _execute_buy delegation method (line 165)"""
        shop_ui = ShopUI()
        shop = Shop(10, 10)  # Shop needs grid position
        warrior = Warrior(0, 0)
        warrior.gold = 1000

        # Create shop item
        item = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        item.gold_value = 100  # Set gold value for the item
        shop_item = ShopItem(item, quantity=1)

        # Call the delegation method directly
        shop_ui._execute_buy(shop, warrior, shop_item)

        # Should have bought the item
        assert warrior.inventory.weapon_slot is not None


class TestShopStateEdgeCases:
    """Tests for shop state edge cases"""

    def test_confirm_action_no_dialog(self):
        """Test confirm_action when no dialog is open (line 116->exit)"""
        state = ShopState()

        # No confirmation dialog
        state.confirmation_dialog = None

        # Should not crash
        state.confirm_action()

        # Nothing should happen
        assert state.confirmation_dialog is None


class TestInventoryRendererFullCoverage:
    """Tests to achieve 100% coverage for inventory_renderer.py"""

    def test_draw_context_menu_near_bottom_edge(self, mock_screen):
        """Test drawing context menu near bottom edge to trigger y-adjustment (line 376)"""
        renderer = InventoryRenderer()
        state = InventoryState()
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Context menu near bottom edge - should trigger menu_y adjustment
        state.context_menu_slot = ("weapon", 0)
        state.context_menu_pos = (400, 590)  # Near bottom edge (screen is 600px tall)

        # Call renderer.draw() which will call _draw_context_menu
        renderer.draw(mock_screen, inventory, state)
        # Should not crash and should have adjusted menu position

    def test_draw_item_with_attack_bonus_in_backpack(self, mock_screen):
        """Test drawing item with attack bonus in backpack slot (line 250)"""
        renderer = InventoryRenderer()
        state = InventoryState()
        inventory = Inventory()

        # Add weapon with attack bonus to backpack
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=15)
        inventory.backpack_slots[0] = weapon

        # Draw the inventory - should draw the item with attack bonus stat
        renderer.draw(mock_screen, inventory, state)
        # Should not crash and should have drawn the attack bonus text
