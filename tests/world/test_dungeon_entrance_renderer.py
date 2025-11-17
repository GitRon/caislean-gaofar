"""Tests for DungeonEntranceRenderer."""

import pygame
from unittest.mock import Mock, patch
from caislean_gaofar.world.dungeon_entrance_renderer import DungeonEntranceRenderer


class TestDungeonEntranceRenderer:
    """Test suite for DungeonEntranceRenderer."""

    def test_draw_entrance_cave(self):
        """Test drawing a cave entrance."""
        screen = Mock()
        renderer = DungeonEntranceRenderer()

        with (
            patch("pygame.draw.ellipse") as mock_ellipse,
            patch("pygame.draw.circle") as mock_circle,
        ):
            renderer.draw_entrance(screen, "C", 100, 200, 50)

            # Should draw background circles, arch, inner cave, and rocky edges
            assert mock_circle.call_count >= 6
            assert mock_ellipse.call_count >= 2

    def test_draw_entrance_castle(self):
        """Test drawing a castle entrance."""
        screen = Mock()
        renderer = DungeonEntranceRenderer()

        with (
            patch("pygame.draw.rect") as mock_rect,
            patch("pygame.draw.circle") as mock_circle,
            patch("pygame.draw.line") as mock_line,
        ):
            renderer.draw_entrance(screen, "K", 100, 200, 50)

            # Should draw background circles, gate structure, battlements, and stone patterns
            assert mock_circle.call_count >= 2
            assert mock_rect.call_count >= 4
            assert mock_line.call_count >= 3

    def test_draw_entrance_generic_dungeon(self):
        """Test drawing a generic dungeon entrance."""
        screen = Mock()
        renderer = DungeonEntranceRenderer()

        with patch("pygame.draw.circle") as mock_circle:
            renderer.draw_entrance(screen, "D", 100, 200, 50)

            # Should draw background circles (2), outer glow, portal, and center = 5 total
            assert mock_circle.call_count >= 5

    def test_draw_entrance_unknown_type(self):
        """Test drawing an unknown entrance type does nothing."""
        screen = Mock()
        renderer = DungeonEntranceRenderer()

        with (
            patch("pygame.draw.circle") as mock_circle,
            patch("pygame.draw.rect") as mock_rect,
            patch("pygame.draw.ellipse") as mock_ellipse,
        ):
            renderer.draw_entrance(screen, "X", 100, 200, 50)

            # Should not draw anything for unknown type
            mock_circle.assert_not_called()
            mock_rect.assert_not_called()
            mock_ellipse.assert_not_called()

    def test_draw_entrance_name(self):
        """Test drawing dungeon entrance name."""
        screen = Mock()
        renderer = DungeonEntranceRenderer()

        with (
            patch("pygame.font.Font") as mock_font_class,
            patch("pygame.draw.rect") as mock_rect,
        ):
            mock_font = Mock()
            mock_font.render.return_value = Mock(
                get_rect=Mock(return_value=pygame.Rect(0, 0, 100, 20)),
                get_width=Mock(return_value=100),
                get_height=Mock(return_value=20),
            )
            mock_font_class.return_value = mock_font

            renderer.draw_entrance_name(screen, "Dark Cave", 100, 200, 50)

            # Should render the name text
            mock_font.render.assert_called_once()
            # Should draw the message box background and border
            assert mock_rect.call_count >= 2

    def test_draw_cave_entrance_details(self):
        """Test cave entrance drawing details."""
        screen = Mock()
        renderer = DungeonEntranceRenderer()

        with (
            patch("pygame.draw.ellipse") as mock_ellipse,
            patch("pygame.draw.circle") as mock_circle,
        ):
            renderer._draw_cave_entrance(screen, 100, 200, 50)

            # Verify ellipse calls for arch and inner cave
            assert mock_ellipse.call_count >= 2
            # Verify circle calls for background and rocky edges
            assert mock_circle.call_count >= 6

    def test_draw_castle_entrance_details(self):
        """Test castle entrance drawing details."""
        screen = Mock()
        renderer = DungeonEntranceRenderer()

        with (
            patch("pygame.draw.rect") as mock_rect,
            patch("pygame.draw.circle") as mock_circle,
            patch("pygame.draw.line") as mock_line,
        ):
            renderer._draw_castle_entrance(screen, 100, 200, 50)

            # Verify background circles
            assert mock_circle.call_count >= 2
            # Verify gate structure and battlements
            assert mock_rect.call_count >= 4
            # Verify stone block pattern
            assert mock_line.call_count >= 3

    def test_draw_dungeon_entrance_details(self):
        """Test generic dungeon entrance drawing details."""
        screen = Mock()
        renderer = DungeonEntranceRenderer()

        with patch("pygame.draw.circle") as mock_circle:
            renderer._draw_dungeon_entrance(screen, 100, 200, 50)

            # Verify background circles (2), glow, portal, and center = 5 total
            assert mock_circle.call_count >= 5
