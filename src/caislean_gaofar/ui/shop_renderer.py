"""Rendering logic for shop UI."""

import pygame
from typing import Optional
from caislean_gaofar.objects.shop import Shop, ShopItem
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.core import config
from caislean_gaofar.ui.shop_state import ShopState
from caislean_gaofar.ui.ui_constants import UIConstants as UI
from caislean_gaofar.ui.ui_drawing_utils import UIDrawingUtils as Draw


class ShopRenderer:
    """Handles rendering of the shop UI."""

    def __init__(self):
        """Initialize the shop renderer with fonts and visual settings."""
        self.font = pygame.font.Font(None, UI.FONT_SIZE_SMALL)
        self.title_font = pygame.font.Font(None, UI.FONT_SIZE_TITLE)
        self.small_font = pygame.font.Font(None, UI.FONT_SIZE_INFO)
        self.desc_font = pygame.font.Font(None, UI.FONT_SIZE_DETAIL)

        # UI positioning (using constants)
        self.panel_width = UI.SHOP_PANEL_WIDTH
        self.panel_height = UI.SHOP_PANEL_HEIGHT
        self.padding = UI.SHOP_PANEL_PADDING
        self.tab_height = UI.SHOP_TAB_HEIGHT

    def draw(
        self,
        screen: pygame.Surface,
        shop: Shop,
        warrior: Warrior,
        state: ShopState,
    ):
        """
        Draw the shop UI overlay.

        Args:
            screen: Pygame surface to draw on
            shop: The shop instance
            warrior: The warrior/player instance
            state: The current shop state
        """
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Update message timer
        state.update_message_timer()

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
        self._draw_tabs(screen, panel_x, tab_y, state)

        # Draw player info (gold and inventory capacity)
        info_y = tab_y + self.tab_height + 10
        self._draw_player_info(screen, panel_x, info_y, warrior)

        # Draw item list based on active tab
        list_y = info_y + 40
        if state.active_tab == "buy":
            self._draw_buy_list(screen, panel_x, list_y, shop, warrior, state)
        else:
            self._draw_sell_list(screen, panel_x, list_y, shop, warrior, state)

        # Draw action button
        button_y = panel_y + self.panel_height - 70
        self._draw_action_button(screen, panel_x, button_y, shop, warrior, state)

        # Draw instructions
        self._draw_instructions(screen, panel_x, panel_y)

        # Draw message if active
        if state.message:
            self._draw_message(screen, panel_x, panel_y, state)

        # Draw confirmation dialog if active
        if state.has_confirmation():
            self._draw_confirmation_dialog(screen, panel_x, panel_y, state)

    def _draw_tabs(
        self, screen: pygame.Surface, panel_x: int, tab_y: int, state: ShopState
    ):
        """Draw buy/sell tabs."""
        tab_width = self.panel_width // 2

        # Buy tab
        buy_tab_color = (
            config.SHOP_TAB_ACTIVE_COLOR
            if state.active_tab == "buy"
            else config.SHOP_TAB_COLOR
        )
        state.buy_tab_rect = pygame.Rect(panel_x, tab_y, tab_width, self.tab_height)
        pygame.draw.rect(screen, buy_tab_color, state.buy_tab_rect)
        pygame.draw.rect(screen, config.SHOP_BORDER_COLOR, state.buy_tab_rect, 2)

        buy_text = self.font.render("BUY", True, config.SHOP_TEXT_COLOR)
        buy_text_x = panel_x + (tab_width - buy_text.get_width()) // 2
        buy_text_y = tab_y + (self.tab_height - buy_text.get_height()) // 2
        screen.blit(buy_text, (buy_text_x, buy_text_y))

        # Sell tab
        sell_tab_color = (
            config.SHOP_TAB_ACTIVE_COLOR
            if state.active_tab == "sell"
            else config.SHOP_TAB_COLOR
        )
        state.sell_tab_rect = pygame.Rect(
            panel_x + tab_width, tab_y, tab_width, self.tab_height
        )
        pygame.draw.rect(screen, sell_tab_color, state.sell_tab_rect)
        pygame.draw.rect(screen, config.SHOP_BORDER_COLOR, state.sell_tab_rect, 2)

        sell_text = self.font.render("SELL", True, config.SHOP_TEXT_COLOR)
        sell_text_x = panel_x + tab_width + (tab_width - sell_text.get_width()) // 2
        sell_text_y = tab_y + (self.tab_height - sell_text.get_height()) // 2
        screen.blit(sell_text, (sell_text_x, sell_text_y))

    def _draw_player_info(
        self, screen: pygame.Surface, panel_x: int, info_y: int, warrior: Warrior
    ):
        """Draw player gold and inventory capacity."""
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
        state: ShopState,
    ):
        """Draw list of items available for purchase."""
        state.clear_item_rects()
        item_height = UI.SHOP_ITEM_HEIGHT
        list_height = UI.SHOP_LIST_HEIGHT
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
        pygame.draw.rect(screen, UI.SHOP_LIST_BG_COLOR, list_rect)
        pygame.draw.rect(
            screen, config.SHOP_BORDER_COLOR, list_rect, UI.BORDER_WIDTH_THIN
        )

        # Enable clipping to prevent overflow
        original_clip = screen.get_clip()
        screen.set_clip(list_rect)

        # Draw each item
        for i, shop_item in enumerate(available_items):
            item_y = list_y + 5 + i * (item_height + 5) - state.scroll_offset
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

            # Check if item rect would extend beyond list bounds
            if item_y + item_height > list_y + list_height:
                break

            # Store rect for click detection with actual item index
            state.item_rects.append((item_rect, shop_item, i))

            # Check if hovered or selected
            is_hovered = item_rect.collidepoint(mouse_pos)
            is_selected = state.selected_item_index == i

            # Draw item background
            if is_selected:
                bg_color = config.SHOP_HIGHLIGHT_COLOR
            elif is_hovered:
                bg_color = UI.SHOP_ITEM_HOVER_COLOR
                state.hovered_item_index = i
            else:
                bg_color = UI.SHOP_ITEM_BG_COLOR

            pygame.draw.rect(screen, bg_color, item_rect)
            pygame.draw.rect(
                screen, config.SHOP_BORDER_COLOR, item_rect, UI.BORDER_WIDTH_MINIMAL
            )

            # Draw item info
            self._draw_item_info(
                screen, item_rect, shop_item.item, warrior.gold, shop_item
            )

        # Restore original clipping
        screen.set_clip(original_clip)

        # Draw scrollbar if needed
        self._draw_scrollbar(
            screen,
            panel_x,
            list_y,
            list_height,
            len(available_items),
            item_height,
            state,
        )

    def _draw_sell_list(
        self,
        screen: pygame.Surface,
        panel_x: int,
        list_y: int,
        shop: Shop,
        warrior: Warrior,
        state: ShopState,
    ):
        """Draw list of items player can sell."""
        state.clear_item_rects()
        item_height = UI.SHOP_ITEM_HEIGHT
        list_height = UI.SHOP_LIST_HEIGHT
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
        pygame.draw.rect(screen, UI.SHOP_LIST_BG_COLOR, list_rect)
        pygame.draw.rect(
            screen, config.SHOP_BORDER_COLOR, list_rect, UI.BORDER_WIDTH_THIN
        )

        # Enable clipping to prevent overflow
        original_clip = screen.get_clip()
        screen.set_clip(list_rect)

        # Draw each item
        for i, item in enumerate(player_items):
            item_y = list_y + 5 + i * (item_height + 5) - state.scroll_offset
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

            # Check if item rect would extend beyond list bounds
            if item_y + item_height > list_y + list_height:
                break

            # Store rect for click detection with actual item index
            state.item_rects.append((item_rect, item, i))

            # Check if hovered or selected
            is_hovered = item_rect.collidepoint(mouse_pos)
            is_selected = state.selected_item_index == i

            # Draw item background
            if is_selected:
                bg_color = config.SHOP_HIGHLIGHT_COLOR
            elif is_hovered:
                bg_color = UI.SHOP_ITEM_HOVER_COLOR
                state.hovered_item_index = i
            else:
                bg_color = UI.SHOP_ITEM_BG_COLOR

            pygame.draw.rect(screen, bg_color, item_rect)
            pygame.draw.rect(
                screen, config.SHOP_BORDER_COLOR, item_rect, UI.BORDER_WIDTH_MINIMAL
            )

            # Draw item info for selling
            self._draw_item_info_sell(screen, item_rect, item)

        # Restore original clipping
        screen.set_clip(original_clip)

        # Draw scrollbar if needed
        self._draw_scrollbar(
            screen, panel_x, list_y, list_height, len(player_items), item_height, state
        )

    def _draw_item_info(
        self,
        screen: pygame.Surface,
        item_rect: pygame.Rect,
        item,
        player_gold: int,
        shop_item: Optional[ShopItem] = None,
    ):
        """Draw item information for buying."""
        padding = UI.SHOP_ITEM_PADDING

        # Item name
        name_text = self.font.render(item.name, True, config.SHOP_TEXT_COLOR)
        screen.blit(name_text, (item_rect.x + padding, item_rect.y + padding))

        # Description
        desc_text = self.desc_font.render(
            item.description, True, UI.SHOP_ITEM_DESC_COLOR
        )
        screen.blit(desc_text, (item_rect.x + padding, item_rect.y + padding + 22))

        # Stats
        stats_text = ""
        if item.attack_bonus > 0:
            stats_text += f"+{item.attack_bonus} ATK  "
        if item.defense_bonus > 0:
            stats_text += f"+{item.defense_bonus} DEF  "

        if stats_text:
            stats_render = self.small_font.render(stats_text, True, UI.SHOP_STAT_COLOR)
            screen.blit(
                stats_render, (item_rect.x + padding, item_rect.y + padding + 42)
            )

        # Price
        price_color = (
            config.GOLD
            if player_gold >= item.gold_value
            else config.SHOP_INSUFFICIENT_FUNDS_COLOR
        )
        price_text = self.font.render(f"{item.gold_value} gold", True, price_color)
        price_x = item_rect.x + item_rect.width - price_text.get_width() - padding
        screen.blit(price_text, (price_x, item_rect.y + padding))

        # Quantity
        if shop_item:
            if shop_item.infinite:
                qty_text = self.small_font.render("∞", True, UI.SHOP_QUANTITY_COLOR)
            else:
                qty_text = self.small_font.render(
                    f"x{shop_item.quantity}", True, UI.SHOP_QUANTITY_COLOR
                )
            qty_x = item_rect.x + item_rect.width - qty_text.get_width() - padding
            screen.blit(qty_text, (qty_x, item_rect.y + padding + 25))

    def _draw_item_info_sell(
        self, screen: pygame.Surface, item_rect: pygame.Rect, item
    ):
        """Draw item information for selling."""
        padding = UI.SHOP_ITEM_PADDING

        # Item name
        name_text = self.font.render(item.name, True, config.SHOP_TEXT_COLOR)
        screen.blit(name_text, (item_rect.x + padding, item_rect.y + padding))

        # Description
        desc_text = self.desc_font.render(
            item.description, True, UI.SHOP_ITEM_DESC_COLOR
        )
        screen.blit(desc_text, (item_rect.x + padding, item_rect.y + padding + 22))

        # Stats
        stats_text = ""
        if item.attack_bonus > 0:
            stats_text += f"+{item.attack_bonus} ATK  "
        if item.defense_bonus > 0:
            stats_text += f"+{item.defense_bonus} DEF  "

        if stats_text:
            stats_render = self.small_font.render(stats_text, True, UI.SHOP_STAT_COLOR)
            screen.blit(
                stats_render, (item_rect.x + padding, item_rect.y + padding + 42)
            )

        # Sell price or unsellable
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
        state: ShopState,
    ):
        """Draw buy/sell button with hover effect."""
        button_x = panel_x + (self.panel_width - UI.SHOP_BUTTON_WIDTH) // 2
        button_rect = pygame.Rect(
            button_x, button_y, UI.SHOP_BUTTON_WIDTH, UI.SHOP_BUTTON_HEIGHT
        )
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouse_pos)

        # Store button rect for click detection
        if state.active_tab == "buy":
            state.buy_button_rect = button_rect
            button_text = "BUY ITEM"
        else:
            state.sell_button_rect = button_rect
            button_text = "SELL ITEM"

        # Determine if button is enabled
        is_enabled = state.selected_item_index is not None

        # Draw button using utility function
        Draw.draw_button(
            screen,
            button_rect,
            button_text,
            self.font,
            is_enabled=is_enabled,
            is_hovered=is_hovered,
        )

    def _draw_instructions(self, screen: pygame.Surface, panel_x: int, panel_y: int):
        """Draw control instructions."""
        instructions = "Press S or I to close shop"
        text = self.small_font.render(instructions, True, UI.SHOP_INSTRUCTION_COLOR)
        text_x = panel_x + self.padding
        text_y = panel_y + self.panel_height - 25
        screen.blit(text, (text_x, text_y))

    def _draw_message(
        self, screen: pygame.Surface, panel_x: int, panel_y: int, state: ShopState
    ):
        """Draw message at bottom of panel."""
        text_x = panel_x + self.panel_width // 2
        text_y = panel_y + self.panel_height - 100

        Draw.draw_message_box(
            screen,
            state.message,
            (text_x, text_y),
            self.font,
            text_color=state.message_color,
            bg_color=UI.SHOP_DIALOG_BG_COLOR,
            border_color=config.SHOP_BORDER_COLOR,
            centered=True,
        )

    def _draw_confirmation_dialog(
        self, screen: pygame.Surface, panel_x: int, panel_y: int, state: ShopState
    ):
        """Draw confirmation dialog."""
        dialog_x = panel_x + (self.panel_width - UI.SHOP_DIALOG_WIDTH) // 2
        dialog_y = panel_y + (self.panel_height - UI.SHOP_DIALOG_HEIGHT) // 2

        # Draw dialog background
        dialog_surface = pygame.Surface(
            (UI.SHOP_DIALOG_WIDTH, UI.SHOP_DIALOG_HEIGHT), pygame.SRCALPHA
        )
        dialog_surface.fill((*UI.SHOP_DIALOG_BG_COLOR, UI.SHOP_DIALOG_BG_ALPHA))
        screen.blit(dialog_surface, (dialog_x, dialog_y))
        pygame.draw.rect(
            screen,
            config.SHOP_BORDER_COLOR,
            (dialog_x, dialog_y, UI.SHOP_DIALOG_WIDTH, UI.SHOP_DIALOG_HEIGHT),
            UI.BORDER_WIDTH_THICK,
        )

        # Draw message
        message = state.confirmation_dialog["message"]
        message_lines = self._wrap_text(message, UI.SHOP_DIALOG_WIDTH - 40)
        for i, line in enumerate(message_lines):
            text = self.font.render(line, True, config.WHITE)
            text_x = dialog_x + (UI.SHOP_DIALOG_WIDTH - text.get_width()) // 2
            text_y = dialog_y + 20 + i * 25
            screen.blit(text, (text_x, text_y))

        # Draw buttons
        button_y = (
            dialog_y
            + UI.SHOP_DIALOG_HEIGHT
            - UI.SHOP_DIALOG_BUTTON_HEIGHT
            - UI.SHOP_DIALOG_BUTTON_MARGIN
        )

        # Yes button
        yes_button_x = (
            dialog_x
            + UI.SHOP_DIALOG_WIDTH // 2
            - UI.SHOP_DIALOG_BUTTON_WIDTH
            - UI.SHOP_DIALOG_BUTTON_SPACING
        )
        yes_button_rect = pygame.Rect(
            yes_button_x,
            button_y,
            UI.SHOP_DIALOG_BUTTON_WIDTH,
            UI.SHOP_DIALOG_BUTTON_HEIGHT,
        )
        mouse_pos = pygame.mouse.get_pos()
        yes_hovered = yes_button_rect.collidepoint(mouse_pos)

        Draw.draw_button(
            screen,
            yes_button_rect,
            "Yes",
            self.font,
            is_enabled=True,
            is_hovered=yes_hovered,
        )

        # No button
        no_button_x = (
            dialog_x + UI.SHOP_DIALOG_WIDTH // 2 + UI.SHOP_DIALOG_BUTTON_SPACING
        )
        no_button_rect = pygame.Rect(
            no_button_x,
            button_y,
            UI.SHOP_DIALOG_BUTTON_WIDTH,
            UI.SHOP_DIALOG_BUTTON_HEIGHT,
        )
        no_hovered = no_button_rect.collidepoint(mouse_pos)

        Draw.draw_button(
            screen,
            no_button_rect,
            "No",
            self.font,
            is_enabled=True,
            is_hovered=no_hovered,
            bg_color=UI.SHOP_NO_BUTTON_COLOR,
            hover_color=UI.SHOP_NO_BUTTON_HOVER,
        )

        # Store button rects for click detection
        state.confirmation_dialog["yes_rect"] = yes_button_rect
        state.confirmation_dialog["no_rect"] = no_button_rect

    def _draw_scrollbar(
        self,
        screen: pygame.Surface,
        panel_x: int,
        list_y: int,
        list_height: int,
        num_items: int,
        item_height: int,
        state: ShopState,
    ):
        """Draw scrollbar indicator if content is scrollable."""
        # Calculate if scrollbar is needed
        total_content_height = num_items * (item_height + 5)
        if total_content_height <= list_height:
            return  # No scrollbar needed

        # Scrollbar dimensions
        scrollbar_x = (
            panel_x
            + self.panel_width
            - self.padding
            - UI.SHOP_SCROLLBAR_WIDTH
            - UI.SHOP_SCROLLBAR_MARGIN
        )
        scrollbar_track_rect = pygame.Rect(
            scrollbar_x,
            list_y + UI.SHOP_SCROLLBAR_MARGIN,
            UI.SHOP_SCROLLBAR_WIDTH,
            list_height - 2 * UI.SHOP_SCROLLBAR_MARGIN,
        )

        # Draw scrollbar using utility function
        Draw.draw_scrollbar(
            screen,
            scrollbar_track_rect,
            state.scroll_offset,
            total_content_height,
            list_height,
        )

        # Draw scroll hint text if at top
        if state.scroll_offset == 0 and num_items > 4:
            hint_text = self.small_font.render(
                "Scroll ↓", True, UI.SHOP_SCROLL_HINT_COLOR
            )
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
