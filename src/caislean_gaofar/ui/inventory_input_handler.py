"""Input handling for inventory UI."""

import pygame
from typing import Tuple
from caislean_gaofar.systems.inventory import Inventory
from caislean_gaofar.ui.inventory_state import InventoryState
from caislean_gaofar.ui.inventory_renderer import InventoryRenderer


class InventoryInputHandler:
    """Handles input events for the inventory UI."""

    def __init__(self, state: InventoryState, renderer: InventoryRenderer, ui=None):
        """
        Initialize the input handler.

        Args:
            state: The inventory state manager
            renderer: The inventory renderer
            ui: Optional reference to parent UI (for testability)
        """
        self.state = state
        self.renderer = renderer
        self.ui = ui

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
        # Handle mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                return self._handle_left_click(event.pos, inventory)
            elif event.button == 3:  # Right click
                return self._handle_right_click(event.pos, inventory, game)

        # Handle mouse button up
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left release
                return self._handle_left_release(event.pos, inventory)

        # Keep keyboard support for accessibility
        elif event.type == pygame.KEYDOWN:
            return self._handle_keydown(event, inventory, game)

        return False

    def _handle_left_click(
        self, mouse_pos: Tuple[int, int], inventory: Inventory
    ) -> bool:
        """Handle left mouse button click."""
        # Close context menu if clicking outside it
        if self.state.has_context_menu():
            if not self.renderer.is_pos_in_context_menu(mouse_pos, self.state):
                self.state.close_context_menu()
                return True

        # Check if clicking on a slot
        clicked_slot = None
        for slot_id, rect in self.state.slot_rects.items():
            if rect.collidepoint(mouse_pos):
                clicked_slot = slot_id
                break

        if clicked_slot:
            # Get the item in this slot
            slot_type, slot_index = clicked_slot
            item = self._get_item_from_slot(inventory, slot_type, slot_index)

            if item:
                # Start dragging
                rect = self.state.slot_rects[clicked_slot]
                drag_offset = (
                    rect.centerx - mouse_pos[0],
                    rect.centery - mouse_pos[1],
                )
                self.state.start_drag(item, clicked_slot, drag_offset)
            else:
                # Select empty slot
                self.state.selected_slot = clicked_slot

            return True

        return False

    def _handle_left_release(
        self, mouse_pos: Tuple[int, int], inventory: Inventory
    ) -> bool:
        """Handle left mouse button release (end of drag or click)."""
        if self.state.is_dragging():
            # Find which slot we're over
            target_slot = None
            for slot_id, rect in self.state.slot_rects.items():
                if rect.collidepoint(mouse_pos):
                    target_slot = slot_id
                    break

            if target_slot and target_slot != self.state.dragging_from:
                # Try to move/swap items (type guard: target_slot is tuple[str, int])
                self._move_item(inventory, self.state.dragging_from, target_slot)  # type: ignore[arg-type]

            # Clear drag state
            self.state.end_drag()
            return True

        return False

    def _handle_right_click(
        self, mouse_pos: Tuple[int, int], inventory: Inventory, game=None
    ) -> bool:
        """Handle right mouse button click."""
        # Check if clicking on a slot with an item
        for slot_id, rect in self.state.slot_rects.items():
            if rect.collidepoint(mouse_pos):
                slot_type, slot_index = slot_id
                item = self._get_item_from_slot(inventory, slot_type, slot_index)
                if item:
                    # Check if clicking on context menu option
                    if self.state.has_context_menu():
                        option_rects = self.renderer.get_context_menu_rects(
                            self.state, inventory
                        )
                        for option_rect, option_text in option_rects:
                            if option_rect.collidepoint(mouse_pos):
                                self._execute_context_menu_action(
                                    option_text, inventory, game
                                )
                                self.state.close_context_menu()
                                return True

                    # Open context menu
                    self.state.open_context_menu(slot_id, mouse_pos)
                    return True

        return False

    def _handle_keydown(
        self, event: pygame.event.Event, inventory: Inventory, game
    ) -> bool:
        """Handle keyboard input."""
        # Select slots with number keys (1-9 for first 9 backpack slots)
        key_to_slot = {
            pygame.K_1: 0,
            pygame.K_2: 1,
            pygame.K_3: 2,
            pygame.K_4: 3,
            pygame.K_5: 4,
            pygame.K_6: 5,
            pygame.K_7: 6,
            pygame.K_8: 7,
            pygame.K_9: 8,
        }

        if event.key in key_to_slot:
            self.state.selected_slot = ("backpack", key_to_slot[event.key])
            return True

        # Equip item from backpack
        if event.key == pygame.K_e:
            if self.state.selected_slot and self.state.selected_slot[0] == "backpack":
                inventory.equip_from_backpack(self.state.selected_slot[1])
                return True

        # Drop/remove item
        if event.key == pygame.K_x:
            if self.state.selected_slot and game:
                slot_type, index = self.state.selected_slot
                item = inventory.remove_item_from_slot(slot_type, index)
                if item:
                    # Drop the item at the warrior's position
                    game.drop_item(item, game.warrior.grid_x, game.warrior.grid_y)
                    return True

        return False

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

    def _move_item(
        self,
        inventory: Inventory,
        from_slot: Tuple[str, int],
        to_slot: Tuple[str, int],
    ):
        """Move or swap items between slots."""
        from_type, from_index = from_slot
        to_type, to_index = to_slot

        # Get items
        from_item = inventory.remove_item_from_slot(from_type, from_index)
        to_item = inventory.remove_item_from_slot(to_type, to_index)

        if from_item is None:
            return  # Nothing to move

        # Use UI's _place_item_in_slot if available (for testability), otherwise use our own
        place_func = (
            self.ui._place_item_in_slot if self.ui else self._place_item_in_slot
        )

        # Try to place from_item in to_slot
        success = place_func(inventory, from_item, to_type, to_index)

        # If successful and there was an item in to_slot, move it to from_slot
        if success and to_item:
            place_func(inventory, to_item, from_type, from_index)
        elif not success:
            # Couldn't place item, put it back
            place_func(inventory, from_item, from_type, from_index)
            if to_item:
                place_func(inventory, to_item, to_type, to_index)

    def _place_item_in_slot(
        self, inventory: Inventory, item, slot_type: str, slot_index: int
    ) -> bool:
        """Place an item in a specific slot, returns True if successful."""
        if slot_type == "weapon":
            from caislean_gaofar.objects.item import ItemType

            if item.item_type == ItemType.WEAPON or inventory.weapon_slot is None:
                inventory.weapon_slot = item
                return True
        elif slot_type == "armor":
            from caislean_gaofar.objects.item import ItemType

            if item.item_type == ItemType.ARMOR or inventory.armor_slot is None:
                inventory.armor_slot = item
                return True
        elif slot_type == "backpack":
            inventory.backpack_slots[slot_index] = item
            return True
        return False

    def _execute_context_menu_action(
        self, action: str, inventory: Inventory, game=None
    ):
        """Execute the selected context menu action."""
        if not self.state.context_menu_slot:
            return

        slot_type, slot_index = self.state.context_menu_slot

        if action == "Equip":
            if slot_type == "backpack":
                inventory.equip_from_backpack(slot_index)
        elif action == "Drop":
            item = inventory.remove_item_from_slot(slot_type, slot_index)
            if item and game:
                # Drop the item at the warrior's position
                game.drop_item(item, game.warrior.grid_x, game.warrior.grid_y)
