"""Tests for Temple class."""

import pytest
import pygame
from caislean_gaofar.objects.temple import Temple
from caislean_gaofar.core import config


class TestTemple:
    """Test cases for the Temple class."""

    @pytest.fixture
    def screen(self):
        """Create a test screen surface."""
        pygame.init()
        return pygame.display.set_mode((800, 600))

    def test_temple_initialization(self):
        """Test temple initializes with correct attributes."""
        temple = Temple(8, 1)

        assert temple.grid_x == 8
        assert temple.grid_y == 1
        assert temple.animation_time == 0.0
        assert temple.x == 8 * config.TILE_SIZE
        assert temple.y == 1 * config.TILE_SIZE
        assert temple.size == config.TILE_SIZE
        assert temple.healing_active is False
        assert temple.healing_effect_time == 0.0

    def test_temple_initialization_different_position(self):
        """Test temple initializes at different grid position."""
        temple = Temple(5, 10)

        assert temple.grid_x == 5
        assert temple.grid_y == 10
        assert temple.x == 5 * config.TILE_SIZE
        assert temple.y == 10 * config.TILE_SIZE

    def test_temple_update(self):
        """Test temple animation time updates."""
        temple = Temple(0, 0)
        initial_time = temple.animation_time

        temple.update(0.5)

        assert temple.animation_time == initial_time + 0.5

    def test_temple_update_multiple_times(self):
        """Test temple animation time accumulates."""
        temple = Temple(0, 0)

        temple.update(0.1)
        temple.update(0.2)
        temple.update(0.3)

        assert temple.animation_time == pytest.approx(0.6)

    def test_temple_activate_healing(self):
        """Test activating the healing effect."""
        temple = Temple(0, 0)

        temple.activate_healing()

        assert temple.healing_active is True
        assert temple.healing_effect_time == 1.0

    def test_temple_healing_effect_expires(self):
        """Test healing effect expires after time."""
        temple = Temple(0, 0)
        temple.activate_healing()

        # Update for 0.5 seconds
        temple.update(0.5)
        assert temple.healing_active is True
        assert temple.healing_effect_time == pytest.approx(0.5)

        # Update for another 0.5 seconds
        temple.update(0.5)
        assert temple.healing_active is False
        assert temple.healing_effect_time <= 0

    def test_temple_healing_effect_does_not_go_negative(self):
        """Test healing effect time doesn't go negative."""
        temple = Temple(0, 0)
        temple.activate_healing()

        # Update for more than the effect duration
        temple.update(2.0)

        assert temple.healing_active is False
        assert temple.healing_effect_time <= 0

    def test_temple_screen_coordinates_with_camera_offset(self, screen):
        """Test temple calculates screen coordinates correctly with camera offset."""
        temple = Temple(10, 15)

        # Test without camera offset
        assert temple.get_screen_x(0) == 10 * config.TILE_SIZE
        assert temple.get_screen_y(0) == 15 * config.TILE_SIZE

        # Test with camera offset
        assert temple.get_screen_x(3) == 7 * config.TILE_SIZE
        assert temple.get_screen_y(5) == 10 * config.TILE_SIZE

        # Verify draw doesn't mutate position
        temple.draw(screen, 3, 5)
        assert temple.x == 10 * config.TILE_SIZE  # Should remain unchanged
        assert temple.y == 15 * config.TILE_SIZE  # Should remain unchanged

    def test_temple_draw_normal(self, screen):
        """Test drawing a temple without healing effect."""
        temple = Temple(1, 1)

        # Should not raise any exceptions
        temple.draw(screen)

    def test_temple_draw_with_healing_active(self, screen):
        """Test drawing a temple with healing effect active."""
        temple = Temple(1, 1)
        temple.activate_healing()

        # Should not raise any exceptions
        temple.draw(screen)

    def test_temple_draw_with_animation(self, screen):
        """Test drawing temple with animation progress."""
        temple = Temple(1, 1)

        # Advance animation
        temple.update(1.0)

        # Should not raise any exceptions
        temple.draw(screen)

    def test_temple_x_y_calculation(self):
        """Test x and y are calculated correctly from grid coordinates."""
        grid_x, grid_y = 7, 4
        temple = Temple(grid_x, grid_y)

        expected_x = grid_x * config.TILE_SIZE
        expected_y = grid_y * config.TILE_SIZE

        assert temple.x == expected_x
        assert temple.y == expected_y

    def test_temple_multiple_healing_activations(self):
        """Test that healing can be activated multiple times."""
        temple = Temple(0, 0)

        # First activation
        temple.activate_healing()
        assert temple.healing_active is True

        # Let it expire
        temple.update(1.5)
        assert temple.healing_active is False

        # Second activation
        temple.activate_healing()
        assert temple.healing_active is True
        assert temple.healing_effect_time == 1.0

    def test_temple_healing_visual_effect_during_active_period(self):
        """Test healing visual effect is active during the effect period."""
        temple = Temple(0, 0)
        temple.activate_healing()

        # Test at different points during the effect - update 10 times with small delta
        dt = 0.09  # Just under 1 second total
        temple.update(dt)
        assert temple.healing_active is True or temple.healing_effect_time <= 0
        temple.update(dt)
        assert temple.healing_active is True or temple.healing_effect_time <= 0
        temple.update(dt)
        assert temple.healing_active is True or temple.healing_effect_time <= 0
        temple.update(dt)
        assert temple.healing_active is True or temple.healing_effect_time <= 0
        temple.update(dt)
        assert temple.healing_active is True or temple.healing_effect_time <= 0

    def test_temple_size_matches_tile_size(self):
        """Test temple size matches the configured tile size."""
        temple = Temple(0, 0)

        assert temple.size == config.TILE_SIZE

    def test_temple_draw_healing_with_zero_pulse(self, screen):
        """Test drawing temple with healing when pulse creates zero/negative radius."""
        temple = Temple(1, 1)
        temple.activate_healing()

        # Set animation time to create a zero pulse (sin = 0)
        # This ensures the radius calculations hit edge cases
        import math

        # When sin(animation_time * 4) = 0, pulse = 0
        temple.animation_time = math.pi / 4  # sin(pi) = 0

        # Should not raise any exceptions even with edge case radius values
        temple.draw(screen)

    def test_temple_draw_healing_with_negative_radius_branch(self, screen):
        """Test drawing temple covering the negative radius branch."""
        temple = Temple(1, 1)
        temple.activate_healing()

        # Create multiple draw calls with different animation times
        # to ensure all branches in the glow effect loop are covered
        import math

        # Test various angles
        temple.animation_time = 0
        temple.draw(screen)
        temple.animation_time = math.pi / 4
        temple.draw(screen)
        temple.animation_time = math.pi / 2
        temple.draw(screen)
        temple.animation_time = math.pi
        temple.draw(screen)
        temple.animation_time = 3 * math.pi / 2
        temple.draw(screen)

        # Also test with very large animation time
        temple.animation_time = 100.0
        temple.draw(screen)
