"""UI overlay for displaying and managing inventory.

This module provides a coordinated interface for the inventory UI,
following the MVC pattern with separate state, rendering, and input handling.
"""

import pygame
from caislean_gaofar.systems.inventory import Inventory
from caislean_gaofar.ui.inventory_state import InventoryState
from caislean_gaofar.ui.inventory_renderer import InventoryRenderer
from caislean_gaofar.ui.inventory_input_handler import InventoryInputHandler


class InventoryUI:
    """UI overlay for displaying and managing inventory."""

    def __init__(self):
        """Initialize the inventory UI with separated concerns."""
        self.state = InventoryState()
        self.renderer = InventoryRenderer()
        self.input_handler = InventoryInputHandler(self.state, self.renderer)

    # Property delegation for backward compatibility with tests
    @property
    def selected_slot(self):
        return self.state.selected_slot

    @selected_slot.setter
    def selected_slot(self, value):
        self.state.selected_slot = value

    @property
    def hovered_slot(self):
        return self.state.hovered_slot

    @hovered_slot.setter
    def hovered_slot(self, value):
        self.state.hovered_slot = value

    @property
    def dragging_item(self):
        return self.state.dragging_item

    @dragging_item.setter
    def dragging_item(self, value):
        self.state.dragging_item = value

    @property
    def dragging_from(self):
        return self.state.dragging_from

    @dragging_from.setter
    def dragging_from(self, value):
        self.state.dragging_from = value

    @property
    def drag_offset(self):
        return self.state.drag_offset

    @drag_offset.setter
    def drag_offset(self, value):
        self.state.drag_offset = value

    @property
    def context_menu_slot(self):
        return self.state.context_menu_slot

    @context_menu_slot.setter
    def context_menu_slot(self, value):
        self.state.context_menu_slot = value

    @property
    def context_menu_pos(self):
        return self.state.context_menu_pos

    @context_menu_pos.setter
    def context_menu_pos(self, value):
        self.state.context_menu_pos = value

    @property
    def slot_rects(self):
        return self.state.slot_rects

    @property
    def panel_width(self):
        return self.renderer.panel_width

    @property
    def panel_height(self):
        return self.renderer.panel_height

    @property
    def padding(self):
        return self.renderer.padding

    @property
    def slot_size(self):
        return self.renderer.slot_size

    @property
    def slot_margin(self):
        return self.renderer.slot_margin

    # Delegate methods to input handler for backward compatibility
    def _get_item_from_slot(self, inventory, slot_type, slot_index):
        return self.input_handler._get_item_from_slot(inventory, slot_type, slot_index)

    def _move_item(self, inventory, from_slot, to_slot):
        return self.input_handler._move_item(inventory, from_slot, to_slot)

    def _place_item_in_slot(self, inventory, item, slot_type, slot_index):
        return self.input_handler._place_item_in_slot(inventory, item, slot_type, slot_index)

    def _execute_context_menu_action(self, action, inventory):
        return self.input_handler._execute_context_menu_action(action, inventory)

    # Delegate methods to renderer for backward compatibility
    def _is_pos_in_context_menu(self, pos):
        return self.renderer.is_pos_in_context_menu(pos, self.state)

    def _update_hovered_slot(self, mouse_pos):
        return self.state.update_hovered_slot(mouse_pos)

    def _draw_tooltip(self, screen, inventory, mouse_pos=None):
        # Support both old (3-arg) and new (4-arg) calling conventions
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        return self.renderer._draw_tooltip(screen, inventory, self.state, mouse_pos)

    def _draw_context_menu(self, screen, inventory):
        # Use self.state as the state parameter
        return self.renderer._draw_context_menu(screen, inventory, self.state)

    def _draw_dragged_item(self, screen, mouse_pos=None):
        # Support both old (2-arg) and new (3-arg) calling conventions
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        return self.renderer._draw_dragged_item(screen, self.state, mouse_pos)

    def _draw_slot(self, screen, x, y, label, item, slot_id, is_equipped=False, is_selected=False, is_hovered=False):
        # Use self.state as the state parameter
        return self.renderer._draw_slot(screen, x, y, label, item, slot_id, self.state, is_equipped, is_selected, is_hovered)

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
        self.state.update_hovered_slot(mouse_pos)

        # Delegate rendering to the renderer
        self.renderer.draw(screen, inventory, self.state)

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
        return self.input_handler.handle_input(event, inventory, game)
