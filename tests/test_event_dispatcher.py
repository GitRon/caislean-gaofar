"""Unit tests for EventDispatcher class."""

from unittest.mock import Mock, patch
import pygame
from event_dispatcher import EventDispatcher
from warrior import Warrior
from game_state_manager import GameStateManager
from turn_processor import TurnProcessor
from entity_manager import EntityManager
from inventory_ui import InventoryUI
from shop import Shop
from shop_ui import ShopUI
import config


class TestEventDispatcher:
    """Test cases for EventDispatcher class."""

    def test_initialization(self):
        """Test EventDispatcher initialization."""
        dispatcher = EventDispatcher()
        assert dispatcher.running is True
        assert dispatcher.last_key_time == 0
        assert dispatcher.key_delay == 200

    def test_reset(self):
        """Test resetting event dispatcher."""
        # Arrange
        dispatcher = EventDispatcher()
        dispatcher.last_key_time = 1000

        # Act
        dispatcher.reset()

        # Assert
        assert dispatcher.last_key_time == 0

    @patch("pygame.event.get")
    def test_handle_quit_event(self, mock_get_events):
        """Test handling quit event."""
        # Arrange
        dispatcher = EventDispatcher()
        quit_event = Mock()
        quit_event.type = pygame.QUIT
        mock_get_events.return_value = [quit_event]

        # Mock all required parameters
        mocks = self._create_mock_parameters()

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        assert dispatcher.running is False

    @patch("pygame.event.get")
    @patch("pygame.time.get_ticks")
    def test_handle_escape_key(self, mock_ticks, mock_get_events):
        """Test handling escape key to quit."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_ticks.return_value = 1000

        escape_event = Mock()
        escape_event.type = pygame.KEYDOWN
        escape_event.key = pygame.K_ESCAPE
        mock_get_events.return_value = [escape_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        assert dispatcher.running is False

    @patch("pygame.event.get")
    def test_handle_restart_key_on_game_over(self, mock_get_events):
        """Test handling restart key on game over screen."""
        # Arrange
        dispatcher = EventDispatcher()

        restart_event = Mock()
        restart_event.type = pygame.KEYDOWN
        restart_event.key = pygame.K_r
        mock_get_events.return_value = [restart_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_GAME_OVER

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["on_restart"].assert_called_once()

    @patch("pygame.event.get")
    def test_handle_quick_save_key(self, mock_get_events):
        """Test handling F5 quick save key."""
        # Arrange
        dispatcher = EventDispatcher()

        save_event = Mock()
        save_event.type = pygame.KEYDOWN
        save_event.key = pygame.K_F5
        mock_get_events.return_value = [save_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["on_save"].assert_called_once_with("quicksave")

    @patch("pygame.event.get")
    def test_handle_inventory_toggle(self, mock_get_events):
        """Test handling inventory toggle key."""
        # Arrange
        dispatcher = EventDispatcher()

        inv_event = Mock()
        inv_event.type = pygame.KEYDOWN
        inv_event.key = pygame.K_i
        mock_get_events.return_value = [inv_event]

        mocks = self._create_mock_parameters()
        game_state_manager = mocks["game_state_manager"]
        game_state_manager.state = config.STATE_PLAYING

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        game_state_manager.transition_to_inventory.assert_called_once()

    @patch("pygame.event.get")
    def test_handle_inventory_close(self, mock_get_events):
        """Test closing inventory."""
        # Arrange
        dispatcher = EventDispatcher()

        inv_event = Mock()
        inv_event.type = pygame.KEYDOWN
        inv_event.key = pygame.K_i
        mock_get_events.return_value = [inv_event]

        mocks = self._create_mock_parameters()
        game_state_manager = mocks["game_state_manager"]
        game_state_manager.state = config.STATE_INVENTORY
        game_state_manager.return_portal = None

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        game_state_manager.transition_from_inventory.assert_called_once()

    @patch("pygame.event.get")
    def test_handle_shop_toggle_success(self, mock_get_events):
        """Test opening shop when near."""
        # Arrange
        dispatcher = EventDispatcher()

        shop_event = Mock()
        shop_event.type = pygame.KEYDOWN
        shop_event.key = pygame.K_s
        mock_get_events.return_value = [shop_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING
        mocks["on_shop_check"].return_value = (True, "")

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["game_state_manager"].transition_to_shop.assert_called_once_with(True)

    @patch("pygame.event.get")
    def test_handle_shop_toggle_fail(self, mock_get_events):
        """Test trying to open shop when not near."""
        # Arrange
        dispatcher = EventDispatcher()

        shop_event = Mock()
        shop_event.type = pygame.KEYDOWN
        shop_event.key = pygame.K_s
        mock_get_events.return_value = [shop_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING
        mocks["on_shop_check"].return_value = (False, "No shop nearby!")

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["game_state_manager"].show_message.assert_called_once_with(
            "No shop nearby!"
        )

    @patch("pygame.event.get")
    def test_handle_pickup_key(self, mock_get_events):
        """Test handling pickup key."""
        # Arrange
        dispatcher = EventDispatcher()

        pickup_event = Mock()
        pickup_event.type = pygame.KEYDOWN
        pickup_event.key = pygame.K_g
        mock_get_events.return_value = [pickup_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING
        mocks["warrior"].grid_x = 5
        mocks["warrior"].grid_y = 10

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["on_pickup_item"].assert_called_once_with(5, 10)

    @patch("pygame.event.get")
    def test_handle_potion_key(self, mock_get_events):
        """Test handling potion use key."""
        # Arrange
        dispatcher = EventDispatcher()

        potion_event = Mock()
        potion_event.type = pygame.KEYDOWN
        potion_event.key = pygame.K_p
        mock_get_events.return_value = [potion_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["on_use_potion"].assert_called_once()

    @patch("pygame.event.get")
    def test_handle_town_portal_key(self, mock_get_events):
        """Test handling town portal key."""
        # Arrange
        dispatcher = EventDispatcher()

        portal_event = Mock()
        portal_event.type = pygame.KEYDOWN
        portal_event.key = pygame.K_t
        mock_get_events.return_value = [portal_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["on_use_town_portal"].assert_called_once()

    @patch("pygame.event.get")
    @patch("pygame.time.get_ticks")
    def test_handle_movement_keys(self, mock_ticks, mock_get_events):
        """Test handling movement keys."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_ticks.return_value = 1000

        move_event = Mock()
        move_event.type = pygame.KEYDOWN
        move_event.key = pygame.K_w
        mock_get_events.return_value = [move_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING
        mocks["turn_processor"].waiting_for_player_input = True

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["turn_processor"].queue_player_action.assert_called_once_with(
            "move", mocks["warrior"], 0, -1
        )

    @patch("pygame.event.get")
    @patch("pygame.time.get_ticks")
    def test_handle_attack_key(self, mock_ticks, mock_get_events):
        """Test handling attack key."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_ticks.return_value = 1000

        attack_event = Mock()
        attack_event.type = pygame.KEYDOWN
        attack_event.key = pygame.K_SPACE
        mock_get_events.return_value = [attack_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING
        mocks["turn_processor"].waiting_for_player_input = True

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["turn_processor"].queue_player_action.assert_called_once_with(
            "attack", mocks["warrior"]
        )

    @patch("pygame.event.get")
    @patch("pygame.time.get_ticks")
    def test_movement_key_delay(self, mock_ticks, mock_get_events):
        """Test that movement respects key delay."""
        # Arrange
        dispatcher = EventDispatcher()
        dispatcher.last_key_time = 1000
        mock_ticks.return_value = 1100  # Only 100ms since last key

        move_event = Mock()
        move_event.type = pygame.KEYDOWN
        move_event.key = pygame.K_w
        mock_get_events.return_value = [move_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING
        mocks["turn_processor"].waiting_for_player_input = True

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["turn_processor"].queue_player_action.assert_not_called()

    @patch("pygame.event.get")
    def test_inventory_ui_handle_input_called(self, mock_get_events):
        """Test that inventory UI receives input events."""
        # Arrange
        dispatcher = EventDispatcher()

        test_event = Mock()
        test_event.type = pygame.MOUSEBUTTONDOWN
        mock_get_events.return_value = [test_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_INVENTORY

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["inventory_ui"].handle_input.assert_called_once_with(
            test_event, mocks["warrior"].inventory, mocks["inventory_game_ref"]
        )

    @patch("pygame.event.get")
    def test_shop_ui_handle_input_called(self, mock_get_events):
        """Test that shop UI receives input events."""
        # Arrange
        dispatcher = EventDispatcher()

        test_event = Mock()
        test_event.type = pygame.MOUSEBUTTONDOWN
        mock_get_events.return_value = [test_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_SHOP

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["shop_ui"].handle_input.assert_called_once_with(
            test_event, mocks["shop"], mocks["warrior"]
        )

    @patch("pygame.event.get")
    def test_handle_escape_in_shop_with_return_portal(self, mock_get_events):
        """Test handling ESC key in shop with return portal."""
        # Arrange
        dispatcher = EventDispatcher()

        escape_event = Mock()
        escape_event.type = pygame.KEYDOWN
        escape_event.key = pygame.K_ESCAPE
        mock_get_events.return_value = [escape_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_SHOP
        mocks["game_state_manager"].return_portal = True

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["on_use_return_portal"].assert_called_once()

    @patch("pygame.event.get")
    def test_handle_skills_toggle_open(self, mock_get_events):
        """Test opening skills screen."""
        # Arrange
        dispatcher = EventDispatcher()

        skills_event = Mock()
        skills_event.type = pygame.KEYDOWN
        skills_event.key = pygame.K_c
        mock_get_events.return_value = [skills_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        assert mocks["game_state_manager"].state == config.STATE_SKILLS

    @patch("pygame.event.get")
    def test_handle_skills_toggle_close(self, mock_get_events):
        """Test closing skills screen."""
        # Arrange
        dispatcher = EventDispatcher()

        skills_event = Mock()
        skills_event.type = pygame.KEYDOWN
        skills_event.key = pygame.K_c
        mock_get_events.return_value = [skills_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_SKILLS

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        assert mocks["game_state_manager"].state == config.STATE_PLAYING

    @patch("pygame.event.get")
    def test_handle_shop_exit(self, mock_get_events):
        """Test exiting shop with S key."""
        # Arrange
        dispatcher = EventDispatcher()

        shop_event = Mock()
        shop_event.type = pygame.KEYDOWN
        shop_event.key = pygame.K_s
        mock_get_events.return_value = [shop_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_SHOP

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["game_state_manager"].transition_from_shop.assert_called_once()

    @patch("pygame.event.get")
    @patch("pygame.time.get_ticks")
    def test_handle_movement_down_arrow(self, mock_ticks, mock_get_events):
        """Test handling DOWN arrow for down movement."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_ticks.return_value = 1000

        move_event = Mock()
        move_event.type = pygame.KEYDOWN
        move_event.key = pygame.K_DOWN
        mock_get_events.return_value = [move_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING
        mocks["turn_processor"].waiting_for_player_input = True

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["turn_processor"].queue_player_action.assert_called_once_with(
            "move", mocks["warrior"], 0, 1
        )

    @patch("pygame.event.get")
    @patch("pygame.time.get_ticks")
    def test_handle_movement_left_a(self, mock_ticks, mock_get_events):
        """Test handling A key for left movement."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_ticks.return_value = 1000

        move_event = Mock()
        move_event.type = pygame.KEYDOWN
        move_event.key = pygame.K_a
        mock_get_events.return_value = [move_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING
        mocks["turn_processor"].waiting_for_player_input = True

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["turn_processor"].queue_player_action.assert_called_once_with(
            "move", mocks["warrior"], -1, 0
        )

    @patch("pygame.event.get")
    @patch("pygame.time.get_ticks")
    def test_handle_movement_left_arrow(self, mock_ticks, mock_get_events):
        """Test handling LEFT arrow for left movement."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_ticks.return_value = 1000

        move_event = Mock()
        move_event.type = pygame.KEYDOWN
        move_event.key = pygame.K_LEFT
        mock_get_events.return_value = [move_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING
        mocks["turn_processor"].waiting_for_player_input = True

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["turn_processor"].queue_player_action.assert_called_once_with(
            "move", mocks["warrior"], -1, 0
        )

    @patch("pygame.event.get")
    @patch("pygame.time.get_ticks")
    def test_handle_movement_right_d(self, mock_ticks, mock_get_events):
        """Test handling D key for right movement."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_ticks.return_value = 1000

        move_event = Mock()
        move_event.type = pygame.KEYDOWN
        move_event.key = pygame.K_d
        mock_get_events.return_value = [move_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING
        mocks["turn_processor"].waiting_for_player_input = True

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["turn_processor"].queue_player_action.assert_called_once_with(
            "move", mocks["warrior"], 1, 0
        )

    @patch("pygame.event.get")
    @patch("pygame.time.get_ticks")
    def test_handle_movement_right_arrow(self, mock_ticks, mock_get_events):
        """Test handling RIGHT arrow for right movement."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_ticks.return_value = 1000

        move_event = Mock()
        move_event.type = pygame.KEYDOWN
        move_event.key = pygame.K_RIGHT
        mock_get_events.return_value = [move_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_PLAYING
        mocks["turn_processor"].waiting_for_player_input = True

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["turn_processor"].queue_player_action.assert_called_once_with(
            "move", mocks["warrior"], 1, 0
        )

    @patch("pygame.event.get")
    def test_handle_return_portal_in_shop(self, mock_get_events):
        """Test using return portal in shop with T key."""
        # Arrange
        dispatcher = EventDispatcher()

        portal_event = Mock()
        portal_event.type = pygame.KEYDOWN
        portal_event.key = pygame.K_t
        mock_get_events.return_value = [portal_event]

        mocks = self._create_mock_parameters()
        mocks["game_state_manager"].state = config.STATE_SHOP
        mocks["game_state_manager"].return_portal = True

        # Act
        dispatcher.handle_events(**mocks)

        # Assert
        mocks["on_use_return_portal"].assert_called_once()

    def _create_mock_parameters(self):
        """Create mock parameters for handle_events method."""
        warrior = Mock(spec=Warrior)
        warrior.grid_x = 0
        warrior.grid_y = 0
        warrior.inventory = Mock()

        game_state_manager = Mock(spec=GameStateManager)
        game_state_manager.state = config.STATE_PLAYING
        game_state_manager.return_portal = None
        game_state_manager.transition_to_inventory = Mock()
        game_state_manager.transition_from_inventory = Mock()
        game_state_manager.transition_to_shop = Mock()
        game_state_manager.transition_from_shop = Mock()
        game_state_manager.show_message = Mock()

        turn_processor = Mock(spec=TurnProcessor)
        turn_processor.waiting_for_player_input = False
        turn_processor.queue_player_action = Mock()

        entity_manager = Mock(spec=EntityManager)
        inventory_ui = Mock(spec=InventoryUI)
        shop = Mock(spec=Shop)
        shop_ui = Mock(spec=ShopUI)
        dungeon_manager = Mock()

        return {
            "warrior": warrior,
            "game_state_manager": game_state_manager,
            "turn_processor": turn_processor,
            "entity_manager": entity_manager,
            "inventory_ui": inventory_ui,
            "shop": shop,
            "shop_ui": shop_ui,
            "dungeon_manager": dungeon_manager,
            "on_restart": Mock(),
            "on_save": Mock(),
            "on_pickup_item": Mock(),
            "on_use_potion": Mock(),
            "on_use_town_portal": Mock(),
            "on_use_return_portal": Mock(),
            "on_shop_check": Mock(),
            "inventory_game_ref": Mock(),
        }
