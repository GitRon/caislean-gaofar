"""Tests for game.py - Game class"""

from unittest.mock import patch
import pygame
from game import Game
import config


# Initialize pygame
pygame.init()


class TestGame:
    """Tests for Game class"""

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_game_initialization(self, mock_caption, mock_clock, mock_display):
        """Test Game initialization"""
        # Arrange & Act
        game = Game()

        # Assert
        assert game.state == config.STATE_PLAYING
        assert game.warrior is not None
        assert game.monsters is not None
        assert len(game.monsters) > 0
        assert game.combat_system is not None
        assert game.inventory_ui is not None
        assert game.world_map is not None
        assert game.camera is not None

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_game_initial_state_is_playing(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test game starts in PLAYING state"""
        # Arrange & Act
        game = Game()

        # Assert
        assert game.state == config.STATE_PLAYING

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_temple_initialization(self, mock_caption, mock_clock, mock_display):
        """Test temple is initialized in game"""
        # Arrange & Act
        game = Game()

        # Assert
        assert game.temple is not None
        assert game.temple.grid_x == 8
        assert game.temple.grid_y == 1

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_heal_at_temple_restores_health(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test healing at temple restores health to max"""
        # Arrange
        game = Game()
        game.warrior.health = 50  # Set health below max
        initial_max_health = game.warrior.max_health

        # Act
        game._heal_at_temple()

        # Assert
        assert game.warrior.health == initial_max_health
        assert game.temple.healing_active is True

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_heal_at_temple_when_already_full_health(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test healing at temple when already at full health"""
        # Arrange
        game = Game()
        game.warrior.health = game.warrior.max_health  # Full health

        # Act
        game._heal_at_temple()

        # Assert - healing effect should not activate
        assert game.warrior.health == game.warrior.max_health
        assert game.temple.healing_active is False

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_heal_at_temple_shows_message(self, mock_caption, mock_clock, mock_display):
        """Test healing at temple shows message"""
        # Arrange
        game = Game()
        game.warrior.health = 50  # Set health below max

        # Act
        game._heal_at_temple()

        # Assert
        assert game.message == "The temple's divine power restores your health!"
        assert game.message_timer > 0
