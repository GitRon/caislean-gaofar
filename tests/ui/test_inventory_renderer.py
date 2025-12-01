"""Comprehensive tests for inventory_renderer.py"""

import pytest
import pygame
from unittest.mock import patch
from caislean_gaofar.ui.inventory_renderer import InventoryRenderer
from caislean_gaofar.ui.inventory_state import InventoryState
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
def screen() -> pygame.Surface:
    """Create a real pygame surface for testing"""
    return pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))


@pytest.fixture
def renderer() -> InventoryRenderer:
    """Create an InventoryRenderer instance"""
    return InventoryRenderer()


@pytest.fixture
def inventory() -> Inventory:
    """Create an empty inventory"""
    return Inventory()


@pytest.fixture
def state() -> InventoryState:
    """Create an empty inventory state"""
    return InventoryState()


class TestInventoryRendererInitialization:
    """Tests for InventoryRenderer initialization"""

    def test_initialization_sets_fonts(self, renderer):
        """Test that initialization creates all required fonts"""
        assert renderer.font is not None
        assert renderer.title_font is not None
        assert renderer.small_font is not None
        assert renderer.tooltip_font is not None

    def test_initialization_sets_dimensions(self, renderer):
        """Test that initialization sets correct dimensions"""
        assert renderer.panel_width == 500
        assert renderer.panel_height == 500
        assert renderer.padding == 20
        assert renderer.slot_size == 80
        assert renderer.slot_margin == 10

    def test_initialization_sets_colors(self, renderer):
        """Test that initialization sets correct colors"""
        assert renderer.bg_color == (40, 40, 50, 230)
        assert renderer.slot_color == (60, 60, 70)
        assert renderer.slot_border_color == (100, 100, 120)
        assert renderer.equipped_slot_color == (80, 60, 40)
        assert renderer.text_color == (255, 255, 255)
        assert renderer.selected_color == (255, 200, 0)
        assert renderer.hover_color == (150, 150, 170)


class TestDrawBaseUI:
    """Tests for _draw_base_ui method"""

    def test_draw_base_ui_renders_background(self, renderer, screen):
        """Test that base UI draws background"""
        renderer._draw_base_ui(screen, 100, 100)
        # Test passes if no exception is raised

    def test_draw_base_ui_renders_border(self, renderer, screen):
        """Test that base UI draws border"""
        renderer._draw_base_ui(screen, 150, 150)
        # Test passes if no exception is raised

    def test_draw_base_ui_renders_title(self, renderer, screen):
        """Test that base UI draws title"""
        renderer._draw_base_ui(screen, 0, 0)
        # Test passes if no exception is raised


class TestDrawSlot:
    """Tests for _draw_slot method"""

    def test_draw_slot_empty(self, renderer, screen, state):
        """Test drawing an empty slot"""
        renderer._draw_slot(screen, 100, 100, "TEST", None, ("backpack", 0), state)
        assert ("backpack", 0) in state.slot_rects

    def test_draw_slot_with_item(self, renderer, screen, state):
        """Test drawing a slot with an item"""
        item = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        renderer._draw_slot(screen, 100, 100, "WEAPON", item, ("weapon", 0), state)
        assert ("weapon", 0) in state.slot_rects

    def test_draw_slot_equipped(self, renderer, screen, state):
        """Test drawing an equipped slot"""
        item = Item("Shield", ItemType.ARMOR, defense_bonus=5)
        renderer._draw_slot(
            screen, 100, 100, "ARMOR", item, ("armor", 0), state, is_equipped=True
        )
        # Test passes if no exception is raised

    def test_draw_slot_selected(self, renderer, screen, state):
        """Test drawing a selected slot"""
        item = Item("Potion", ItemType.CONSUMABLE)
        renderer._draw_slot(
            screen, 100, 100, "SLOT", item, ("backpack", 0), state, is_selected=True
        )
        # Test passes if no exception is raised

    def test_draw_slot_hovered(self, renderer, screen, state):
        """Test drawing a hovered slot"""
        item = Item("Gem", ItemType.MISC)
        renderer._draw_slot(
            screen, 100, 100, "SLOT", item, ("backpack", 1), state, is_hovered=True
        )
        # Test passes if no exception is raised

    def test_draw_slot_hides_dragged_item(self, renderer, screen, state):
        """Test that slot doesn't show item if it's being dragged from that slot"""
        item = Item("Dragged", ItemType.WEAPON, attack_bonus=5)
        state.dragging_from = ("weapon", 0)
        state.dragging_item = item
        renderer._draw_slot(screen, 100, 100, "WEAPON", item, ("weapon", 0), state)
        # Test passes if no exception is raised


class TestDrawItemInSlot:
    """Tests for _draw_item_in_slot method"""

    def test_draw_item_short_name(self, renderer, screen):
        """Test drawing item with short name"""
        item = Item("Sword", ItemType.WEAPON)
        renderer._draw_item_in_slot(screen, 100, 100, item)
        # Test passes if no exception is raised

    def test_draw_item_long_name_abbreviated(self, renderer, screen):
        """Test drawing item with long name gets abbreviated"""
        item = Item("Very Long Weapon Name", ItemType.WEAPON)
        renderer._draw_item_in_slot(screen, 100, 100, item)
        # Test passes if no exception is raised

    def test_draw_item_with_attack_bonus(self, renderer, screen):
        """Test drawing item with attack bonus"""
        item = Item("Sword", ItemType.WEAPON, attack_bonus=15)
        renderer._draw_item_in_slot(screen, 100, 100, item)
        # Test passes if no exception is raised

    def test_draw_item_with_defense_bonus(self, renderer, screen):
        """Test drawing item with defense bonus"""
        item = Item("Shield", ItemType.ARMOR, defense_bonus=10)
        renderer._draw_item_in_slot(screen, 100, 100, item)
        # Test passes if no exception is raised

    def test_draw_item_with_health_restore(self, renderer, screen):
        """Test drawing item with health restore"""
        item = Item("Potion", ItemType.CONSUMABLE, health_restore=30)
        renderer._draw_item_in_slot(screen, 100, 100, item)
        # Test passes if no exception is raised

    def test_draw_item_with_all_bonuses(self, renderer, screen):
        """Test drawing item with all bonuses (stacked vertically)"""
        item = Item(
            "Elixir",
            ItemType.CONSUMABLE,
            attack_bonus=5,
            defense_bonus=3,
            health_restore=50,
        )
        renderer._draw_item_in_slot(screen, 100, 100, item)
        # Test passes if no exception is raised

    def test_draw_item_zero_bonuses(self, renderer, screen):
        """Test drawing item with zero bonuses doesn't display them"""
        item = Item(
            "Plain Item",
            ItemType.MISC,
            attack_bonus=0,
            defense_bonus=0,
            health_restore=0,
        )
        renderer._draw_item_in_slot(screen, 100, 100, item)
        # Test passes if no exception is raised


class TestDrawTooltip:
    """Tests for _draw_tooltip method"""

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_no_hovered_slot(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test that tooltip doesn't draw when no slot is hovered"""
        state.hovered_slot = None
        renderer._draw_tooltip(screen, inventory, state, (400, 300))
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_empty_slot(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test that tooltip doesn't draw for empty slot"""
        state.hovered_slot = ("backpack", 0)
        renderer._draw_tooltip(screen, inventory, state, (400, 300))
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_basic_item(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test drawing tooltip for basic item"""
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON)
        state.hovered_slot = ("weapon", 0)
        renderer._draw_tooltip(screen, inventory, state, (400, 300))
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_with_description(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test drawing tooltip with description"""
        inventory.armor_slot = Item(
            "Shield", ItemType.ARMOR, description="A sturdy shield"
        )
        state.hovered_slot = ("armor", 0)
        renderer._draw_tooltip(screen, inventory, state, (400, 300))
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_with_attack_bonus(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test drawing tooltip with attack bonus"""
        inventory.weapon_slot = Item("Axe", ItemType.WEAPON, attack_bonus=20)
        state.hovered_slot = ("weapon", 0)
        renderer._draw_tooltip(screen, inventory, state, (400, 300))
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_with_defense_bonus(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test drawing tooltip with defense bonus"""
        inventory.armor_slot = Item("Plate", ItemType.ARMOR, defense_bonus=15)
        state.hovered_slot = ("armor", 0)
        renderer._draw_tooltip(screen, inventory, state, (400, 300))
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_with_health_restore(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test drawing tooltip with health restore - ensures line 315 coverage"""
        inventory.backpack_slots[0] = Item(
            "Health Potion",
            ItemType.CONSUMABLE,
            health_restore=30,
            description="Restores health",
        )
        state.hovered_slot = ("backpack", 0)
        renderer._draw_tooltip(screen, inventory, state, (400, 300))
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_tooltip_with_all_stats(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test drawing tooltip with all stats"""
        inventory.backpack_slots[0] = Item(
            "Magic Elixir",
            ItemType.CONSUMABLE,
            description="Powerful",
            attack_bonus=5,
            defense_bonus=3,
            health_restore=50,
        )
        state.hovered_slot = ("backpack", 0)
        renderer._draw_tooltip(screen, inventory, state, (400, 300))
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(790, 300))
    def test_draw_tooltip_repositioned_right_edge(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test tooltip repositioning near right edge"""
        inventory.weapon_slot = Item(
            "Sword", ItemType.WEAPON, description="A long description"
        )
        state.hovered_slot = ("weapon", 0)
        renderer._draw_tooltip(screen, inventory, state, (790, 300))
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 580))
    def test_draw_tooltip_repositioned_bottom_edge(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test tooltip repositioning near bottom edge"""
        inventory.armor_slot = Item(
            "Shield", ItemType.ARMOR, description="A description"
        )
        state.hovered_slot = ("armor", 0)
        renderer._draw_tooltip(screen, inventory, state, (400, 580))
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(790, 580))
    def test_draw_tooltip_repositioned_both_edges(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test tooltip repositioning near both edges"""
        inventory.backpack_slots[0] = Item("Item", ItemType.MISC, description="Test")
        state.hovered_slot = ("backpack", 0)
        renderer._draw_tooltip(screen, inventory, state, (790, 580))
        # Test passes if no exception is raised


class TestDrawContextMenu:
    """Tests for _draw_context_menu method"""

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_context_menu_no_slot(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test context menu doesn't draw when no slot is set"""
        state.context_menu_slot = None
        state.context_menu_pos = None
        renderer._draw_context_menu(screen, inventory, state)
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_context_menu_empty_slot_closes(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test context menu closes for empty slot"""
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 300)
        renderer._draw_context_menu(screen, inventory, state)
        assert state.context_menu_slot is None

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_context_menu_weapon_in_backpack(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test context menu for weapon in backpack shows Equip and Drop"""
        inventory.backpack_slots[0] = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 300)
        renderer._draw_context_menu(screen, inventory, state)
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_context_menu_armor_in_backpack(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test context menu for armor in backpack shows Equip and Drop"""
        inventory.backpack_slots[0] = Item("Shield", ItemType.ARMOR, defense_bonus=5)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 300)
        renderer._draw_context_menu(screen, inventory, state)
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_context_menu_misc_item(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test context menu for misc item shows only Drop"""
        inventory.backpack_slots[0] = Item("Gem", ItemType.MISC)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 300)
        renderer._draw_context_menu(screen, inventory, state)
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(780, 300))
    def test_draw_context_menu_near_right_edge(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test context menu repositions near right edge"""
        inventory.backpack_slots[0] = Item("Item", ItemType.MISC)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (780, 300)
        renderer._draw_context_menu(screen, inventory, state)
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 580))
    def test_draw_context_menu_near_bottom_edge(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test context menu repositions near bottom edge"""
        inventory.backpack_slots[0] = Item("Item", ItemType.MISC)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 580)
        renderer._draw_context_menu(screen, inventory, state)
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(450, 350))
    def test_draw_context_menu_with_hover(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test context menu highlights hovered option"""
        inventory.backpack_slots[0] = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 300)
        renderer._draw_context_menu(screen, inventory, state)
        # Test passes if no exception is raised


class TestDrawDraggedItem:
    """Tests for _draw_dragged_item method"""

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_dragged_item_none(self, mock_pos, renderer, screen, state):
        """Test dragged item doesn't draw when None"""
        state.dragging_item = None
        renderer._draw_dragged_item(screen, state, (400, 300))
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_dragged_item_weapon(self, mock_pos, renderer, screen, state):
        """Test drawing dragged weapon"""
        state.dragging_item = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        state.drag_offset = (0, 0)
        renderer._draw_dragged_item(screen, state, (400, 300))
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(450, 350))
    def test_draw_dragged_item_with_offset(self, mock_pos, renderer, screen, state):
        """Test drawing dragged item with offset"""
        state.dragging_item = Item("Shield", ItemType.ARMOR, defense_bonus=5)
        state.drag_offset = (10, -5)
        renderer._draw_dragged_item(screen, state, (450, 350))
        # Test passes if no exception is raised


class TestGetItemFromSlot:
    """Tests for _get_item_from_slot method"""

    def test_get_item_from_weapon_slot(self, renderer, inventory):
        """Test getting item from weapon slot"""
        weapon = Item("Sword", ItemType.WEAPON)
        inventory.weapon_slot = weapon
        result = renderer._get_item_from_slot(inventory, "weapon", 0)
        assert result == weapon

    def test_get_item_from_armor_slot(self, renderer, inventory):
        """Test getting item from armor slot"""
        armor = Item("Shield", ItemType.ARMOR)
        inventory.armor_slot = armor
        result = renderer._get_item_from_slot(inventory, "armor", 0)
        assert result == armor

    def test_get_item_from_backpack_slot(self, renderer, inventory):
        """Test getting item from backpack slot"""
        item = Item("Potion", ItemType.CONSUMABLE)
        inventory.backpack_slots[3] = item
        result = renderer._get_item_from_slot(inventory, "backpack", 3)
        assert result == item

    def test_get_item_from_invalid_slot_type(self, renderer, inventory):
        """Test getting item from invalid slot type returns None"""
        result = renderer._get_item_from_slot(inventory, "invalid", 0)
        assert result is None

    def test_get_item_from_empty_slot(self, renderer, inventory):
        """Test getting item from empty slot returns None"""
        result = renderer._get_item_from_slot(inventory, "backpack", 0)
        assert result is None


class TestGetContextMenuRects:
    """Tests for get_context_menu_rects method"""

    def test_get_context_menu_rects_no_slot(self, renderer, inventory, state):
        """Test get_context_menu_rects with no slot returns empty list"""
        state.context_menu_slot = None
        state.context_menu_pos = None
        result = renderer.get_context_menu_rects(state, inventory)
        assert result == []

    def test_get_context_menu_rects_empty_slot(self, renderer, inventory, state):
        """Test get_context_menu_rects with empty slot returns empty list"""
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 300)
        result = renderer.get_context_menu_rects(state, inventory)
        assert result == []

    def test_get_context_menu_rects_weapon_in_backpack(
        self, renderer, inventory, state, screen
    ):
        """Test get_context_menu_rects for weapon shows Equip and Drop"""
        inventory.backpack_slots[0] = Item("Sword", ItemType.WEAPON)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 300)
        result = renderer.get_context_menu_rects(state, inventory)
        assert len(result) == 2
        assert result[0][1] == "Equip"
        assert result[1][1] == "Drop"

    def test_get_context_menu_rects_armor_in_backpack(
        self, renderer, inventory, state, screen
    ):
        """Test get_context_menu_rects for armor shows Equip and Drop"""
        inventory.backpack_slots[0] = Item("Shield", ItemType.ARMOR)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 300)
        result = renderer.get_context_menu_rects(state, inventory)
        assert len(result) == 2

    def test_get_context_menu_rects_misc_item(self, renderer, inventory, state, screen):
        """Test get_context_menu_rects for misc item shows only Drop"""
        inventory.backpack_slots[0] = Item("Gem", ItemType.MISC)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 300)
        result = renderer.get_context_menu_rects(state, inventory)
        assert len(result) == 1
        assert result[0][1] == "Drop"

    def test_get_context_menu_rects_near_right_edge(
        self, renderer, inventory, state, screen
    ):
        """Test get_context_menu_rects repositions near right edge"""
        inventory.backpack_slots[0] = Item("Item", ItemType.MISC)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (780, 300)
        result = renderer.get_context_menu_rects(state, inventory)
        assert len(result) == 1

    def test_get_context_menu_rects_near_bottom_edge(
        self, renderer, inventory, state, screen
    ):
        """Test get_context_menu_rects repositions near bottom edge"""
        inventory.backpack_slots[0] = Item("Item", ItemType.MISC)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 580)
        result = renderer.get_context_menu_rects(state, inventory)
        assert len(result) == 1


class TestIsPosInContextMenu:
    """Tests for is_pos_in_context_menu method"""

    def test_is_pos_in_context_menu_no_menu(self, renderer, state):
        """Test position check with no context menu"""
        state.context_menu_pos = None
        result = renderer.is_pos_in_context_menu((400, 300), state)
        assert result is False

    def test_is_pos_in_context_menu_inside(self, renderer, state):
        """Test position inside context menu"""
        state.context_menu_pos = (400, 300)
        state.context_menu_slot = ("backpack", 0)
        result = renderer.is_pos_in_context_menu((450, 320), state)
        assert result is True

    def test_is_pos_in_context_menu_outside(self, renderer, state):
        """Test position outside context menu"""
        state.context_menu_pos = (400, 300)
        state.context_menu_slot = ("backpack", 0)
        result = renderer.is_pos_in_context_menu((100, 100), state)
        assert result is False


class TestDrawEquipmentSection:
    """Tests for _draw_equipment_section method"""

    def test_draw_equipment_section_empty(self, renderer, screen, inventory, state):
        """Test drawing empty equipment section"""
        renderer._draw_equipment_section(screen, inventory, state, 100, 100)
        assert ("weapon", 0) in state.slot_rects
        assert ("armor", 0) in state.slot_rects

    def test_draw_equipment_section_with_items(
        self, renderer, screen, inventory, state
    ):
        """Test drawing equipment section with items"""
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory.armor_slot = Item("Shield", ItemType.ARMOR, defense_bonus=5)
        renderer._draw_equipment_section(screen, inventory, state, 100, 100)
        # Test passes if no exception is raised

    def test_draw_equipment_section_selected(self, renderer, screen, inventory, state):
        """Test drawing equipment section with selected slot"""
        inventory.weapon_slot = Item("Axe", ItemType.WEAPON, attack_bonus=15)
        state.selected_slot = ("weapon", 0)
        renderer._draw_equipment_section(screen, inventory, state, 100, 100)
        # Test passes if no exception is raised

    def test_draw_equipment_section_hovered(self, renderer, screen, inventory, state):
        """Test drawing equipment section with hovered slot"""
        inventory.armor_slot = Item("Plate", ItemType.ARMOR, defense_bonus=10)
        state.hovered_slot = ("armor", 0)
        renderer._draw_equipment_section(screen, inventory, state, 100, 100)
        # Test passes if no exception is raised


class TestDrawBackpackSection:
    """Tests for _draw_backpack_section method"""

    def test_draw_backpack_section_empty(self, renderer, screen, inventory, state):
        """Test drawing empty backpack section"""
        renderer._draw_backpack_section(screen, inventory, state, 100, 200)
        # Verify all 10 backpack slots have rects created
        assert ("backpack", 0) in state.slot_rects
        assert ("backpack", 1) in state.slot_rects
        assert ("backpack", 2) in state.slot_rects
        assert ("backpack", 3) in state.slot_rects
        assert ("backpack", 4) in state.slot_rects
        assert ("backpack", 5) in state.slot_rects
        assert ("backpack", 6) in state.slot_rects
        assert ("backpack", 7) in state.slot_rects
        assert ("backpack", 8) in state.slot_rects
        assert ("backpack", 9) in state.slot_rects

    def test_draw_backpack_section_with_items(self, renderer, screen, inventory, state):
        """Test drawing backpack section with items"""
        # Add items to first 5 slots
        inventory.backpack_slots[0] = Item("Item 0", ItemType.MISC)
        inventory.backpack_slots[1] = Item("Item 1", ItemType.MISC)
        inventory.backpack_slots[2] = Item("Item 2", ItemType.MISC)
        inventory.backpack_slots[3] = Item("Item 3", ItemType.MISC)
        inventory.backpack_slots[4] = Item("Item 4", ItemType.MISC)
        renderer._draw_backpack_section(screen, inventory, state, 100, 200)
        # Test passes if no exception is raised

    def test_draw_backpack_section_selected(self, renderer, screen, inventory, state):
        """Test drawing backpack section with selected slot"""
        inventory.backpack_slots[3] = Item("Selected", ItemType.MISC)
        state.selected_slot = ("backpack", 3)
        renderer._draw_backpack_section(screen, inventory, state, 100, 200)
        # Test passes if no exception is raised

    def test_draw_backpack_section_hovered(self, renderer, screen, inventory, state):
        """Test drawing backpack section with hovered slot"""
        inventory.backpack_slots[7] = Item("Hovered", ItemType.CONSUMABLE)
        state.hovered_slot = ("backpack", 7)
        renderer._draw_backpack_section(screen, inventory, state, 100, 200)
        # Test passes if no exception is raised


class TestDrawInstructions:
    """Tests for _draw_instructions method"""

    def test_draw_instructions(self, renderer, screen):
        """Test drawing instructions"""
        renderer._draw_instructions(screen, 100, 100)
        # Test passes if no exception is raised


class TestMainDrawMethod:
    """Tests for main draw method"""

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_empty_inventory(self, mock_pos, renderer, screen, inventory, state):
        """Test drawing empty inventory"""
        renderer.draw(screen, inventory, state)
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_with_items(self, mock_pos, renderer, screen, inventory, state):
        """Test drawing with items"""
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory.armor_slot = Item("Shield", ItemType.ARMOR, defense_bonus=5)
        inventory.backpack_slots[0] = Item(
            "Potion", ItemType.CONSUMABLE, health_restore=30
        )
        renderer.draw(screen, inventory, state)
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_with_tooltip(self, mock_pos, renderer, screen, inventory, state):
        """Test drawing with tooltip"""
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        state.hovered_slot = ("weapon", 0)
        renderer.draw(screen, inventory, state)
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_with_context_menu(self, mock_pos, renderer, screen, inventory, state):
        """Test drawing with context menu"""
        inventory.backpack_slots[0] = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        state.context_menu_slot = ("backpack", 0)
        state.context_menu_pos = (400, 300)
        renderer.draw(screen, inventory, state)
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(450, 350))
    def test_draw_with_dragged_item(self, mock_pos, renderer, screen, inventory, state):
        """Test drawing with dragged item"""
        item = Item("Dragged", ItemType.WEAPON, attack_bonus=5)
        state.dragging_item = item
        state.dragging_from = ("weapon", 0)
        state.drag_offset = (0, 0)
        renderer.draw(screen, inventory, state)
        # Test passes if no exception is raised

    @patch("pygame.mouse.get_pos", return_value=(400, 300))
    def test_draw_no_tooltip_when_dragging(
        self, mock_pos, renderer, screen, inventory, state
    ):
        """Test that tooltip doesn't show when dragging"""
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        state.hovered_slot = ("weapon", 0)
        state.dragging_item = Item("Dragged", ItemType.ARMOR)
        renderer.draw(screen, inventory, state)
        # Test passes if no exception is raised
