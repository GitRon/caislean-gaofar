"""Shop UI for displaying and interacting with the shop system.

This module provides a coordinated interface for the shop UI,
following the MVC pattern with separate state, rendering, and input handling.
"""

import pygame
from caislean_gaofar.objects.shop import Shop
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.ui.shop_state import ShopState
from caislean_gaofar.ui.shop_renderer import ShopRenderer
from caislean_gaofar.ui.shop_input_handler import ShopInputHandler


class ShopUI:
    """UI overlay for shop system with buy/sell functionality."""

    def __init__(self):
        """Initialize the shop UI with separated concerns."""
        self.state = ShopState()
        self.renderer = ShopRenderer()
        self.input_handler = ShopInputHandler(self.state)

    # Delegate methods to renderer for backward compatibility
    def _wrap_text(self, text, max_width):
        return self.renderer._wrap_text(text, max_width)

    def _draw_item_info(self, screen, item_rect, item, player_gold, shop_item=None):
        return self.renderer._draw_item_info(
            screen, item_rect, item, player_gold, shop_item
        )

    # Delegate methods to state for backward compatibility
    def _show_message(self, message, color=None):
        return self.state.show_message(message, color)

    # Delegate methods to input handler for backward compatibility
    def _handle_buy_click(self, shop, warrior):
        return self.input_handler._handle_buy_click(shop, warrior)

    def _execute_buy(self, shop, warrior, shop_item):
        return self.input_handler._execute_buy(shop, warrior, shop_item)

    def _handle_sell_click(self, shop, warrior):
        return self.input_handler._handle_sell_click(shop, warrior)

    def _execute_sell(self, shop, warrior, item):
        return self.input_handler._execute_sell(shop, warrior, item)

    def draw(self, screen: pygame.Surface, shop: Shop, warrior: Warrior):
        """
        Draw the shop UI overlay.

        Args:
            screen: Pygame surface to draw on
            shop: The shop instance
            warrior: The warrior/player instance
        """
        self.renderer.draw(screen, shop, warrior, self.state)

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
        return self.input_handler.handle_input(event, shop, warrior)
