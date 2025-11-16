"""Tests for game_loop.py"""

from unittest.mock import MagicMock, patch
import pygame
from caislean_gaofar.core.game_loop import GameLoop

# Initialize pygame
pygame.init()


class TestGameLoop:
    """Tests for GameLoop class"""

    def test_game_loop_initialization(self):
        """Test GameLoop initialization"""
        # Arrange
        clock = pygame.time.Clock()

        # Act
        game_loop = GameLoop(clock)

        # Assert
        assert game_loop.clock is clock
        assert game_loop.running is True

    def test_game_loop_run_executes_callbacks(self):
        """Test that run() executes callbacks in correct order"""
        # Arrange
        clock = pygame.time.Clock()
        game_loop = GameLoop(clock)

        handle_events_mock = MagicMock()
        update_mock = MagicMock()
        draw_mock = MagicMock()

        # Track number of iterations
        iteration_count = [0]

        def handle_events_wrapper():
            iteration_count[0] += 1
            handle_events_mock()
            if iteration_count[0] >= 2:
                game_loop.stop()

        # Act
        with patch("pygame.quit"):
            game_loop.run(
                handle_events=handle_events_wrapper,
                update=update_mock,
                draw=draw_mock,
            )

        # Assert
        assert iteration_count[0] == 2
        assert handle_events_mock.call_count == 2
        assert update_mock.call_count == 2
        assert draw_mock.call_count == 2

    def test_game_loop_stop(self):
        """Test stopping the game loop"""
        # Arrange
        clock = pygame.time.Clock()
        game_loop = GameLoop(clock)

        # Act
        game_loop.stop()

        # Assert
        assert game_loop.running is False

    def test_game_loop_calls_pygame_quit(self):
        """Test that run() calls pygame.quit() when stopped"""
        # Arrange
        clock = pygame.time.Clock()
        game_loop = GameLoop(clock)
        game_loop.stop()  # Stop immediately

        handle_events_mock = MagicMock()
        update_mock = MagicMock()
        draw_mock = MagicMock()

        # Act
        with patch("pygame.quit") as mock_quit:
            game_loop.run(
                handle_events=handle_events_mock,
                update=update_mock,
                draw=draw_mock,
            )

            # Assert
            mock_quit.assert_called_once()

    def test_game_loop_passes_delta_time_to_update(self):
        """Test that update receives delta time parameter"""
        # Arrange
        mock_clock = MagicMock()
        mock_clock.tick.return_value = 16  # 16 milliseconds
        game_loop = GameLoop(mock_clock)

        handle_events_mock = MagicMock()
        update_mock = MagicMock()
        draw_mock = MagicMock()

        iteration_count = [0]

        def handle_events_wrapper():
            iteration_count[0] += 1
            handle_events_mock()
            if iteration_count[0] >= 1:
                game_loop.stop()

        # Act
        with patch("pygame.quit"):
            game_loop.run(
                handle_events=handle_events_wrapper,
                update=update_mock,
                draw=draw_mock,
            )

        # Assert
        update_mock.assert_called()
        # Delta time should be 16 ms / 1000 = 0.016 seconds
        call_args = update_mock.call_args[0]
        assert len(call_args) == 1
        assert call_args[0] == 0.016
