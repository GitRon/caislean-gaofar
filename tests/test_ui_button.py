"""Tests for ui_button.py - Button class"""

import pytest
from unittest.mock import Mock, patch
import pygame
from ui_button import Button


@pytest.fixture(autouse=True)
def setup_pygame():
    """Setup pygame before each test and cleanup after"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_screen():
    """Create a mock pygame surface"""
    return Mock(spec=pygame.Surface)


class TestButton:
    """Tests for Button class"""

    def test_button_initialization_with_defaults(self):
        """Test Button initialization with default parameters"""
        # Arrange & Act
        button = Button(100, 50, 200, 40, "Click Me")

        # Assert
        assert button.rect.x == 100
        assert button.rect.y == 50
        assert button.rect.width == 200
        assert button.rect.height == 40
        assert button.text == "Click Me"
        assert button.bg_color == (60, 60, 70)
        assert button.hover_color == (80, 80, 90)
        assert button.text_color == (255, 255, 255)
        assert button.border_color == (100, 100, 120)
        assert button.is_hovered is False

    def test_button_initialization_with_custom_colors(self):
        """Test Button initialization with custom colors"""
        # Arrange & Act
        button = Button(
            100,
            50,
            200,
            40,
            "Click Me",
            bg_color=(255, 0, 0),
            hover_color=(0, 255, 0),
            text_color=(0, 0, 255),
            border_color=(255, 255, 0),
        )

        # Assert
        assert button.bg_color == (255, 0, 0)
        assert button.hover_color == (0, 255, 0)
        assert button.text_color == (0, 0, 255)
        assert button.border_color == (255, 255, 0)

    def test_button_initialization_with_custom_font_size(self):
        """Test Button initialization with custom font size"""
        # Arrange & Act
        button = Button(100, 50, 200, 40, "Click Me", font_size=36)

        # Assert
        assert button.text == "Click Me"

    @patch("pygame.mouse.get_pos", return_value=(150, 70))
    @patch("pygame.draw.rect")
    def test_draw_button_when_hovered(self, mock_draw_rect, mock_get_pos, mock_screen):
        """Test drawing button when mouse is hovering"""
        # Arrange
        button = Button(100, 50, 200, 40, "Click Me")

        # Act
        button.draw(mock_screen)

        # Assert
        assert button.is_hovered is True
        assert mock_draw_rect.called

    @patch("pygame.mouse.get_pos", return_value=(50, 30))
    @patch("pygame.draw.rect")
    def test_draw_button_when_not_hovered(
        self, mock_draw_rect, mock_get_pos, mock_screen
    ):
        """Test drawing button when mouse is not hovering"""
        # Arrange
        button = Button(100, 50, 200, 40, "Click Me")

        # Act
        button.draw(mock_screen)

        # Assert
        assert button.is_hovered is False
        assert mock_draw_rect.called

    @patch("pygame.mouse.get_pos", return_value=(100, 50))
    @patch("pygame.draw.rect")
    def test_draw_button_mouse_on_top_left_edge(
        self, mock_draw_rect, mock_get_pos, mock_screen
    ):
        """Test drawing button when mouse is on top-left edge"""
        # Arrange
        button = Button(100, 50, 200, 40, "Click Me")

        # Act
        button.draw(mock_screen)

        # Assert
        assert button.is_hovered is True

    @patch("pygame.mouse.get_pos", return_value=(299, 89))
    @patch("pygame.draw.rect")
    def test_draw_button_mouse_on_bottom_right_edge(
        self, mock_draw_rect, mock_get_pos, mock_screen
    ):
        """Test drawing button when mouse is on bottom-right edge"""
        # Arrange
        button = Button(100, 50, 200, 40, "Click Me")

        # Act
        button.draw(mock_screen)

        # Assert
        assert button.is_hovered is True

    @patch("pygame.mouse.get_pos", return_value=(300, 90))
    @patch("pygame.draw.rect")
    def test_draw_button_mouse_outside_bottom_right(
        self, mock_draw_rect, mock_get_pos, mock_screen
    ):
        """Test drawing button when mouse is just outside bottom-right"""
        # Arrange
        button = Button(100, 50, 200, 40, "Click Me")

        # Act
        button.draw(mock_screen)

        # Assert
        assert button.is_hovered is False

    def test_is_clicked_inside_button(self):
        """Test is_clicked returns True when position inside button"""
        # Arrange
        button = Button(100, 50, 200, 40, "Click Me")

        # Act
        result = button.is_clicked((150, 70))

        # Assert
        assert result is True

    def test_is_clicked_outside_button(self):
        """Test is_clicked returns False when position outside button"""
        # Arrange
        button = Button(100, 50, 200, 40, "Click Me")

        # Act
        result = button.is_clicked((50, 30))

        # Assert
        assert result is False

    def test_is_clicked_on_top_left_corner(self):
        """Test is_clicked on top-left corner"""
        # Arrange
        button = Button(100, 50, 200, 40, "Click Me")

        # Act
        result = button.is_clicked((100, 50))

        # Assert
        assert result is True

    def test_is_clicked_on_bottom_right_corner(self):
        """Test is_clicked on bottom-right corner (inside)"""
        # Arrange
        button = Button(100, 50, 200, 40, "Click Me")

        # Act
        result = button.is_clicked((299, 89))

        # Assert
        assert result is True

    def test_is_clicked_outside_bottom_right_corner(self):
        """Test is_clicked just outside bottom-right corner"""
        # Arrange
        button = Button(100, 50, 200, 40, "Click Me")

        # Act
        result = button.is_clicked((300, 90))

        # Assert
        assert result is False

    def test_is_clicked_negative_coordinates(self):
        """Test is_clicked with negative coordinates"""
        # Arrange
        button = Button(100, 50, 200, 40, "Click Me")

        # Act
        result = button.is_clicked((-10, -10))

        # Assert
        assert result is False
