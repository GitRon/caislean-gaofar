"""Input handling for shop UI."""

import pygame
from caislean_gaofar.objects.shop import Shop
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.ui.shop_state import ShopState
from caislean_gaofar.core import config


class ShopInputHandler:
    """Handles input events for the shop UI."""

    def __init__(self, state: ShopState):
        """
        Initialize the input handler.

        Args:
            state: The shop state manager
        """
        self.state = state

    def handle_input(
        self, event: pygame.event.Event, shop: Shop, warrior: Warrior
    ) -> bool:
        """
        Handle input events for shop UI.

        Args:
            event: The pygame event to handle
            shop: The shop instance
            warrior: The warrior/player instance

        Returns:
            True if the event was handled
        """
        # Handle mouse wheel scrolling
        if event.type == pygame.MOUSEWHEEL:
            # Get the list of items to calculate max scroll
            if self.state.active_tab == "buy":
                num_items = len(shop.get_available_items())
            else:
                num_items = len(warrior.inventory.get_all_items())

            # Calculate max scroll (ensure we can see all items)
            item_height = 65
            list_height = 310
            scroll_amount = 70  # Pixels per scroll wheel tick

            self.state.update_scroll(
                event.y * scroll_amount, num_items, list_height, item_height
            )
            return True

        # Handle confirmation dialog input first
        if self.state.has_confirmation() and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Type guard: confirmation_dialog is not None after has_confirmation()
                assert self.state.confirmation_dialog is not None
                yes_rect = self.state.confirmation_dialog.get("yes_rect")
                no_rect = self.state.confirmation_dialog.get("no_rect")

                if yes_rect and yes_rect.collidepoint(event.pos):
                    # Execute callback
                    self.state.confirm_action()
                    return True
                elif no_rect and no_rect.collidepoint(event.pos):
                    # Cancel
                    self.state.close_confirmation()
                    return True

        # Handle tab clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.state.buy_tab_rect and self.state.buy_tab_rect.collidepoint(
                event.pos
            ):
                self.state.switch_tab("buy")
                return True
            elif self.state.sell_tab_rect and self.state.sell_tab_rect.collidepoint(
                event.pos
            ):
                self.state.switch_tab("sell")
                return True

        # Handle item selection
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, item_data, actual_index in self.state.item_rects:
                if rect.collidepoint(event.pos):
                    self.state.select_item(actual_index)
                    return True

        # Handle action button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.state.active_tab == "buy" and self.state.buy_button_rect:
                if self.state.buy_button_rect.collidepoint(event.pos):
                    self._handle_buy_click(shop, warrior)
                    return True
            elif self.state.active_tab == "sell" and self.state.sell_button_rect:
                if self.state.sell_button_rect.collidepoint(event.pos):
                    self._handle_sell_click(shop, warrior)
                    return True

        return False

    def _handle_buy_click(self, shop: Shop, warrior: Warrior) -> None:
        """Handle buy button click (requires confirmation)."""
        if self.state.selected_item_index is None:
            return

        # Get selected item
        available_items = shop.get_available_items()
        if self.state.selected_item_index >= len(available_items):
            return

        shop_item = available_items[self.state.selected_item_index]

        # Show confirmation dialog
        message = f"Buy {shop_item.item.name} for {shop_item.item.gold_value} gold?"
        self.state.show_confirmation(
            message, lambda: self._execute_buy(shop, warrior, shop_item)
        )

    def _execute_buy(self, shop: Shop, warrior: Warrior, shop_item):
        """Execute the buy transaction."""
        success, message = shop.buy_item(shop_item, warrior.gold, warrior.inventory)

        if success:
            # Atomic transaction - deduct gold after successful purchase
            warrior.remove_gold(shop_item.item.gold_value)
            self.state.show_message(message, config.GREEN)
            self.state.selected_item_index = None
        else:
            # Show error message
            self.state.show_message(message, config.SHOP_INSUFFICIENT_FUNDS_COLOR)

    def _handle_sell_click(self, shop: Shop, warrior: Warrior) -> None:
        """Handle sell button click (requires confirmation)."""
        if self.state.selected_item_index is None:
            return

        # Get selected item
        player_items = warrior.inventory.get_all_items()
        if self.state.selected_item_index >= len(player_items):
            return

        item = player_items[self.state.selected_item_index]

        # Check if item is sellable
        if item.unsellable:
            self.state.show_message("This item cannot be sold!", config.RED)
            return

        # Show confirmation dialog
        message = f"Sell {item.name} for {item.sell_price} gold?"
        self.state.show_confirmation(
            message, lambda: self._execute_sell(shop, warrior, item)
        )

    def _execute_sell(self, shop: Shop, warrior: Warrior, item):
        """Execute the sell transaction."""
        success, message, gold_earned = shop.sell_item(item, warrior.inventory)

        if success:
            # Atomic transaction - add gold after successful sale
            warrior.add_gold(gold_earned)
            self.state.show_message(message, config.GREEN)
            self.state.selected_item_index = None
        else:
            self.state.show_message(message, config.RED)
