"""Shared UI drawing utilities for common rendering patterns.

This module provides reusable drawing functions to eliminate code duplication
across renderer classes.
"""

import pygame
from caislean_gaofar.ui.ui_constants import UIConstants


class UIDrawingUtils:
    """Utility class for common UI rendering operations."""

    @staticmethod
    def draw_ornate_border(surface: pygame.Surface, rect: pygame.Rect):
        """
        Draw an ornate medieval-style border around a rectangle.

        Args:
            surface: Surface to draw on
            rect: Rectangle to draw border around
        """
        # Draw outer border (darker)
        pygame.draw.rect(
            surface, UIConstants.WOOD_BORDER, rect, UIConstants.BORDER_WIDTH_THICK
        )

        # Draw inner ornate line (golden)
        inner_rect = rect.inflate(
            -UIConstants.ORNATE_BORDER_OFFSET, -UIConstants.ORNATE_BORDER_OFFSET
        )
        pygame.draw.rect(
            surface,
            UIConstants.ORNATE_GOLD,
            inner_rect,
            UIConstants.BORDER_WIDTH_MINIMAL,
        )

        # Draw corner decorations (small circles)
        corners = [
            (rect.left + 5, rect.top + 5),
            (rect.right - 5, rect.top + 5),
            (rect.left + 5, rect.bottom - 5),
            (rect.right - 5, rect.bottom - 5),
        ]
        for corner in corners:
            pygame.draw.circle(
                surface, UIConstants.ORNATE_GOLD, corner, UIConstants.ORNATE_CORNER_RADIUS
            )

    @staticmethod
    def draw_shadowed_text(
        surface: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        position: tuple,
        color: tuple,
        shadow_color: tuple = (0, 0, 0),
        shadow_offset: int = None,
        centered: bool = False,
    ):
        """
        Draw text with a drop shadow for better readability.

        Args:
            surface: Surface to draw on
            font: Font to use
            text: Text to render
            position: (x, y) position for the text
            color: Color of the main text
            shadow_color: Color of the shadow (default: black)
            shadow_offset: Offset for shadow (default: from UIConstants)
            centered: Whether to center the text at the position
        """
        if shadow_offset is None:
            shadow_offset = UIConstants.TEXT_SHADOW_OFFSET

        # Render text surfaces
        text_surface = font.render(text, True, color)
        shadow_surface = font.render(text, True, shadow_color)

        if centered:
            # Calculate centered position
            text_rect = text_surface.get_rect(center=position)
            shadow_rect = shadow_surface.get_rect(
                center=(position[0] + shadow_offset, position[1] + shadow_offset)
            )
            surface.blit(shadow_surface, shadow_rect)
            surface.blit(text_surface, text_rect)
        else:
            # Draw shadow
            shadow_pos = (position[0] + shadow_offset, position[1] + shadow_offset)
            surface.blit(shadow_surface, shadow_pos)
            # Draw main text
            surface.blit(text_surface, position)

        if centered:
            return text_surface.get_rect(center=position)
        else:
            return text_surface.get_rect(topleft=position)

    @staticmethod
    def draw_panel(
        surface: pygame.Surface,
        rect: pygame.Rect,
        bg_color: tuple = None,
        border_color: tuple = None,
        ornate: bool = True,
    ):
        """
        Draw a standard UI panel with background and border.

        Args:
            surface: Surface to draw on
            rect: Rectangle defining the panel area
            bg_color: Background color (default: wood color)
            border_color: Border color (used if ornate=False)
            ornate: Whether to use ornate border style
        """
        if bg_color is None:
            bg_color = UIConstants.WOOD_COLOR

        # Draw panel background
        pygame.draw.rect(surface, bg_color, rect)

        # Draw border
        if ornate:
            UIDrawingUtils.draw_ornate_border(surface, rect)
        elif border_color:
            pygame.draw.rect(
                surface, border_color, rect, UIConstants.BORDER_WIDTH_THIN
            )

    @staticmethod
    def draw_progress_bar(
        surface: pygame.Surface,
        rect: pygame.Rect,
        progress: float,
        bar_color: tuple,
        bg_color: tuple = None,
        border_color: tuple = None,
        border_width: int = None,
    ):
        """
        Draw a progress bar.

        Args:
            surface: Surface to draw on
            rect: Rectangle defining the bar area
            progress: Progress value (0.0 to 1.0)
            bar_color: Color of the filled portion
            bg_color: Background color (default: wood border)
            border_color: Border color (default: ornate gold)
            border_width: Width of border (default: 2)
        """
        if bg_color is None:
            bg_color = UIConstants.WOOD_BORDER
        if border_color is None:
            border_color = UIConstants.ORNATE_GOLD
        if border_width is None:
            border_width = UIConstants.BORDER_WIDTH_THIN

        # Draw background
        pygame.draw.rect(surface, bg_color, rect)

        # Draw filled portion
        if progress > 0:
            fill_width = int(rect.width * progress)
            fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
            pygame.draw.rect(surface, bar_color, fill_rect)

        # Draw border
        pygame.draw.rect(surface, border_color, rect, border_width)

    @staticmethod
    def draw_scrollbar(
        surface: pygame.Surface,
        track_rect: pygame.Rect,
        scroll_offset: int,
        total_content_height: int,
        visible_height: int,
    ):
        """
        Draw a scrollbar with track and thumb.

        Args:
            surface: Surface to draw on
            track_rect: Rectangle defining the scrollbar track
            scroll_offset: Current scroll offset
            total_content_height: Total height of scrollable content
            visible_height: Height of visible area
        """
        # Draw track
        pygame.draw.rect(
            surface,
            UIConstants.SHOP_SCROLLBAR_TRACK_COLOR,
            track_rect,
            border_radius=6,
        )

        # Calculate thumb size and position
        visible_ratio = visible_height / total_content_height
        thumb_height = max(
            UIConstants.SHOP_SCROLLBAR_MIN_THUMB, int(track_rect.height * visible_ratio)
        )

        max_scroll = total_content_height - visible_height
        scroll_ratio = scroll_offset / max_scroll if max_scroll > 0 else 0
        thumb_y = track_rect.y + scroll_ratio * (track_rect.height - thumb_height)

        thumb_rect = pygame.Rect(track_rect.x, thumb_y, track_rect.width, thumb_height)

        # Draw thumb
        pygame.draw.rect(
            surface, UIConstants.SHOP_SCROLLBAR_THUMB_COLOR, thumb_rect, border_radius=6
        )
        pygame.draw.rect(
            surface,
            UIConstants.WOOD_BORDER,
            thumb_rect,
            UIConstants.BORDER_WIDTH_MINIMAL,
            border_radius=6,
        )

    @staticmethod
    def draw_button(
        surface: pygame.Surface,
        rect: pygame.Rect,
        text: str,
        font: pygame.font.Font,
        is_enabled: bool = True,
        is_hovered: bool = False,
        bg_color: tuple = None,
        hover_color: tuple = None,
        disabled_bg_color: tuple = None,
        text_color: tuple = None,
        disabled_text_color: tuple = None,
        border_color: tuple = None,
    ):
        """
        Draw a button with text.

        Args:
            surface: Surface to draw on
            rect: Rectangle defining the button area
            text: Button text
            font: Font for the text
            is_enabled: Whether button is enabled
            is_hovered: Whether button is hovered
            bg_color: Background color when enabled
            hover_color: Background color when hovered
            disabled_bg_color: Background color when disabled
            text_color: Text color when enabled
            disabled_text_color: Text color when disabled
            border_color: Border color
        """
        # Set default colors if not provided
        from caislean_gaofar.core import config

        if bg_color is None:
            bg_color = config.SHOP_BUTTON_COLOR
        if hover_color is None:
            hover_color = config.SHOP_BUTTON_HOVER_COLOR
        if disabled_bg_color is None:
            disabled_bg_color = UIConstants.SHOP_BUTTON_DISABLED_BG
        if text_color is None:
            text_color = config.WHITE
        if disabled_text_color is None:
            disabled_text_color = UIConstants.SHOP_BUTTON_DISABLED_TEXT
        if border_color is None:
            border_color = config.SHOP_BORDER_COLOR

        # Determine colors based on state
        if not is_enabled:
            button_color = disabled_bg_color
            current_text_color = disabled_text_color
        elif is_hovered:
            button_color = hover_color
            current_text_color = text_color
        else:
            button_color = bg_color
            current_text_color = text_color

        # Draw button background
        pygame.draw.rect(surface, button_color, rect)
        pygame.draw.rect(
            surface, border_color, rect, UIConstants.BORDER_WIDTH_THIN
        )

        # Draw button text (centered)
        text_surface = font.render(text, True, current_text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    @staticmethod
    def draw_icon_circle(
        surface: pygame.Surface,
        center: tuple,
        radius: int,
        inner_color: tuple,
        outer_color: tuple = None,
        inner_radius_offset: int = 3,
    ):
        """
        Draw a circular icon with inner and outer circles.

        Args:
            surface: Surface to draw on
            center: (x, y) center position
            radius: Outer radius
            inner_color: Color of inner circle
            outer_color: Color of outer circle (default: same as inner)
            inner_radius_offset: How much smaller the inner circle is
        """
        if outer_color is None:
            outer_color = inner_color

        # Draw outer circle
        pygame.draw.circle(surface, outer_color, center, radius)

        # Draw inner circle
        if inner_radius_offset > 0:
            pygame.draw.circle(surface, inner_color, center, radius - inner_radius_offset)

    @staticmethod
    def draw_message_box(
        surface: pygame.Surface,
        text: str,
        position: tuple,
        font: pygame.font.Font,
        text_color: tuple = None,
        bg_color: tuple = None,
        border_color: tuple = None,
        padding: int = None,
        centered: bool = True,
    ):
        """
        Draw a message box with text and background.

        Args:
            surface: Surface to draw on
            text: Message text
            position: (x, y) position for the message
            font: Font to use
            text_color: Text color
            bg_color: Background color
            border_color: Border color
            padding: Padding around text
            centered: Whether to center at position
        """
        from caislean_gaofar.core import config

        if text_color is None:
            text_color = config.WHITE
        if bg_color is None:
            bg_color = config.BLACK
        if border_color is None:
            border_color = config.SHOP_BORDER_COLOR
        if padding is None:
            padding = UIConstants.TEXT_PADDING

        # Render text
        text_surface = font.render(text, True, text_color)

        if centered:
            text_rect = text_surface.get_rect(center=position)
        else:
            text_rect = text_surface.get_rect(topleft=position)

        # Draw background
        bg_rect = text_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(surface, bg_color, bg_rect)
        pygame.draw.rect(
            surface, border_color, bg_rect, UIConstants.BORDER_WIDTH_THIN
        )

        # Draw text
        surface.blit(text_surface, text_rect)

        return bg_rect

    @staticmethod
    def draw_entrance_background_circle(
        surface: pygame.Surface, center: tuple, radius: int, bg_color: tuple
    ):
        """
        Draw background circle for dungeon entrance icons.

        Args:
            surface: Surface to draw on
            center: (x, y) center position
            radius: Circle radius
            bg_color: Background color
        """
        # Draw dark outline
        pygame.draw.circle(
            surface,
            UIConstants.CAVE_BG_DARK,
            center,
            radius + UIConstants.ENTRANCE_ICON_CIRCLE_OFFSET,
        )
        # Draw main background
        pygame.draw.circle(surface, bg_color, center, radius)
