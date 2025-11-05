"""Tests for game.py - Game class"""

import pytest
from unittest.mock import Mock, patch, MagicMock
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
        assert game.monster is not None
        assert game.combat_system is not None
        assert game.inventory_ui is not None

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
