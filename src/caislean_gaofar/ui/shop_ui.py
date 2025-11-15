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

    # Property delegation for backward compatibility with tests
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
    def active_tab(self):
        return self.state.active_tab

    @active_tab.setter
    def active_tab(self, value):
        self.state.active_tab = value

    @property
    def tab_height(self):
        return self.renderer.tab_height

    @property
    def selected_item_index(self):
        return self.state.selected_item_index

    @selected_item_index.setter
    def selected_item_index(self, value):
        self.state.selected_item_index = value

    @property
    def hovered_item_index(self):
        return self.state.hovered_item_index

    @hovered_item_index.setter
    def hovered_item_index(self, value):
        self.state.hovered_item_index = value

    @property
    def item_rects(self):
        return self.state.item_rects

    @item_rects.setter
    def item_rects(self, value):
        self.state.item_rects = value

    @property
    def scroll_offset(self):
        return self.state.scroll_offset

    @scroll_offset.setter
    def scroll_offset(self, value):
        self.state.scroll_offset = value

    @property
    def buy_button_rect(self):
        return self.state.buy_button_rect

    @buy_button_rect.setter
    def buy_button_rect(self, value):
        self.state.buy_button_rect = value

    @property
    def sell_button_rect(self):
        return self.state.sell_button_rect

    @sell_button_rect.setter
    def sell_button_rect(self, value):
        self.state.sell_button_rect = value

    @property
    def buy_tab_rect(self):
        return self.state.buy_tab_rect

    @buy_tab_rect.setter
    def buy_tab_rect(self, value):
        self.state.buy_tab_rect = value

    @property
    def sell_tab_rect(self):
        return self.state.sell_tab_rect

    @sell_tab_rect.setter
    def sell_tab_rect(self, value):
        self.state.sell_tab_rect = value

    @property
    def confirmation_dialog(self):
        return self.state.confirmation_dialog

    @confirmation_dialog.setter
    def confirmation_dialog(self, value):
        self.state.confirmation_dialog = value

    @property
    def message(self):
        return self.state.message

    @message.setter
    def message(self, value):
        self.state.message = value

    @property
    def message_start_time(self):
        return self.state.message_start_time

    @message_start_time.setter
    def message_start_time(self, value):
        self.state.message_start_time = value

    @property
    def message_duration(self):
        return self.state.message_duration

    @property
    def message_color(self):
        return self.state.message_color

    @message_color.setter
    def message_color(self, value):
        self.state.message_color = value

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
