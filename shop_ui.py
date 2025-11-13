"""Shop UI for displaying and interacting with the shop system."""

import pygame
from typing import Optional
from shop import Shop, ShopItem
from warrior import Warrior
import config


class ShopUI:
    """UI overlay for shop system with buy/sell functionality."""

    def __init__(self):
        """Initialize the shop UI."""
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 20)
        self.desc_font = pygame.font.Font(None, 18)

        # UI positioning
        self.panel_width = 700
        self.panel_height = 550
        self.padding = 20

        # Tab state
        self.active_tab = "buy"  # "buy" or "sell"
        self.tab_height = 50

        # Item list state
        self.selected_item_index = None
        self.hovered_item_index = None
        self.item_rects = []  # List of (rect, item/shop_item) tuples
        self.scroll_offset = 0  # Vertical scroll offset for item list

        # Button state
        self.buy_button_rect = None
        self.sell_button_rect = None
        self.buy_tab_rect = None
        self.sell_tab_rect = None

        # Confirmation dialog state
        self.confirmation_dialog = None  # {"message": str, "callback": function}

        # Message state
        self.message = ""
        self.message_start_time = 0
        self.message_duration = 3000  # milliseconds
        self.message_color = config.WHITE

    def draw(self, screen: pygame.Surface, shop: Shop, warrior: Warrior):
        """
        Draw the shop UI overlay.

        Args:
            screen: Pygame surface to draw on
            shop: The shop instance
            warrior: The warrior/player instance
        """
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Update message timer
        if self.message and self.message_start_time > 0:
            elapsed = pygame.time.get_ticks() - self.message_start_time
            if elapsed >= self.message_duration:
                self.message = ""
                self.message_start_time = 0

        # Center the panel
        panel_x = (screen_width - self.panel_width) // 2
        panel_y = (screen_height - self.panel_height) // 2

        # Draw semi-transparent background
        overlay = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        overlay.fill((*config.SHOP_BACKGROUND_COLOR, 240))
        screen.blit(overlay, (panel_x, panel_y))

        # Draw border
        pygame.draw.rect(
            screen,
            config.SHOP_BORDER_COLOR,
            (panel_x, panel_y, self.panel_width, self.panel_height),
            3,
        )

        # Draw title
        title_text = self.title_font.render("SHOP", True, config.SHOP_TEXT_COLOR)
        title_x = panel_x + (self.panel_width - title_text.get_width()) // 2
        screen.blit(title_text, (title_x, panel_y + 10))

        # Draw tabs
        tab_y = panel_y + 70
        self._draw_tabs(screen, panel_x, tab_y)

        # Draw player info (gold and inventory capacity)
        info_y = tab_y + self.tab_height + 10
        self._draw_player_info(screen, panel_x, info_y, warrior)

        # Draw item list based on active tab
        list_y = info_y + 40
        if self.active_tab == "buy":
            self._draw_buy_list(screen, panel_x, list_y, shop, warrior)
        else:
            self._draw_sell_list(screen, panel_x, list_y, shop, warrior)

        # Draw action button
        button_y = panel_y + self.panel_height - 70
        self._draw_action_button(screen, panel_x, button_y, shop, warrior)

        # Draw instructions
        self._draw_instructions(screen, panel_x, panel_y)

        # Draw message if active
        if self.message:
            self._draw_message(screen, panel_x, panel_y)

        # Draw confirmation dialog if active
        if self.confirmation_dialog:
            self._draw_confirmation_dialog(screen, panel_x, panel_y)

    def _draw_tabs(self, screen: pygame.Surface, panel_x: int, tab_y: int):
        """Draw buy/sell tabs."""
        tab_width = self.panel_width // 2

        # Buy tab
        buy_tab_color = (
            config.SHOP_TAB_ACTIVE_COLOR
            if self.active_tab == "buy"
            else config.SHOP_TAB_COLOR
        )
        self.buy_tab_rect = pygame.Rect(panel_x, tab_y, tab_width, self.tab_height)
        pygame.draw.rect(screen, buy_tab_color, self.buy_tab_rect)
        pygame.draw.rect(screen, config.SHOP_BORDER_COLOR, self.buy_tab_rect, 2)

        buy_text = self.font.render("BUY", True, config.SHOP_TEXT_COLOR)
        buy_text_x = panel_x + (tab_width - buy_text.get_width()) // 2
        buy_text_y = tab_y + (self.tab_height - buy_text.get_height()) // 2
        screen.blit(buy_text, (buy_text_x, buy_text_y))

        # Sell tab
        sell_tab_color = (
            config.SHOP_TAB_ACTIVE_COLOR
            if self.active_tab == "sell"
            else config.SHOP_TAB_COLOR
        )
        self.sell_tab_rect = pygame.Rect(
            panel_x + tab_width, tab_y, tab_width, self.tab_height
        )
        pygame.draw.rect(screen, sell_tab_color, self.sell_tab_rect)
        pygame.draw.rect(screen, config.SHOP_BORDER_COLOR, self.sell_tab_rect, 2)

        sell_text = self.font.render("SELL", True, config.SHOP_TEXT_COLOR)
        sell_text_x = panel_x + tab_width + (tab_width - sell_text.get_width()) // 2
        sell_text_y = tab_y + (self.tab_height - sell_text.get_height()) // 2
        screen.blit(sell_text, (sell_text_x, sell_text_y))

    def _draw_player_info(
        self, screen: pygame.Surface, panel_x: int, info_y: int, warrior: Warrior
    ):
        """Draw player gold and inventory capacity (AC13)."""
        # Gold
        gold_text = self.font.render(f"Gold: {warrior.gold}", True, config.GOLD)
        screen.blit(gold_text, (panel_x + self.padding, info_y))

        # Inventory capacity
        total_items = len(warrior.inventory.get_all_items())
        max_slots = 15  # 1 weapon + 1 armor + 13 backpack
        capacity_text = self.font.render(
            f"Inventory: {total_items}/{max_slots}", True, config.SHOP_TEXT_COLOR
        )
        capacity_x = (
            panel_x + self.panel_width - capacity_text.get_width() - self.padding
        )
        screen.blit(capacity_text, (capacity_x, info_y))

    def _draw_buy_list(
        self,
        screen: pygame.Surface,
        panel_x: int,
        list_y: int,
        shop: Shop,
        warrior: Warrior,
    ):
        """Draw list of items available for purchase (AC1)."""
        self.item_rects = []
        item_height = 65
        list_height = 310
        mouse_pos = pygame.mouse.get_pos()

        # Get available items
        available_items = shop.get_available_items()

        # Draw scrollable list area
        list_rect = pygame.Rect(
            panel_x + self.padding,
            list_y,
            self.panel_width - 2 * self.padding,
            list_height,
        )
        pygame.draw.rect(screen, (30, 30, 40), list_rect)
        pygame.draw.rect(screen, config.SHOP_BORDER_COLOR, list_rect, 2)

        # Enable clipping to prevent overflow
        original_clip = screen.get_clip()
        screen.set_clip(list_rect)

        # Draw each item
        for i, shop_item in enumerate(available_items):
            item_y = list_y + 5 + i * (item_height + 5) - self.scroll_offset
            item_rect = pygame.Rect(
                panel_x + self.padding + 5,
                item_y,
                self.panel_width
                - 2 * self.padding
                - 10
                - 20,  # Leave space for scrollbar
                item_height,
            )

            # Skip items that are above the visible area
            if item_y + item_height < list_y:
                continue

            # Check if item is within list bounds
            if item_y > list_y + list_height:
                break

            # Store rect for click detection with actual item index
            self.item_rects.append((item_rect, shop_item, i))

            # Check if hovered or selected
            is_hovered = item_rect.collidepoint(mouse_pos)
            is_selected = self.selected_item_index == i

            # Draw item background
            if is_selected:
                bg_color = config.SHOP_HIGHLIGHT_COLOR
            elif is_hovered:
                bg_color = (70, 70, 110)
                self.hovered_item_index = i
            else:
                bg_color = (50, 50, 70)

            pygame.draw.rect(screen, bg_color, item_rect)
            pygame.draw.rect(screen, config.SHOP_BORDER_COLOR, item_rect, 1)

            # Draw item info
            self._draw_item_info(
                screen, item_rect, shop_item.item, warrior.gold, shop_item
            )

        # Restore original clipping
        screen.set_clip(original_clip)

        # Draw scrollbar if needed
        self._draw_scrollbar(
            screen, panel_x, list_y, list_height, len(available_items), item_height
        )

    def _draw_sell_list(
        self,
        screen: pygame.Surface,
        panel_x: int,
        list_y: int,
        shop: Shop,
        warrior: Warrior,
    ):
        """Draw list of items player can sell (AC6)."""
        self.item_rects = []
        item_height = 65
        list_height = 310
        mouse_pos = pygame.mouse.get_pos()

        # Get all player items
        player_items = warrior.inventory.get_all_items()

        # Draw scrollable list area
        list_rect = pygame.Rect(
            panel_x + self.padding,
            list_y,
            self.panel_width - 2 * self.padding,
            list_height,
        )
        pygame.draw.rect(screen, (30, 30, 40), list_rect)
        pygame.draw.rect(screen, config.SHOP_BORDER_COLOR, list_rect, 2)

        # Enable clipping to prevent overflow
        original_clip = screen.get_clip()
        screen.set_clip(list_rect)

        # Draw each item
        for i, item in enumerate(player_items):
            item_y = list_y + 5 + i * (item_height + 5) - self.scroll_offset
            item_rect = pygame.Rect(
                panel_x + self.padding + 5,
                item_y,
                self.panel_width
                - 2 * self.padding
                - 10
                - 20,  # Leave space for scrollbar
                item_height,
            )

            # Skip items that are above the visible area
            if item_y + item_height < list_y:
                continue

            # Check if item is within list bounds
            if item_y > list_y + list_height:
                break

            # Store rect for click detection with actual item index
            self.item_rects.append((item_rect, item, i))

            # Check if hovered or selected
            is_hovered = item_rect.collidepoint(mouse_pos)
            is_selected = self.selected_item_index == i

            # Draw item background
            if is_selected:
                bg_color = config.SHOP_HIGHLIGHT_COLOR
            elif is_hovered:
                bg_color = (70, 70, 110)
                self.hovered_item_index = i
            else:
                bg_color = (50, 50, 70)

            pygame.draw.rect(screen, bg_color, item_rect)
            pygame.draw.rect(screen, config.SHOP_BORDER_COLOR, item_rect, 1)

            # Draw item info for selling
            self._draw_item_info_sell(screen, item_rect, item)

        # Restore original clipping
        screen.set_clip(original_clip)

        # Draw scrollbar if needed
        self._draw_scrollbar(
            screen, panel_x, list_y, list_height, len(player_items), item_height
        )

    def _draw_item_info(
        self,
        screen: pygame.Surface,
        item_rect: pygame.Rect,
        item,
        player_gold: int,
        shop_item: Optional[ShopItem] = None,
    ):
        """Draw item information for buying (AC1)."""
        padding = 8

        # Item name
        name_text = self.font.render(item.name, True, config.SHOP_TEXT_COLOR)
        screen.blit(name_text, (item_rect.x + padding, item_rect.y + padding))

        # Description
        desc_text = self.desc_font.render(item.description, True, (200, 200, 200))
        screen.blit(desc_text, (item_rect.x + padding, item_rect.y + padding + 22))

        # Stats
        stats_text = ""
        if item.attack_bonus > 0:
            stats_text += f"+{item.attack_bonus} ATK  "
        if item.defense_bonus > 0:
            stats_text += f"+{item.defense_bonus} DEF  "

        if stats_text:
            stats_render = self.small_font.render(stats_text, True, (150, 200, 150))
            screen.blit(
                stats_render, (item_rect.x + padding, item_rect.y + padding + 42)
            )

        # Price (AC1, AC4)
        price_color = (
            config.GOLD
            if player_gold >= item.gold_value
            else config.SHOP_INSUFFICIENT_FUNDS_COLOR
        )
        price_text = self.font.render(f"{item.gold_value} gold", True, price_color)
        price_x = item_rect.x + item_rect.width - price_text.get_width() - padding
        screen.blit(price_text, (price_x, item_rect.y + padding))

        # Quantity (AC1)
        if shop_item:
            if shop_item.infinite:
                qty_text = self.small_font.render("∞", True, (150, 200, 255))
            else:
                qty_text = self.small_font.render(
                    f"x{shop_item.quantity}", True, (150, 200, 255)
                )
            qty_x = item_rect.x + item_rect.width - qty_text.get_width() - padding
            screen.blit(qty_text, (qty_x, item_rect.y + padding + 25))

    def _draw_item_info_sell(
        self, screen: pygame.Surface, item_rect: pygame.Rect, item
    ):
        """Draw item information for selling (AC6, AC9)."""
        padding = 8

        # Item name
        name_text = self.font.render(item.name, True, config.SHOP_TEXT_COLOR)
        screen.blit(name_text, (item_rect.x + padding, item_rect.y + padding))

        # Description
        desc_text = self.desc_font.render(item.description, True, (200, 200, 200))
        screen.blit(desc_text, (item_rect.x + padding, item_rect.y + padding + 22))

        # Stats
        stats_text = ""
        if item.attack_bonus > 0:
            stats_text += f"+{item.attack_bonus} ATK  "
        if item.defense_bonus > 0:
            stats_text += f"+{item.defense_bonus} DEF  "

        if stats_text:
            stats_render = self.small_font.render(stats_text, True, (150, 200, 150))
            screen.blit(
                stats_render, (item_rect.x + padding, item_rect.y + padding + 42)
            )

        # Sell price or unsellable (AC9)
        if item.unsellable:
            price_text = self.font.render("Unsellable", True, config.RED)
        else:
            price_text = self.font.render(
                f"Sell: {item.sell_price} gold", True, config.GOLD
            )

        price_x = item_rect.x + item_rect.width - price_text.get_width() - padding
        screen.blit(price_text, (price_x, item_rect.y + padding))

    def _draw_action_button(
        self,
        screen: pygame.Surface,
        panel_x: int,
        button_y: int,
        shop: Shop,
        warrior: Warrior,
    ):
        """Draw buy/sell button with hover effect."""
        button_width = 200
        button_height = 40
        button_x = panel_x + (self.panel_width - button_width) // 2

        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouse_pos)

        # Store button rect for click detection
        if self.active_tab == "buy":
            self.buy_button_rect = button_rect
            button_text = "BUY ITEM"
        else:
            self.sell_button_rect = button_rect
            button_text = "SELL ITEM"

        # Determine if button is enabled
        is_enabled = self.selected_item_index is not None

        # Draw button
        if not is_enabled:
            button_color = (50, 50, 50)
            text_color = (100, 100, 100)
        elif is_hovered:
            button_color = config.SHOP_BUTTON_HOVER_COLOR
            text_color = config.WHITE
        else:
            button_color = config.SHOP_BUTTON_COLOR
            text_color = config.WHITE

        pygame.draw.rect(screen, button_color, button_rect)
        pygame.draw.rect(screen, config.SHOP_BORDER_COLOR, button_rect, 2)

        # Draw button text
        text_render = self.font.render(button_text, True, text_color)
        text_x = button_x + (button_width - text_render.get_width()) // 2
        text_y = button_y + (button_height - text_render.get_height()) // 2
        screen.blit(text_render, (text_x, text_y))

    def _draw_instructions(self, screen: pygame.Surface, panel_x: int, panel_y: int):
        """Draw control instructions."""
        instructions = "Press ESC or I to close shop"
        text = self.small_font.render(instructions, True, (180, 180, 180))
        text_x = panel_x + self.padding
        text_y = panel_y + self.panel_height - 25
        screen.blit(text, (text_x, text_y))

    def _draw_message(self, screen: pygame.Surface, panel_x: int, panel_y: int):
        """Draw message at bottom of panel."""
        text = self.font.render(self.message, True, self.message_color)
        text_x = panel_x + (self.panel_width - text.get_width()) // 2
        text_y = panel_y + self.panel_height - 100

        # Draw background
        padding = 10
        bg_rect = pygame.Rect(
            text_x - padding,
            text_y - padding,
            text.get_width() + 2 * padding,
            text.get_height() + 2 * padding,
        )
        pygame.draw.rect(screen, (30, 30, 40), bg_rect)
        pygame.draw.rect(screen, config.SHOP_BORDER_COLOR, bg_rect, 2)

        screen.blit(text, (text_x, text_y))

    def _draw_confirmation_dialog(
        self, screen: pygame.Surface, panel_x: int, panel_y: int
    ):
        """Draw confirmation dialog (AC16)."""
        dialog_width = 400
        dialog_height = 150
        dialog_x = panel_x + (self.panel_width - dialog_width) // 2
        dialog_y = panel_y + (self.panel_height - dialog_height) // 2

        # Draw dialog background
        dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
        dialog_surface.fill((40, 40, 60, 250))
        screen.blit(dialog_surface, (dialog_x, dialog_y))
        pygame.draw.rect(
            screen,
            config.SHOP_BORDER_COLOR,
            (dialog_x, dialog_y, dialog_width, dialog_height),
            3,
        )

        # Draw message
        message = self.confirmation_dialog["message"]
        message_lines = self._wrap_text(message, dialog_width - 40)
        for i, line in enumerate(message_lines):
            text = self.font.render(line, True, config.WHITE)
            text_x = dialog_x + (dialog_width - text.get_width()) // 2
            text_y = dialog_y + 20 + i * 25
            screen.blit(text, (text_x, text_y))

        # Draw buttons
        button_width = 100
        button_height = 35
        button_y = dialog_y + dialog_height - button_height - 20

        # Yes button
        yes_button_x = dialog_x + dialog_width // 2 - button_width - 10
        yes_button_rect = pygame.Rect(
            yes_button_x, button_y, button_width, button_height
        )
        mouse_pos = pygame.mouse.get_pos()
        yes_hovered = yes_button_rect.collidepoint(mouse_pos)

        yes_color = (
            config.SHOP_BUTTON_HOVER_COLOR if yes_hovered else config.SHOP_BUTTON_COLOR
        )
        pygame.draw.rect(screen, yes_color, yes_button_rect)
        pygame.draw.rect(screen, config.SHOP_BORDER_COLOR, yes_button_rect, 2)

        yes_text = self.font.render("Yes", True, config.WHITE)
        yes_text_x = yes_button_x + (button_width - yes_text.get_width()) // 2
        yes_text_y = button_y + (button_height - yes_text.get_height()) // 2
        screen.blit(yes_text, (yes_text_x, yes_text_y))

        # No button
        no_button_x = dialog_x + dialog_width // 2 + 10
        no_button_rect = pygame.Rect(no_button_x, button_y, button_width, button_height)
        no_hovered = no_button_rect.collidepoint(mouse_pos)

        no_color = (150, 50, 50) if no_hovered else (100, 30, 30)
        pygame.draw.rect(screen, no_color, no_button_rect)
        pygame.draw.rect(screen, config.SHOP_BORDER_COLOR, no_button_rect, 2)

        no_text = self.font.render("No", True, config.WHITE)
        no_text_x = no_button_x + (button_width - no_text.get_width()) // 2
        no_text_y = button_y + (button_height - no_text.get_height()) // 2
        screen.blit(no_text, (no_text_x, no_text_y))

        # Store button rects for click detection
        self.confirmation_dialog["yes_rect"] = yes_button_rect
        self.confirmation_dialog["no_rect"] = no_button_rect

    def _draw_scrollbar(
        self,
        screen: pygame.Surface,
        panel_x: int,
        list_y: int,
        list_height: int,
        num_items: int,
        item_height: int,
    ):
        """Draw scrollbar indicator if content is scrollable."""
        # Calculate if scrollbar is needed
        total_content_height = num_items * (item_height + 5)
        if total_content_height <= list_height:
            return  # No scrollbar needed

        # Scrollbar dimensions
        scrollbar_width = 12
        scrollbar_x = panel_x + self.panel_width - self.padding - scrollbar_width - 5
        scrollbar_track_rect = pygame.Rect(
            scrollbar_x, list_y + 5, scrollbar_width, list_height - 10
        )

        # Draw scrollbar track
        pygame.draw.rect(screen, (40, 40, 50), scrollbar_track_rect, border_radius=6)

        # Calculate scrollbar thumb size and position
        visible_ratio = list_height / total_content_height
        thumb_height = max(30, int(scrollbar_track_rect.height * visible_ratio))

        max_scroll = total_content_height - list_height
        scroll_ratio = self.scroll_offset / max_scroll if max_scroll > 0 else 0
        thumb_y = scrollbar_track_rect.y + scroll_ratio * (
            scrollbar_track_rect.height - thumb_height
        )

        thumb_rect = pygame.Rect(scrollbar_x, thumb_y, scrollbar_width, thumb_height)

        # Draw scrollbar thumb
        pygame.draw.rect(screen, (100, 100, 120), thumb_rect, border_radius=6)
        pygame.draw.rect(
            screen, config.SHOP_BORDER_COLOR, thumb_rect, 1, border_radius=6
        )

        # Draw scroll hint text if at top
        if self.scroll_offset == 0 and num_items > 4:
            hint_text = self.small_font.render("Scroll ↓", True, (150, 150, 150))
            hint_x = scrollbar_x - hint_text.get_width() - 10
            hint_y = list_y + list_height - 25
            screen.blit(hint_text, (hint_x, hint_y))

    def _wrap_text(self, text: str, max_width: int) -> list:
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines

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
            if self.active_tab == "buy":
                num_items = len(shop.get_available_items())
            else:
                num_items = len(warrior.inventory.get_all_items())

            # Calculate max scroll (ensure we can see all items)
            item_height = 65
            list_height = 310
            total_height = num_items * (item_height + 5)
            max_scroll = max(0, total_height - list_height)

            # Update scroll offset
            scroll_amount = 70  # Pixels per scroll wheel tick
            self.scroll_offset -= event.y * scroll_amount
            self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
            return True

        # Handle confirmation dialog input first
        if self.confirmation_dialog and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                yes_rect = self.confirmation_dialog.get("yes_rect")
                no_rect = self.confirmation_dialog.get("no_rect")

                if yes_rect and yes_rect.collidepoint(event.pos):
                    # Execute callback
                    callback = self.confirmation_dialog["callback"]
                    callback()
                    self.confirmation_dialog = None
                    return True
                elif no_rect and no_rect.collidepoint(event.pos):
                    # Cancel
                    self.confirmation_dialog = None
                    return True

        # Handle tab clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.buy_tab_rect and self.buy_tab_rect.collidepoint(event.pos):
                self.active_tab = "buy"
                self.selected_item_index = None
                self.scroll_offset = 0  # Reset scroll when switching tabs
                return True
            elif self.sell_tab_rect and self.sell_tab_rect.collidepoint(event.pos):
                self.active_tab = "sell"
                self.selected_item_index = None
                self.scroll_offset = 0  # Reset scroll when switching tabs
                return True

        # Handle item selection
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, item_data, actual_index in self.item_rects:
                if rect.collidepoint(event.pos):
                    self.selected_item_index = actual_index
                    return True

        # Handle action button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.active_tab == "buy" and self.buy_button_rect:
                if self.buy_button_rect.collidepoint(event.pos):
                    self._handle_buy_click(shop, warrior)
                    return True
            elif self.active_tab == "sell" and self.sell_button_rect:
                if self.sell_button_rect.collidepoint(event.pos):
                    self._handle_sell_click(shop, warrior)
                    return True

        return False

    def _handle_buy_click(self, shop: Shop, warrior: Warrior):
        """Handle buy button click (AC16 - requires confirmation)."""
        if self.selected_item_index is None:
            return

        # Get selected item
        available_items = shop.get_available_items()
        if self.selected_item_index >= len(available_items):
            return

        shop_item = available_items[self.selected_item_index]

        # Show confirmation dialog (AC16)
        message = f"Buy {shop_item.item.name} for {shop_item.item.gold_value} gold?"
        self.confirmation_dialog = {
            "message": message,
            "callback": lambda: self._execute_buy(shop, warrior, shop_item),
        }

    def _execute_buy(self, shop: Shop, warrior: Warrior, shop_item: ShopItem):
        """Execute the buy transaction (AC2, AC3, AC4, AC14)."""
        success, message = shop.buy_item(shop_item, warrior.gold, warrior.inventory)

        if success:
            # AC3, AC14: Atomic transaction - deduct gold after successful purchase
            warrior.remove_gold(shop_item.item.gold_value)
            self.message_color = config.GREEN
            self.selected_item_index = None
        else:
            # AC4: Show error message
            self.message_color = config.SHOP_INSUFFICIENT_FUNDS_COLOR

        self._show_message(message)

    def _handle_sell_click(self, shop: Shop, warrior: Warrior):
        """Handle sell button click (AC16 - requires confirmation)."""
        if self.selected_item_index is None:
            return

        # Get selected item
        player_items = warrior.inventory.get_all_items()
        if self.selected_item_index >= len(player_items):
            return

        item = player_items[self.selected_item_index]

        # Check if item is sellable (AC9)
        if item.unsellable:
            self._show_message("This item cannot be sold!")
            self.message_color = config.RED
            return

        # Show confirmation dialog (AC16)
        message = f"Sell {item.name} for {item.sell_price} gold?"
        self.confirmation_dialog = {
            "message": message,
            "callback": lambda: self._execute_sell(shop, warrior, item),
        }

    def _execute_sell(self, shop: Shop, warrior: Warrior, item):
        """Execute the sell transaction (AC7, AC8, AC10, AC14)."""
        success, message, gold_earned = shop.sell_item(item, warrior.inventory)

        if success:
            # AC8, AC14: Atomic transaction - add gold after successful sale
            warrior.add_gold(gold_earned)
            self.message_color = config.GREEN
            self.selected_item_index = None
        else:
            self.message_color = config.RED

        self._show_message(message)

    def _show_message(self, message: str):
        """Show a message to the player."""
        self.message = message
        self.message_start_time = pygame.time.get_ticks()
