"""Tests for main menu functionality."""

import pygame
import pytest
from unittest.mock import patch
from caislean_gaofar.ui.main_menu import MainMenu
from caislean_gaofar.core import config


@pytest.fixture
def mock_screen():
    """Create a mock pygame screen."""
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    yield screen
    pygame.quit()


@pytest.fixture
def main_menu(mock_screen):
    """Create a MainMenu instance for testing."""
    return MainMenu(mock_screen)


def test_main_menu_init(mock_screen):
    """Test main menu initialization."""
    menu = MainMenu(mock_screen)
    assert menu.screen == mock_screen
    assert menu.selected_option == 0
    assert menu.save_files == []
    assert menu.running is True
    assert menu.result is None


def test_load_save_files_empty(main_menu):
    """Test loading save files when none exist."""
    with patch(
        "caislean_gaofar.ui.main_menu.SaveGame.list_save_files", return_value=[]
    ):
        main_menu.load_save_files()
        assert main_menu.save_files == []


def test_load_save_files_with_data(main_menu):
    """Test loading save files with existing saves."""
    mock_saves = [
        {"filename": "save1", "timestamp": "2024-01-01T12:00:00"},
        {"filename": "save2", "timestamp": "2024-01-02T12:00:00"},
    ]
    with patch(
        "caislean_gaofar.ui.main_menu.SaveGame.list_save_files", return_value=mock_saves
    ):
        main_menu.load_save_files()
        assert main_menu.save_files == mock_saves


def test_select_new_game(main_menu):
    """Test selecting new game option."""
    main_menu.selected_option = 0
    main_menu.select_option()

    assert main_menu.result == ("new", None)
    assert main_menu.running is False


def test_select_load_game(main_menu):
    """Test selecting load game option."""
    mock_save_data = {"player": {"health": 100}}
    main_menu.save_files = [{"filename": "test_save"}]
    main_menu.selected_option = 1

    with patch(
        "caislean_gaofar.ui.main_menu.SaveGame.load_game", return_value=mock_save_data
    ):
        main_menu.select_option()

        assert main_menu.result == ("load", mock_save_data)
        assert main_menu.running is False


def test_select_load_game_invalid_index(main_menu):
    """Test selecting load game with invalid index."""
    main_menu.save_files = [{"filename": "test_save"}]
    main_menu.selected_option = 2  # Out of range

    main_menu.select_option()

    # Should not change result or stop running
    assert main_menu.result is None
    assert main_menu.running is True


def test_delete_selected_save(main_menu):
    """Test deleting a selected save file."""
    mock_saves = [
        {"filename": "save1", "timestamp": "2024-01-01T12:00:00"},
        {"filename": "save2", "timestamp": "2024-01-02T12:00:00"},
    ]
    main_menu.save_files = mock_saves.copy()
    main_menu.selected_option = 1  # Select first save (index 0)

    with patch(
        "caislean_gaofar.ui.main_menu.SaveGame.delete_save", return_value=True
    ) as mock_delete:
        with patch(
            "caislean_gaofar.ui.main_menu.SaveGame.list_save_files",
            return_value=[mock_saves[1]],
        ):
            main_menu.delete_selected_save()
            mock_delete.assert_called_once_with("save1")
            assert len(main_menu.save_files) == 1


def test_delete_selected_save_new_game_selected(main_menu):
    """Test that delete does nothing when new game is selected."""
    main_menu.selected_option = 0  # New game option
    main_menu.save_files = [{"filename": "save1"}]

    with patch("caislean_gaofar.ui.main_menu.SaveGame.delete_save") as mock_delete:
        main_menu.delete_selected_save()
        mock_delete.assert_not_called()


def test_delete_adjusts_selection_when_needed(main_menu):
    """Test that selection is adjusted if it becomes out of range."""
    main_menu.save_files = [{"filename": "save1"}]
    main_menu.selected_option = 1  # Only save

    with patch("caislean_gaofar.ui.main_menu.SaveGame.delete_save", return_value=True):
        with patch(
            "caislean_gaofar.ui.main_menu.SaveGame.list_save_files", return_value=[]
        ):
            main_menu.delete_selected_save()
            # Selection should be adjusted to 0 (no saves left)
            assert main_menu.selected_option == 0


def test_handle_events_quit(main_menu):
    """Test handling quit event."""
    quit_event = pygame.event.Event(pygame.QUIT)

    with patch("pygame.event.get", return_value=[quit_event]):
        main_menu.handle_events()

        assert main_menu.running is False
        assert main_menu.result is None


def test_handle_events_escape(main_menu):
    """Test handling escape key."""
    escape_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)

    with patch("pygame.event.get", return_value=[escape_event]):
        main_menu.handle_events()

        assert main_menu.running is False
        assert main_menu.result is None


def test_handle_events_up_key(main_menu):
    """Test handling up arrow key."""
    main_menu.selected_option = 2
    up_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)

    with patch("pygame.event.get", return_value=[up_event]):
        main_menu.handle_events()

        assert main_menu.selected_option == 1


def test_handle_events_up_key_at_top(main_menu):
    """Test handling up arrow key when already at top."""
    main_menu.selected_option = 0
    up_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)

    with patch("pygame.event.get", return_value=[up_event]):
        main_menu.handle_events()

        assert main_menu.selected_option == 0  # Should stay at 0


def test_handle_events_down_key(main_menu):
    """Test handling down arrow key."""
    main_menu.save_files = [{"filename": "save1"}, {"filename": "save2"}]
    main_menu.selected_option = 0
    down_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)

    with patch("pygame.event.get", return_value=[down_event]):
        main_menu.handle_events()

        assert main_menu.selected_option == 1


def test_handle_events_down_key_at_bottom(main_menu):
    """Test handling down arrow key when already at bottom."""
    main_menu.save_files = [{"filename": "save1"}]
    main_menu.selected_option = 1  # Max is 1 (one save file)
    down_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)

    with patch("pygame.event.get", return_value=[down_event]):
        main_menu.handle_events()

        assert main_menu.selected_option == 1  # Should stay at 1


def test_handle_events_enter_key(main_menu):
    """Test handling enter key to select option."""
    main_menu.selected_option = 0
    enter_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)

    with patch("pygame.event.get", return_value=[enter_event]):
        main_menu.handle_events()

        assert main_menu.result == ("new", None)
        assert main_menu.running is False


def test_handle_events_space_key(main_menu):
    """Test handling space key to select option."""
    main_menu.selected_option = 0
    space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)

    with patch("pygame.event.get", return_value=[space_event]):
        main_menu.handle_events()

        assert main_menu.result == ("new", None)
        assert main_menu.running is False


def test_handle_events_delete_key(main_menu):
    """Test handling delete key to remove save."""
    main_menu.save_files = [{"filename": "save1"}]
    main_menu.selected_option = 1
    delete_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DELETE)

    with patch("pygame.event.get", return_value=[delete_event]):
        with patch.object(main_menu, "delete_selected_save") as mock_delete:
            main_menu.handle_events()
            mock_delete.assert_called_once()


def test_draw_renders_without_error(main_menu):
    """Test that draw method runs without error."""
    main_menu.save_files = []
    # Just verify it doesn't raise an exception
    try:
        main_menu.draw()
    except Exception as e:
        pytest.fail(f"Draw raised an exception: {e}")


def test_draw_with_save_files(main_menu):
    """Test that draw method handles save files without error."""
    main_menu.save_files = [
        {
            "filename": "save1",
            "timestamp": "2024-01-01T12:00:00",
            "player_health": 100,
            "player_gold": 50,
        }
    ]
    main_menu.selected_option = 1

    try:
        main_menu.draw()
    except Exception as e:
        pytest.fail(f"Draw raised an exception: {e}")
