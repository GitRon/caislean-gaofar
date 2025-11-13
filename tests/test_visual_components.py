"""Tests for visual_components module."""

import pygame
import pytest
import visual_components


class TestVisualComponents:
    """Test visual component helper functions."""

    @pytest.fixture(autouse=True)
    def setup_pygame(self):
        """Initialize pygame before each test."""
        pygame.init()
        pygame.display.set_mode((800, 600))
        yield
        pygame.quit()

    def test_apply_floating_effect_default_params(self):
        """Test apply_floating_effect with default parameters"""
        # Arrange
        y = 100
        frame_count = 0

        # Act
        result = visual_components.apply_floating_effect(y, frame_count)

        # Assert - at frame 0, sin(0) = 0, so offset is 0
        assert result == 100

    def test_apply_floating_effect_custom_params(self):
        """Test apply_floating_effect with custom parameters"""
        # Arrange
        y = 100
        frame_count = 0

        # Act
        result = visual_components.apply_floating_effect(
            y, frame_count, amplitude=10, speed=0.1
        )

        # Assert
        assert result == 100  # sin(0) = 0

    def test_apply_floating_effect_non_zero_frame(self):
        """Test apply_floating_effect with non-zero frame"""
        # Arrange
        y = 100
        frame_count = 10

        # Act
        result = visual_components.apply_floating_effect(y, frame_count)

        # Assert - result should be different from y
        assert result != 100

    def test_create_transparent_surface(self):
        """Test create_transparent_surface creates surface with SRCALPHA"""
        # Arrange & Act
        surface = visual_components.create_transparent_surface(100, 200)

        # Assert
        assert surface.get_width() == 100
        assert surface.get_height() == 200
        assert surface.get_flags() & pygame.SRCALPHA

    def test_draw_glow_effect(self):
        """Test draw_glow_effect draws without error"""
        # Arrange
        screen = pygame.display.get_surface()
        center = (100, 100)
        radius = 50
        color = (255, 0, 0)
        frame_count = 0

        # Act & Assert - should not raise exception
        visual_components.draw_glow_effect(screen, center, radius, color, frame_count)

    def test_draw_glow_effect_custom_alpha(self):
        """Test draw_glow_effect with custom alpha parameters"""
        # Arrange
        screen = pygame.display.get_surface()
        center = (100, 100)
        radius = 50
        color = (0, 255, 0)
        frame_count = 0

        # Act & Assert - should not raise exception
        visual_components.draw_glow_effect(
            screen,
            center,
            radius,
            color,
            frame_count,
            min_alpha=20,
            max_alpha=200,
            speed=0.2,
        )

    def test_draw_wispy_trail(self):
        """Test draw_wispy_trail draws without error"""
        # Arrange
        screen = pygame.display.get_surface()
        x = 100.0
        y = 100.0
        width = 50.0
        height = 50.0
        frame_count = 0

        # Act & Assert - should not raise exception
        visual_components.draw_wispy_trail(screen, x, y, width, height, frame_count)

    def test_draw_wispy_trail_custom_color(self):
        """Test draw_wispy_trail with custom color"""
        # Arrange
        screen = pygame.display.get_surface()
        x = 100.0
        y = 100.0
        width = 50.0
        height = 50.0
        frame_count = 0

        # Act & Assert - should not raise exception
        visual_components.draw_wispy_trail(
            screen,
            x,
            y,
            width,
            height,
            frame_count,
            color=(100, 150, 200),
            min_alpha=30,
            max_alpha=100,
        )

    def test_apply_size_tuple_with_tuple(self):
        """Test apply_size_tuple with tuple input"""
        # Arrange
        size = (100, 200)

        # Act
        result = visual_components.apply_size_tuple(size)

        # Assert
        assert result == (100, 200)

    def test_apply_size_tuple_with_single_value(self):
        """Test apply_size_tuple with single value"""
        # Arrange
        size = 100

        # Act
        result = visual_components.apply_size_tuple(size)

        # Assert
        assert result == (100, 100)

    def test_apply_pulse_effect_default_params(self):
        """Test apply_pulse_effect with default parameters"""
        # Arrange
        size = 100.0
        frame_count = 0

        # Act
        result = visual_components.apply_pulse_effect(size, frame_count)

        # Assert - at frame 0, pulse should be 1.0
        assert result == 100.0

    def test_apply_pulse_effect_custom_params(self):
        """Test apply_pulse_effect with custom parameters"""
        # Arrange
        size = 100.0
        frame_count = 0

        # Act
        result = visual_components.apply_pulse_effect(
            size, frame_count, intensity=0.2, speed=0.1
        )

        # Assert
        assert result == 100.0

    def test_draw_aura_effect(self):
        """Test draw_aura_effect draws without error"""
        # Arrange
        screen = pygame.display.get_surface()
        x = 100.0
        y = 100.0
        width = 50.0
        height = 50.0
        frame_count = 0
        color = (255, 0, 255)

        # Act & Assert - should not raise exception
        visual_components.draw_aura_effect(
            screen, x, y, width, height, frame_count, color
        )

    def test_draw_aura_effect_custom_params(self):
        """Test draw_aura_effect with custom parameters"""
        # Arrange
        screen = pygame.display.get_surface()
        x = 100.0
        y = 100.0
        width = 50.0
        height = 50.0
        frame_count = 0
        color = (0, 255, 0)

        # Act & Assert - should not raise exception
        visual_components.draw_aura_effect(
            screen,
            x,
            y,
            width,
            height,
            frame_count,
            color,
            min_alpha=10,
            max_alpha=100,
            size_multiplier=1.5,
        )
