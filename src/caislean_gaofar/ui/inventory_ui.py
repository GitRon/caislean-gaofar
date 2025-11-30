"""UI overlay for displaying and managing inventory.

This module provides a coordinated interface for the inventory UI,
following the MVC pattern with separate state, rendering, and input handling.
"""

from __future__ import annotations

import pygame
from typing import TYPE_CHECKING

from caislean_gaofar.systems.inventory import Inventory
from caislean_gaofar.ui.inventory_state import InventoryState
from caislean_gaofar.ui.inventory_renderer import InventoryRenderer
from caislean_gaofar.ui.inventory_input_handler import InventoryInputHandler

if TYPE_CHECKING:
    from caislean_gaofar.objects.item import Item


class InventoryUI:
    """UI overlay for displaying and managing inventory."""

    def __init__(self):
        """Initialize the inventory UI with separated concerns."""
        self.state = InventoryState()
        self.renderer = InventoryRenderer()
        self.input_handler = InventoryInputHandler(self.state, self.renderer, ui=self)
        self._game = None  # Store reference to game for immediate-mode handling

    # Delegate methods to input handler for backward compatibility
    def _get_item_from_slot(self, inventory, slot_type, slot_index) -> Item | None:
        return self.input_handler._get_item_from_slot(inventory, slot_type, slot_index)

    def _move_item(self, inventory, from_slot, to_slot) -> None:
        return self.input_handler._move_item(inventory, from_slot, to_slot)

    def _place_item_in_slot(self, inventory, item, slot_type, slot_index) -> bool:
        return self.input_handler._place_item_in_slot(
            inventory, item, slot_type, slot_index
        )

    def _execute_context_menu_action(self, action, inventory, game=None) -> None:
        return self.input_handler._execute_context_menu_action(action, inventory, game)

    # Delegate methods to renderer for backward compatibility
    def _is_pos_in_context_menu(self, pos) -> bool:
        return self.renderer.is_pos_in_context_menu(pos, self.state)

    def _update_hovered_slot(self, mouse_pos) -> None:
        return self.state.update_hovered_slot(mouse_pos)

    def _draw_tooltip(self, screen, inventory, mouse_pos=None) -> None:
        # Support both old (3-arg) and new (4-arg) calling conventions
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        return self.renderer._draw_tooltip(screen, inventory, self.state, mouse_pos)

    def _draw_context_menu(self, screen, inventory) -> None:
        # Use self.state as the state parameter
        return self.renderer._draw_context_menu(screen, inventory, self.state)

    def _draw_dragged_item(self, screen, mouse_pos=None) -> None:
        # Support both old (2-arg) and new (3-arg) calling conventions
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        return self.renderer._draw_dragged_item(screen, self.state, mouse_pos)

    def _draw_slot(
        self,
        screen,
        x,
        y,
        label,
        item,
        slot_id,
        is_equipped=False,
        is_selected=False,
        is_hovered=False,
    ) -> None:
        # Use self.state as the state parameter
        return self.renderer._draw_slot(
            screen,
            x,
            y,
            label,
            item,
            slot_id,
            self.state,
            is_equipped,
            is_selected,
            is_hovered,
        )

    def draw(self, screen: pygame.Surface, inventory: Inventory):
        """
        Draw the inventory overlay.

        Args:
            screen: Pygame surface to draw on
            inventory: The inventory to display
        """
        # Clear slot rects for this frame
        self.state.clear_slot_rects()

        # Update hovered slot based on mouse position
        mouse_pos = pygame.mouse.get_pos()
        self._update_hovered_slot(mouse_pos)

        # Delegate main rendering to the renderer (but not tooltip/context menu for testability)
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        panel_x = (screen_width - self.renderer.panel_width) // 2
        panel_y = (screen_height - self.renderer.panel_height) // 2

        # Draw base UI elements
        self.renderer._draw_base_ui(screen, panel_x, panel_y)
        self.renderer._draw_equipment_section(
            screen, inventory, self.state, panel_x, panel_y + 60
        )
        self.renderer._draw_backpack_section(
            screen, inventory, self.state, panel_x, panel_y + 200
        )
        self.renderer._draw_instructions(screen, panel_x, panel_y)

        # Draw tooltip if hovering (call through UI for testability)
        if self.state.hovered_slot and not self.state.is_dragging():
            self._draw_tooltip(screen, inventory, mouse_pos)

        # Draw context menu if active (call through UI for testability)
        if self.state.has_context_menu():
            self._draw_context_menu(screen, inventory)

        # Draw dragged item (on top of everything)
        if self.state.is_dragging():
            self._draw_dragged_item(screen, mouse_pos)

        # Handle immediate-mode click detection on context menu (for backward compatibility)
        if self.state.has_context_menu() and pygame.mouse.get_pressed()[0]:
            option_rects = self.renderer.get_context_menu_rects(self.state, inventory)
            for option_rect, option_text in option_rects:
                if option_rect.collidepoint(mouse_pos):
                    self._execute_context_menu_action(
                        option_text, inventory, self._game
                    )
                    self.state.close_context_menu()
                    break

    def handle_input(
        self, event: pygame.event.Event, inventory: Inventory, game=None
    ) -> bool:
        """
        Handle input events for inventory management.

        Args:
            event: The pygame event to handle
            inventory: The inventory to manage
            game: The game instance (needed for dropping items)

        Returns:
            True if the event was handled.
        """
        # Store game reference for immediate-mode handling in draw()
        self._game = game
        return self.input_handler.handle_input(event, inventory, game)
