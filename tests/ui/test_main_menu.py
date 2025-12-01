"""Tests for main menu functionality."""

import pygame
import pytest
from unittest.mock import patch
from caislean_gaofar.ui.main_menu import MainMenu
from caislean_gaofar.core import config


@pytest.fixture
def mock_screen() -> pygame.Surface:
    """Create a mock pygame screen."""
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    yield screen
    pygame.quit()


@pytest.fixture
def main_menu(mock_screen) -> MainMenu:
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


def test_run_with_quit_event(main_menu):
    """Test run method with quit event."""
    quit_event = pygame.event.Event(pygame.QUIT)

    with patch(
        "caislean_gaofar.ui.main_menu.SaveGame.list_save_files", return_value=[]
    ):
        with patch("pygame.event.get", return_value=[quit_event]):
            result = main_menu.run()

            assert result is None
            assert main_menu.running is False


def test_run_with_new_game_selection(main_menu):
    """Test run method selecting new game."""
    # Create events: press ENTER to select new game
    enter_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)

    with patch(
        "caislean_gaofar.ui.main_menu.SaveGame.list_save_files", return_value=[]
    ):
        # First call returns enter, second call returns empty to allow loop to exit
        with patch("pygame.event.get", side_effect=[[enter_event], []]):
            result = main_menu.run()

            assert result == ("new", None)
            assert main_menu.running is False


def test_run_with_escape_key(main_menu):
    """Test run method with escape key."""
    escape_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)

    with patch(
        "caislean_gaofar.ui.main_menu.SaveGame.list_save_files", return_value=[]
    ):
        with patch("pygame.event.get", return_value=[escape_event]):
            result = main_menu.run()

            assert result is None
            assert main_menu.running is False


def test_run_with_load_game_selection(main_menu):
    """Test run method selecting load game."""
    mock_saves = [{"filename": "save1", "timestamp": "2024-01-01T12:00:00"}]
    mock_save_data = {"player": {"health": 100}}

    # Navigate down to first save, then press enter
    down_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
    enter_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)

    with patch(
        "caislean_gaofar.ui.main_menu.SaveGame.list_save_files", return_value=mock_saves
    ):
        with patch(
            "caislean_gaofar.ui.main_menu.SaveGame.load_game",
            return_value=mock_save_data,
        ):
            with patch(
                "pygame.event.get", side_effect=[[down_event], [enter_event], []]
            ):
                result = main_menu.run()

                assert result == ("load", mock_save_data)
                assert main_menu.running is False


def test_select_load_game_with_failed_load(main_menu):
    """Test selecting load game when save data fails to load."""
    main_menu.save_files = [{"filename": "corrupt_save"}]
    main_menu.selected_option = 1

    with patch("caislean_gaofar.ui.main_menu.SaveGame.load_game", return_value=None):
        main_menu.select_option()

        # Should not change result or stop running since load failed
        assert main_menu.result is None
        assert main_menu.running is True


def test_select_load_game_with_false_save_data(main_menu):
    """Test selecting load game when save data returns False."""
    main_menu.save_files = [{"filename": "bad_save"}]
    main_menu.selected_option = 1

    with patch("caislean_gaofar.ui.main_menu.SaveGame.load_game", return_value=False):
        main_menu.select_option()

        # Should not change result or stop running since load failed
        assert main_menu.result is None
        assert main_menu.running is True


def test_delete_selected_save_invalid_index(main_menu):
    """Test delete with invalid save index (out of range)."""
    main_menu.save_files = [{"filename": "save1"}]
    main_menu.selected_option = 2  # Index 1 would be out of range

    with patch("caislean_gaofar.ui.main_menu.SaveGame.delete_save") as mock_delete:
        main_menu.delete_selected_save()
        # Delete should not be called if index is invalid
        mock_delete.assert_not_called()


def test_handle_events_delete_key_on_new_game(main_menu):
    """Test that DELETE key does nothing when New Game is selected."""
    main_menu.selected_option = 0  # New Game
    main_menu.save_files = [{"filename": "save1"}]
    delete_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DELETE)

    with patch("pygame.event.get", return_value=[delete_event]):
        with patch.object(main_menu, "delete_selected_save") as mock_delete:
            main_menu.handle_events()
            # Should not call delete_selected_save because condition fails
            mock_delete.assert_not_called()


def test_handle_events_unhandled_key(main_menu):
    """Test handling a key that is not handled by the menu."""
    # Use a key that's not in the handle_events conditions
    unhandled_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)

    with patch("pygame.event.get", return_value=[unhandled_event]):
        main_menu.handle_events()

        # State should remain unchanged
        assert main_menu.running is True
        assert main_menu.result is None


def test_handle_events_unhandled_event_type(main_menu):
    """Test handling an event type that is not QUIT or KEYDOWN."""
    # Use MOUSEMOTION which is not handled
    unhandled_event = pygame.event.Event(pygame.MOUSEMOTION, pos=(100, 100))

    with patch("pygame.event.get", return_value=[unhandled_event]):
        main_menu.handle_events()

        # State should remain unchanged
        assert main_menu.running is True
        assert main_menu.result is None


def test_draw_with_selected_save_file_delete_hint(main_menu):
    """Test drawing when a save file is selected (shows delete hint)."""
    main_menu.save_files = [
        {"filename": "save1", "timestamp": "2024-01-01T12:00:00.123456"}
    ]
    main_menu.selected_option = 1  # Select the save file

    try:
        main_menu.draw()
        # Should render delete hint when save is selected
    except Exception as e:
        pytest.fail(f"Draw raised an exception: {e}")


def test_draw_with_multiple_save_files(main_menu):
    """Test drawing with multiple save files."""
    main_menu.save_files = [
        {"filename": "save1", "timestamp": "2024-01-01T12:00:00.123"},
        {"filename": "save2", "timestamp": "2024-01-02T15:30:45.678"},
        {"filename": "save3", "timestamp": "2024-01-03T09:15:30.999"},
    ]
    main_menu.selected_option = 2  # Select middle save

    try:
        main_menu.draw()
    except Exception as e:
        pytest.fail(f"Draw raised an exception: {e}")


def test_draw_with_malformed_timestamp(main_menu):
    """Test drawing with malformed timestamp in save file."""
    main_menu.save_files = [{"filename": "save1", "timestamp": "InvalidTimestamp"}]
    main_menu.selected_option = 0

    try:
        main_menu.draw()
        # Should handle malformed timestamp gracefully
    except Exception as e:
        pytest.fail(f"Draw raised an exception: {e}")


def test_draw_with_timestamp_without_time_part(main_menu):
    """Test drawing with timestamp that has no time component."""
    main_menu.save_files = [{"filename": "save1", "timestamp": "2024-01-01"}]
    main_menu.selected_option = 1

    try:
        main_menu.draw()
        # Should handle timestamp without time part
    except Exception as e:
        pytest.fail(f"Draw raised an exception: {e}")
