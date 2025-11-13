"""Tests for Portal class."""

import pytest
import pygame
from caislean_gaofar.objects.portal import Portal
from caislean_gaofar.core import config


class TestPortal:
    """Test cases for the Portal class."""

    @pytest.fixture
    def screen(self):
        """Create a test screen surface."""
        pygame.init()
        return pygame.display.set_mode((800, 600))

    def test_portal_initialization(self):
        """Test portal initializes with correct attributes."""
        portal = Portal(5, 10, False)

        assert portal.grid_x == 5
        assert portal.grid_y == 10
        assert portal.is_return_portal is False
        assert portal.animation_time == 0.0
        assert portal.x == 5 * config.TILE_SIZE
        assert portal.y == 10 * config.TILE_SIZE
        assert portal.size == config.TILE_SIZE

    def test_portal_initialization_return_portal(self):
        """Test return portal initializes with is_return_portal=True."""
        portal = Portal(3, 7, True)

        assert portal.grid_x == 3
        assert portal.grid_y == 7
        assert portal.is_return_portal is True

    def test_portal_update(self):
        """Test portal animation time updates."""
        portal = Portal(0, 0, False)
        initial_time = portal.animation_time

        portal.update(0.5)

        assert portal.animation_time == initial_time + 0.5

    def test_portal_update_multiple_times(self):
        """Test portal animation time accumulates."""
        portal = Portal(0, 0, False)

        portal.update(0.1)
        portal.update(0.2)
        portal.update(0.3)

        assert portal.animation_time == pytest.approx(0.6)

    def test_portal_screen_coordinates_with_camera_offset(self, screen):
        """Test portal calculates screen coordinates correctly with camera offset."""
        portal = Portal(10, 15, False)

        # Test without camera offset
        assert portal.get_screen_x(0) == 10 * config.TILE_SIZE
        assert portal.get_screen_y(0) == 15 * config.TILE_SIZE

        # Test with camera offset
        assert portal.get_screen_x(3) == 7 * config.TILE_SIZE
        assert portal.get_screen_y(5) == 10 * config.TILE_SIZE

        # Verify draw doesn't mutate position
        portal.draw(screen, 3, 5)
        assert portal.x == 10 * config.TILE_SIZE  # Should remain unchanged
        assert portal.y == 15 * config.TILE_SIZE  # Should remain unchanged

    def test_portal_draw_town_portal(self, screen):
        """Test drawing a town portal (not return)."""
        portal = Portal(1, 1, False)

        # Should not raise any exceptions
        portal.draw(screen)

    def test_portal_draw_return_portal(self, screen):
        """Test drawing a return portal."""
        portal = Portal(1, 1, True)

        # Should not raise any exceptions
        portal.draw(screen)

    def test_portal_draw_with_animation(self, screen):
        """Test drawing portal with animation progress."""
        portal = Portal(1, 1, False)

        # Advance animation
        portal.update(1.0)

        # Should not raise any exceptions
        portal.draw(screen)

    def test_portal_x_y_calculation(self):
        """Test x and y are calculated correctly from grid coordinates."""
        grid_x, grid_y = 7, 4
        portal = Portal(grid_x, grid_y, False)

        expected_x = grid_x * config.TILE_SIZE
        expected_y = grid_y * config.TILE_SIZE

        assert portal.x == expected_x
        assert portal.y == expected_y
