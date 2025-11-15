"""Rendering logic for inventory UI."""

import pygame
from typing import Tuple
from caislean_gaofar.systems.inventory import Inventory
from caislean_gaofar.ui.inventory_state import InventoryState


class InventoryRenderer:
    """Handles rendering of the inventory UI."""

    def __init__(self):
        """Initialize the renderer with fonts and visual settings."""
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 20)
        self.tooltip_font = pygame.font.Font(None, 18)

        # UI positioning
        self.panel_width = 500
        self.panel_height = 500
        self.padding = 20
        self.slot_size = 80
        self.slot_margin = 10

        # Colors
        self.bg_color = (40, 40, 50, 230)  # Dark semi-transparent
        self.slot_color = (60, 60, 70)
        self.slot_border_color = (100, 100, 120)
        self.equipped_slot_color = (80, 60, 40)
        self.text_color = (255, 255, 255)
        self.selected_color = (255, 200, 0)
        self.hover_color = (150, 150, 170)

    def draw(self, screen: pygame.Surface, inventory: Inventory, state: InventoryState):
        """
        Draw the inventory overlay.

        Args:
            screen: Pygame surface to draw on
            inventory: The inventory to display
            state: The current UI state
        """
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Center the panel
        panel_x = (screen_width - self.panel_width) // 2
        panel_y = (screen_height - self.panel_height) // 2

        # Draw semi-transparent background
        overlay = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        overlay.fill(self.bg_color)
        screen.blit(overlay, (panel_x, panel_y))

        # Draw border
        pygame.draw.rect(
            screen,
            self.slot_border_color,
            (panel_x, panel_y, self.panel_width, self.panel_height),
            2,
        )

        # Draw title
        title_text = self.title_font.render("INVENTORY", True, self.text_color)
        title_x = panel_x + (self.panel_width - title_text.get_width()) // 2
        screen.blit(title_text, (title_x, panel_y + 10))

        # Starting position for slots
        current_y = panel_y + 60

        # Draw equipment slots (weapon and armor)
        self._draw_equipment_section(screen, inventory, state, panel_x, current_y)

        # Draw backpack slots
        current_y += 140
        self._draw_backpack_section(screen, inventory, state, panel_x, current_y)

        # Draw instructions
        self._draw_instructions(screen, panel_x, panel_y)

        # Draw tooltip if hovering over an item
        mouse_pos = pygame.mouse.get_pos()
        if state.hovered_slot and not state.is_dragging():
            self._draw_tooltip(screen, inventory, state, mouse_pos)

        # Draw context menu if active
        if state.has_context_menu():
            self._draw_context_menu(screen, inventory, state)

        # Draw dragged item (on top of everything)
        if state.is_dragging():
            self._draw_dragged_item(screen, state, mouse_pos)

    def _draw_equipment_section(
        self,
        screen: pygame.Surface,
        inventory: Inventory,
        state: InventoryState,
        panel_x: int,
        start_y: int,
    ):
        """Draw weapon and armor equipment slots."""
        # Weapon slot
        weapon_x = panel_x + self.padding
        weapon_y = start_y

        is_selected = state.selected_slot == ("weapon", 0)
        is_hovered = state.hovered_slot == ("weapon", 0)
        self._draw_slot(
            screen,
            weapon_x,
            weapon_y,
            "WEAPON",
            inventory.weapon_slot,
            ("weapon", 0),
            state,
            is_equipped=True,
            is_selected=is_selected,
            is_hovered=is_hovered,
        )

        # Armor slot
        armor_x = weapon_x + self.slot_size + self.slot_margin * 3
        armor_y = start_y

        is_selected = state.selected_slot == ("armor", 0)
        is_hovered = state.hovered_slot == ("armor", 0)
        self._draw_slot(
            screen,
            armor_x,
            armor_y,
            "ARMOR",
            inventory.armor_slot,
            ("armor", 0),
            state,
            is_equipped=True,
            is_selected=is_selected,
            is_hovered=is_hovered,
        )

    def _draw_backpack_section(
        self,
        screen: pygame.Surface,
        inventory: Inventory,
        state: InventoryState,
        panel_x: int,
        start_y: int,
    ):
        """Draw backpack slots."""
        # Backpack label
        label = self.font.render("BACKPACK", True, self.text_color)
        screen.blit(label, (panel_x + self.padding, start_y - 25))

        # Draw 13 backpack slots in a 5x3 grid (5 cols, 3 rows, last row has 3 slots)
        slots_per_row = 5
        for i in range(13):
            row = i // slots_per_row
            col = i % slots_per_row

            slot_x = panel_x + self.padding + col * (self.slot_size + self.slot_margin)
            slot_y = start_y + row * (self.slot_size + self.slot_margin)

            is_selected = state.selected_slot == ("backpack", i)
            is_hovered = state.hovered_slot == ("backpack", i)
            self._draw_slot(
                screen,
                slot_x,
                slot_y,
                f"SLOT {i + 1}",
                inventory.backpack_slots[i],
                ("backpack", i),
                state,
                is_selected=is_selected,
                is_hovered=is_hovered,
            )

    def _draw_slot(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        label: str,
        item,
        slot_id: Tuple[str, int],
        state: InventoryState,
        is_equipped: bool = False,
        is_selected: bool = False,
        is_hovered: bool = False,
    ):
        """Draw a single inventory slot."""
        # Store rect for mouse detection
        rect = pygame.Rect(x, y, self.slot_size, self.slot_size)
        state.slot_rects[slot_id] = rect

        # Determine slot color
        if is_equipped:
            slot_bg = self.equipped_slot_color
        else:
            slot_bg = self.slot_color

        # Draw slot background
        pygame.draw.rect(screen, slot_bg, rect)

        # Draw border (highlighted if selected or hovered)
        if is_selected:
            border_color = self.selected_color
            border_width = 3
        elif is_hovered:
            border_color = self.hover_color
            border_width = 3
        else:
            border_color = self.slot_border_color
            border_width = 2

        pygame.draw.rect(screen, border_color, rect, border_width)

        # Draw label
        label_text = self.small_font.render(label, True, self.text_color)
        label_x = x + (self.slot_size - label_text.get_width()) // 2
        screen.blit(label_text, (label_x, y + 5))

        # Draw item if present (and not being dragged from this slot)
        if item and state.dragging_from != slot_id:
            self._draw_item_in_slot(screen, x, y, item)

    def _draw_item_in_slot(self, screen: pygame.Surface, x: int, y: int, item):
        """Draw item information in a slot."""
        # Draw item name (abbreviated if too long)
        name = item.name
        if len(name) > 10:
            name = name[:8] + ".."

        name_text = self.small_font.render(name, True, self.text_color)
        name_x = x + (self.slot_size - name_text.get_width()) // 2
        screen.blit(name_text, (name_x, y + 30))

        # Draw stats
        stats_y = y + 50
        if item.attack_bonus > 0:
            stat_text = self.small_font.render(
                f"+{item.attack_bonus} ATK", True, (255, 100, 100)
            )
            stat_x = x + (self.slot_size - stat_text.get_width()) // 2
            screen.blit(stat_text, (stat_x, stats_y))

        if item.defense_bonus > 0:
            stat_text = self.small_font.render(
                f"+{item.defense_bonus} DEF", True, (100, 100, 255)
            )
            stat_x = x + (self.slot_size - stat_text.get_width()) // 2
            screen.blit(stat_text, (stat_x, stats_y))

    def _draw_instructions(self, screen: pygame.Surface, panel_x: int, panel_y: int):
        """Draw control instructions."""
        instructions = [
            "Left Click - Select/Move Item",
            "Drag & Drop - Move Items",
            "Right Click - Item Menu",
            "Hover - Show Details",
        ]

        y_offset = self.panel_height - 80
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, (200, 200, 200))
            screen.blit(text, (panel_x + self.padding, panel_y + y_offset + i * 18))

    def _draw_tooltip(
        self,
        screen: pygame.Surface,
        inventory: Inventory,
        state: InventoryState,
        mouse_pos: Tuple[int, int],
    ):
        """Draw tooltip showing item details."""
        if not state.hovered_slot:
            return

        slot_type, slot_index = state.hovered_slot
        item = self._get_item_from_slot(inventory, slot_type, slot_index)

        if not item:
            return

        # Tooltip content
        lines = [
            f"Name: {item.name}",
            f"Type: {item.item_type.value.capitalize()}",
        ]

        if item.description:
            lines.append(f"Description: {item.description}")

        if item.attack_bonus > 0:
            lines.append(f"Attack: +{item.attack_bonus}")
        if item.defense_bonus > 0:
            lines.append(f"Defense: +{item.defense_bonus}")

        # Calculate tooltip size
        padding = 10
        line_height = 20
        max_width = max(self.tooltip_font.size(line)[0] for line in lines)
        tooltip_width = max_width + padding * 2
        tooltip_height = len(lines) * line_height + padding * 2

        # Position tooltip near mouse, but keep on screen
        tooltip_x = mouse_pos[0] + 15
        tooltip_y = mouse_pos[1] + 15

        screen_width = screen.get_width()
        screen_height = screen.get_height()

        if tooltip_x + tooltip_width > screen_width:
            tooltip_x = mouse_pos[0] - tooltip_width - 15
        if tooltip_y + tooltip_height > screen_height:
            tooltip_y = mouse_pos[1] - tooltip_height - 15

        # Draw tooltip background
        tooltip_surface = pygame.Surface(
            (tooltip_width, tooltip_height), pygame.SRCALPHA
        )
        tooltip_surface.fill((30, 30, 40, 240))
        pygame.draw.rect(
            tooltip_surface, (150, 150, 170), (0, 0, tooltip_width, tooltip_height), 2
        )
        screen.blit(tooltip_surface, (tooltip_x, tooltip_y))

        # Draw tooltip text
        for i, line in enumerate(lines):
            text = self.tooltip_font.render(line, True, self.text_color)
            screen.blit(
                text, (tooltip_x + padding, tooltip_y + padding + i * line_height)
            )

    def _draw_context_menu(
        self, screen: pygame.Surface, inventory: Inventory, state: InventoryState
    ):
        """Draw right-click context menu."""
        if not state.context_menu_slot or not state.context_menu_pos:
            return

        slot_type, slot_index = state.context_menu_slot
        item = self._get_item_from_slot(inventory, slot_type, slot_index)

        if not item:
            state.close_context_menu()
            return

        # Menu options based on slot type
        options = []
        if slot_type == "backpack":
            from caislean_gaofar.objects.item import ItemType

            if item.item_type in [ItemType.WEAPON, ItemType.ARMOR]:
                options.append("Equip")
        options.append("Drop")
        options.append("Inspect")

        # Menu dimensions
        menu_width = 120
        menu_item_height = 30
        menu_height = len(options) * menu_item_height

        menu_x, menu_y = state.context_menu_pos

        # Keep menu on screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        if menu_x + menu_width > screen_width:
            menu_x = screen_width - menu_width
        if menu_y + menu_height > screen_height:
            menu_y = screen_height - menu_height

        # Draw menu background
        menu_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        menu_surface.fill((40, 40, 50, 250))
        pygame.draw.rect(
            menu_surface, (100, 100, 120), (0, 0, menu_width, menu_height), 2
        )
        screen.blit(menu_surface, (menu_x, menu_y))

        # Draw menu options
        mouse_pos = pygame.mouse.get_pos()
        for i, option in enumerate(options):
            option_y = menu_y + i * menu_item_height
            option_rect = pygame.Rect(menu_x, option_y, menu_width, menu_item_height)

            # Highlight if hovering
            if option_rect.collidepoint(mouse_pos):
                highlight = pygame.Surface(
                    (menu_width - 4, menu_item_height - 4), pygame.SRCALPHA
                )
                highlight.fill((80, 80, 100, 200))
                screen.blit(highlight, (menu_x + 2, option_y + 2))

            # Draw text
            text = self.font.render(option, True, self.text_color)
            text_x = menu_x + (menu_width - text.get_width()) // 2
            text_y = option_y + (menu_item_height - text.get_height()) // 2
            screen.blit(text, (text_x, text_y))

    def _draw_dragged_item(
        self, screen: pygame.Surface, state: InventoryState, mouse_pos: Tuple[int, int]
    ):
        """Draw the item being dragged."""
        if not state.dragging_item:
            return

        # Calculate position with offset
        x = mouse_pos[0] + state.drag_offset[0] - self.slot_size // 2
        y = mouse_pos[1] + state.drag_offset[1] - self.slot_size // 2

        # Draw semi-transparent slot
        drag_surface = pygame.Surface((self.slot_size, self.slot_size), pygame.SRCALPHA)
        drag_surface.fill((60, 60, 70, 200))
        pygame.draw.rect(
            drag_surface,
            self.selected_color,
            (0, 0, self.slot_size, self.slot_size),
            3,
        )
        screen.blit(drag_surface, (x, y))

        # Draw item info
        self._draw_item_in_slot(screen, x, y, state.dragging_item)

    def _get_item_from_slot(
        self, inventory: Inventory, slot_type: str, slot_index: int
    ):
        """Get the item from a specific slot."""
        if slot_type == "weapon":
            return inventory.weapon_slot
        elif slot_type == "armor":
            return inventory.armor_slot
        elif slot_type == "backpack":
            return inventory.backpack_slots[slot_index]
        return None

    def get_context_menu_rects(
        self, state: InventoryState, inventory: Inventory
    ) -> list:
        """Get context menu option rectangles for click detection."""
        if not state.context_menu_slot or not state.context_menu_pos:
            return []

        slot_type, slot_index = state.context_menu_slot
        item = self._get_item_from_slot(inventory, slot_type, slot_index)

        if not item:
            return []

        # Menu options based on slot type
        options = []
        if slot_type == "backpack":
            from caislean_gaofar.objects.item import ItemType

            if item.item_type in [ItemType.WEAPON, ItemType.ARMOR]:
                options.append("Equip")
        options.append("Drop")
        options.append("Inspect")

        # Menu dimensions
        menu_width = 120
        menu_item_height = 30
        menu_height = len(options) * menu_item_height

        menu_x, menu_y = state.context_menu_pos

        # Keep menu on screen
        from pygame import display

        screen = display.get_surface()
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        if menu_x + menu_width > screen_width:
            menu_x = screen_width - menu_width
        if menu_y + menu_height > screen_height:
            menu_y = screen_height - menu_height

        # Create option rects
        option_rects = []
        for i, option in enumerate(options):
            option_y = menu_y + i * menu_item_height
            option_rect = pygame.Rect(menu_x, option_y, menu_width, menu_item_height)
            option_rects.append((option_rect, option))

        return option_rects

    def is_pos_in_context_menu(
        self, pos: Tuple[int, int], state: InventoryState
    ) -> bool:
        """Check if a position is inside the context menu."""
        if not state.context_menu_pos:
            return False

        menu_width = 120
        menu_item_height = 30

        # Count menu items
        if state.context_menu_slot:
            slot_type, _ = state.context_menu_slot
            num_options = 3 if slot_type == "backpack" else 2
            menu_height = num_options * menu_item_height

            menu_x, menu_y = state.context_menu_pos
            menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
            return menu_rect.collidepoint(pos)

        return False
