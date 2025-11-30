"""Tests for Library class."""

import pytest
import pygame
from caislean_gaofar.objects.library import Library


class TestLibrary:
    """Test cases for Library class."""

    @pytest.fixture
    def library(self):
        """Create a library instance for testing."""
        return Library(grid_x=2, grid_y=6)

    def test_initialization(self, library):
        """Test library initializes with correct properties."""
        assert library.grid_x == 2
        assert library.grid_y == 6
        assert library.animation_time == 0.0
        assert library.x == 2 * 50  # TILE_SIZE = 50
        assert library.y == 6 * 50
        assert library.size == 50
        assert library.portal_gift_active is False
        assert library.portal_effect_time == 0.0

    def test_update(self, library):
        """Test library animation update."""
        initial_time = library.animation_time

        library.update(0.1)  # 100ms

        assert library.animation_time > initial_time
        assert library.animation_time == pytest.approx(0.1)

    def test_update_portal_gift_effect(self, library):
        """Test portal gift effect timer decreases."""
        library.portal_gift_active = True
        library.portal_effect_time = 1.5

        library.update(0.5)

        assert library.portal_effect_time == pytest.approx(1.0)
        assert library.portal_gift_active is True  # Still active

        library.update(1.0)

        assert library.portal_effect_time <= 0.0
        assert library.portal_gift_active is False  # Deactivated

    def test_activate_portal_gift(self, library):
        """Test activating portal gift effect."""
        library.activate_portal_gift()

        assert library.portal_gift_active is True
        assert library.portal_effect_time == 1.5

    def test_get_screen_x(self, library):
        """Test getting screen x coordinate."""
        # No camera offset
        screen_x = library.get_screen_x()
        assert screen_x == 2 * 50

        # With camera offset
        screen_x = library.get_screen_x(camera_offset_x=1)
        assert screen_x == (2 - 1) * 50

    def test_get_screen_y(self, library):
        """Test getting screen y coordinate."""
        # No camera offset
        screen_y = library.get_screen_y()
        assert screen_y == 6 * 50

        # With camera offset
        screen_y = library.get_screen_y(camera_offset_y=2)
        assert screen_y == (6 - 2) * 50

    def test_draw(self, library):
        """Test library drawing (basic smoke test)."""
        # Initialize pygame for drawing
        pygame.init()
        screen = pygame.display.set_mode((800, 600))

        # Should not raise an exception
        library.draw(screen, camera_offset_x=0, camera_offset_y=0)

        pygame.quit()

    def test_draw_with_portal_gift_effect(self, library):
        """Test library drawing with portal gift effect active."""
        pygame.init()
        screen = pygame.display.set_mode((800, 600))

        library.activate_portal_gift()

        # Should not raise an exception
        library.draw(screen, camera_offset_x=0, camera_offset_y=0)

        pygame.quit()

    def test_portal_gift_effect_animation(self, library):
        """Test portal gift effect animates over time."""
        library.activate_portal_gift()
        initial_time = library.portal_effect_time

        library.update(0.1)

        assert library.portal_effect_time < initial_time
        assert library.portal_gift_active is True

        # Advance time to complete effect
        library.update(2.0)

        assert library.portal_gift_active is False

    def test_multiple_portal_gift_activations(self, library):
        """Test that portal gift can be activated multiple times."""
        library.activate_portal_gift()
        library.update(2.0)  # Complete first effect
        assert library.portal_gift_active is False

        library.activate_portal_gift()
        assert library.portal_gift_active is True
        assert library.portal_effect_time == 1.5
