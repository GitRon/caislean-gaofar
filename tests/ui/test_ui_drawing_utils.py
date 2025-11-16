"""Tests for UI drawing utilities."""

import pygame
from unittest.mock import Mock, patch
from caislean_gaofar.ui.ui_drawing_utils import UIDrawingUtils as Draw
from caislean_gaofar.ui.ui_constants import UIConstants


class TestUIDrawingUtils:
    """Test suite for UIDrawingUtils."""

    def test_draw_ornate_border(self):
        """Test drawing ornate border."""
        surface = Mock()
        rect = pygame.Rect(10, 10, 100, 100)

        with patch("pygame.draw.rect") as mock_rect, patch(
            "pygame.draw.circle"
        ) as mock_circle:
            Draw.draw_ornate_border(surface, rect)

            # Should draw outer border, inner border, and 4 corner circles
            assert mock_rect.call_count >= 2
            assert mock_circle.call_count == 4

    def test_draw_shadowed_text_centered(self):
        """Test drawing shadowed text centered."""
        surface = Mock()
        font = Mock()
        font.render.return_value = Mock(get_rect=Mock(return_value=pygame.Rect(0, 0, 50, 20)))

        result = Draw.draw_shadowed_text(
            surface, font, "Test", (100, 100), (255, 255, 255), centered=True
        )

        # Should render both shadow and main text
        assert font.render.call_count == 2
        # Should return a rect
        assert isinstance(result, pygame.Rect)

    def test_draw_shadowed_text_not_centered(self):
        """Test drawing shadowed text not centered."""
        surface = Mock()
        font = Mock()
        font.render.return_value = Mock(get_rect=Mock(return_value=pygame.Rect(0, 0, 50, 20)))

        result = Draw.draw_shadowed_text(
            surface, font, "Test", (100, 100), (255, 255, 255), centered=False
        )

        # Should render both shadow and main text
        assert font.render.call_count == 2
        # Should return a rect with topleft
        assert isinstance(result, pygame.Rect)

    def test_draw_shadowed_text_custom_shadow_offset(self):
        """Test drawing shadowed text with custom shadow offset."""
        surface = Mock()
        font = Mock()
        font.render.return_value = Mock(get_rect=Mock(return_value=pygame.Rect(0, 0, 50, 20)))

        Draw.draw_shadowed_text(
            surface,
            font,
            "Test",
            (100, 100),
            (255, 255, 255),
            shadow_offset=5,
            centered=True,
        )

        assert font.render.call_count == 2

    def test_draw_panel_with_ornate_border(self):
        """Test drawing panel with ornate border."""
        surface = Mock()
        rect = pygame.Rect(10, 10, 100, 100)

        with patch("pygame.draw.rect") as mock_rect, patch(
            "pygame.draw.circle"
        ) as mock_circle:
            Draw.draw_panel(surface, rect, ornate=True)

            # Should draw background and ornate border components
            assert mock_rect.call_count >= 1
            # Should draw 4 corner circles
            assert mock_circle.call_count == 4

    def test_draw_panel_with_simple_border(self):
        """Test drawing panel with simple border."""
        surface = Mock()
        rect = pygame.Rect(10, 10, 100, 100)

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_panel(
                surface, rect, bg_color=(100, 100, 100), border_color=(50, 50, 50), ornate=False
            )

            # Should draw background and border
            assert mock_rect.call_count >= 2

    def test_draw_panel_no_border(self):
        """Test drawing panel without border when ornate=False and no border_color."""
        surface = Mock()
        rect = pygame.Rect(10, 10, 100, 100)

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_panel(surface, rect, ornate=False)

            # Should only draw background
            assert mock_rect.call_count >= 1

    def test_draw_progress_bar(self):
        """Test drawing progress bar."""
        surface = Mock()
        rect = pygame.Rect(10, 10, 200, 20)

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_progress_bar(surface, rect, 0.75, (0, 255, 0))

            # Should draw background, fill, and border
            assert mock_rect.call_count >= 3

    def test_draw_progress_bar_zero_progress(self):
        """Test drawing progress bar with zero progress."""
        surface = Mock()
        rect = pygame.Rect(10, 10, 200, 20)

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_progress_bar(surface, rect, 0.0, (0, 255, 0))

            # Should draw background and border only
            assert mock_rect.call_count >= 2

    def test_draw_progress_bar_custom_colors(self):
        """Test drawing progress bar with custom colors."""
        surface = Mock()
        rect = pygame.Rect(10, 10, 200, 20)

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_progress_bar(
                surface,
                rect,
                0.5,
                (255, 0, 0),
                bg_color=(50, 50, 50),
                border_color=(255, 255, 0),
                border_width=3,
            )

            assert mock_rect.call_count >= 3

    def test_draw_scrollbar(self):
        """Test drawing scrollbar."""
        surface = Mock()
        track_rect = pygame.Rect(10, 10, 12, 200)

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_scrollbar(surface, track_rect, 50, 500, 200)

            # Should draw track and thumb
            assert mock_rect.call_count >= 2

    def test_draw_scrollbar_at_max_scroll(self):
        """Test drawing scrollbar at maximum scroll."""
        surface = Mock()
        track_rect = pygame.Rect(10, 10, 12, 200)

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_scrollbar(surface, track_rect, 300, 500, 200)

            assert mock_rect.call_count >= 2

    def test_draw_scrollbar_no_scroll_needed(self):
        """Test drawing scrollbar when scroll_offset is 0 and max_scroll is 0."""
        surface = Mock()
        track_rect = pygame.Rect(10, 10, 12, 200)

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_scrollbar(surface, track_rect, 0, 200, 200)

            # Should still draw track and thumb
            assert mock_rect.call_count >= 2

    def test_draw_button_enabled_not_hovered(self):
        """Test drawing enabled button not hovered."""
        surface = Mock()
        rect = pygame.Rect(10, 10, 100, 40)
        font = Mock()
        font.render.return_value = Mock(get_rect=Mock(return_value=pygame.Rect(0, 0, 50, 20)))

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_button(surface, rect, "Click", font, is_enabled=True, is_hovered=False)

            # Should draw button background and border
            assert mock_rect.call_count >= 2

    def test_draw_button_enabled_hovered(self):
        """Test drawing enabled button hovered."""
        surface = Mock()
        rect = pygame.Rect(10, 10, 100, 40)
        font = Mock()
        font.render.return_value = Mock(get_rect=Mock(return_value=pygame.Rect(0, 0, 50, 20)))

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_button(surface, rect, "Click", font, is_enabled=True, is_hovered=True)

            assert mock_rect.call_count >= 2

    def test_draw_button_disabled(self):
        """Test drawing disabled button."""
        surface = Mock()
        rect = pygame.Rect(10, 10, 100, 40)
        font = Mock()
        font.render.return_value = Mock(get_rect=Mock(return_value=pygame.Rect(0, 0, 50, 20)))

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_button(surface, rect, "Click", font, is_enabled=False, is_hovered=False)

            assert mock_rect.call_count >= 2

    def test_draw_button_with_custom_colors(self):
        """Test drawing button with custom colors."""
        surface = Mock()
        rect = pygame.Rect(10, 10, 100, 40)
        font = Mock()
        font.render.return_value = Mock(get_rect=Mock(return_value=pygame.Rect(0, 0, 50, 20)))

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_button(
                surface,
                rect,
                "Click",
                font,
                is_enabled=True,
                is_hovered=False,
                bg_color=(100, 100, 100),
                hover_color=(150, 150, 150),
                disabled_bg_color=(50, 50, 50),
                text_color=(255, 255, 255),
                disabled_text_color=(100, 100, 100),
                border_color=(200, 200, 200),
            )

            assert mock_rect.call_count >= 2

    def test_draw_icon_circle(self):
        """Test drawing icon circle."""
        surface = Mock()

        with patch("pygame.draw.circle") as mock_circle:
            Draw.draw_icon_circle(surface, (100, 100), 20, (255, 0, 0))

            # Should draw outer and inner circles
            assert mock_circle.call_count >= 2

    def test_draw_icon_circle_with_different_outer_color(self):
        """Test drawing icon circle with different outer color."""
        surface = Mock()

        with patch("pygame.draw.circle") as mock_circle:
            Draw.draw_icon_circle(
                surface, (100, 100), 20, (255, 0, 0), outer_color=(0, 0, 255)
            )

            assert mock_circle.call_count >= 2

    def test_draw_icon_circle_no_inner_offset(self):
        """Test drawing icon circle with no inner radius offset."""
        surface = Mock()

        with patch("pygame.draw.circle") as mock_circle:
            Draw.draw_icon_circle(
                surface, (100, 100), 20, (255, 0, 0), inner_radius_offset=0
            )

            # Should only draw outer circle
            assert mock_circle.call_count == 1

    def test_draw_message_box_centered(self):
        """Test drawing message box centered."""
        surface = Mock()
        font = Mock()
        font.render.return_value = Mock(
            get_rect=Mock(return_value=pygame.Rect(0, 0, 100, 20)),
            get_width=Mock(return_value=100),
            get_height=Mock(return_value=20),
        )

        with patch("pygame.draw.rect") as mock_rect:
            result = Draw.draw_message_box(
                surface, "Test message", (200, 200), font, centered=True
            )

            # Should draw background and border
            assert mock_rect.call_count >= 2
            # Should return the background rect
            assert isinstance(result, pygame.Rect)

    def test_draw_message_box_not_centered(self):
        """Test drawing message box not centered."""
        surface = Mock()
        font = Mock()
        font.render.return_value = Mock(
            get_rect=Mock(return_value=pygame.Rect(0, 0, 100, 20)),
            get_width=Mock(return_value=100),
            get_height=Mock(return_value=20),
        )

        with patch("pygame.draw.rect") as mock_rect:
            result = Draw.draw_message_box(
                surface, "Test message", (200, 200), font, centered=False
            )

            assert mock_rect.call_count >= 2
            assert isinstance(result, pygame.Rect)

    def test_draw_message_box_custom_colors(self):
        """Test drawing message box with custom colors."""
        surface = Mock()
        font = Mock()
        font.render.return_value = Mock(
            get_rect=Mock(return_value=pygame.Rect(0, 0, 100, 20)),
            get_width=Mock(return_value=100),
            get_height=Mock(return_value=20),
        )

        with patch("pygame.draw.rect") as mock_rect:
            Draw.draw_message_box(
                surface,
                "Test",
                (200, 200),
                font,
                text_color=(255, 255, 0),
                bg_color=(50, 50, 50),
                border_color=(100, 100, 100),
                padding=15,
                centered=True,
            )

            assert mock_rect.call_count >= 2

    def test_draw_entrance_background_circle(self):
        """Test drawing entrance background circle."""
        surface = Mock()

        with patch("pygame.draw.circle") as mock_circle:
            Draw.draw_entrance_background_circle(surface, (100, 100), 25, (200, 180, 140))

            # Should draw dark outline and main background
            assert mock_circle.call_count == 2
