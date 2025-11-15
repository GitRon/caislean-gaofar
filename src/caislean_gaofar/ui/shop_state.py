"""State management for shop UI."""

from typing import Optional
import pygame
from caislean_gaofar.core import config


class ShopState:
    """Manages the state of the shop UI."""

    def __init__(self):
        """Initialize shop UI state."""
        # Tab state
        self.active_tab = "buy"  # "buy" or "sell"

        # Item list state
        self.selected_item_index: Optional[int] = None
        self.hovered_item_index: Optional[int] = None
        self.item_rects = []  # List of (rect, item/shop_item, index) tuples
        self.scroll_offset = 0  # Vertical scroll offset for item list

        # Button state
        self.buy_button_rect: Optional[pygame.Rect] = None
        self.sell_button_rect: Optional[pygame.Rect] = None
        self.buy_tab_rect: Optional[pygame.Rect] = None
        self.sell_tab_rect: Optional[pygame.Rect] = None

        # Confirmation dialog state
        self.confirmation_dialog: Optional[dict] = (
            None  # {"message": str, "callback": function}
        )

        # Message state
        self.message = ""
        self.message_start_time = 0
        self.message_duration = 3000  # milliseconds
        self.message_color = config.WHITE

    def switch_tab(self, tab: str):
        """
        Switch to a different tab.

        Args:
            tab: The tab to switch to ("buy" or "sell")
        """
        self.active_tab = tab
        self.selected_item_index = None
        self.scroll_offset = 0

    def select_item(self, index: int):
        """Select an item by index."""
        self.selected_item_index = index

    def clear_item_rects(self):
        """Clear item rectangles for a new frame."""
        self.item_rects = []

    def update_scroll(
        self, delta: int, num_items: int, list_height: int, item_height: int
    ):
        """
        Update scroll offset.

        Args:
            delta: The scroll delta amount
            num_items: Total number of items
            list_height: Height of the visible list area
            item_height: Height of each item
        """
        total_height = num_items * (item_height + 5)
        max_scroll = max(0, total_height - list_height)

        self.scroll_offset -= delta
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

    def show_message(self, message: str, color=None):
        """
        Show a message to the player.

        Args:
            message: The message text
            color: The message color (defaults to white)
        """
        self.message = message
        self.message_start_time = pygame.time.get_ticks()
        if color:
            self.message_color = color

    def update_message_timer(self):
        """Update message timer and clear expired messages."""
        if self.message and self.message_start_time > 0:
            elapsed = pygame.time.get_ticks() - self.message_start_time
            if elapsed >= self.message_duration:
                self.message = ""
                self.message_start_time = 0

    def show_confirmation(self, message: str, callback):
        """
        Show a confirmation dialog.

        Args:
            message: The confirmation message
            callback: The function to call if confirmed
        """
        self.confirmation_dialog = {
            "message": message,
            "callback": callback,
        }

    def close_confirmation(self):
        """Close the confirmation dialog."""
        self.confirmation_dialog = None

    def has_confirmation(self) -> bool:
        """Check if a confirmation dialog is active."""
        return self.confirmation_dialog is not None

    def confirm_action(self):
        """Execute the confirmed action."""
        if self.confirmation_dialog:
            callback = self.confirmation_dialog["callback"]
            callback()
            self.close_confirmation()
