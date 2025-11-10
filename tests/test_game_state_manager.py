"""Unit tests for GameStateManager class."""

from unittest.mock import Mock, patch
from game_state_manager import GameStateManager
import config


class TestGameStateManager:
    """Test cases for GameStateManager class."""

    def test_initialization(self):
        """Test GameStateManager initialization."""
        manager = GameStateManager()
        assert manager.state == config.STATE_PLAYING
        assert manager.message == ""
        assert manager.message_timer == 0
        assert manager.message_duration == 3000
        assert manager.active_portal is None
        assert manager.return_portal is None
        assert manager.portal_return_location is None
        assert manager.portal_cooldown == 0

    def test_update_message_timer(self):
        """Test updating message timer."""
        # Arrange
        manager = GameStateManager()
        manager.message = "Test message"
        manager.message_timer = 1000

        clock = Mock()
        clock.get_time.return_value = 500

        warrior = Mock()

        # Act
        manager.update(clock, warrior, 0.016)

        # Assert
        assert manager.message_timer == 500

    def test_update_message_timer_expires(self):
        """Test message timer expiring."""
        # Arrange
        manager = GameStateManager()
        manager.message = "Test message"
        manager.message_timer = 300

        clock = Mock()
        clock.get_time.return_value = 500

        warrior = Mock()

        # Act
        manager.update(clock, warrior, 0.016)

        # Assert
        assert manager.message_timer <= 0
        assert manager.message == ""

    def test_update_portal_cooldown(self):
        """Test updating portal cooldown timer."""
        # Arrange
        manager = GameStateManager()
        manager.portal_cooldown = 500

        clock = Mock()
        clock.get_time.return_value = 200

        warrior = Mock()

        # Act
        manager.update(clock, warrior, 0.016)

        # Assert
        assert manager.portal_cooldown == 300

    @patch("game_state_manager.Portal")
    def test_update_portal_animations(self, mock_portal):
        """Test updating portal animations."""
        # Arrange
        manager = GameStateManager()
        active_portal = Mock()
        return_portal = Mock()
        manager.active_portal = active_portal
        manager.return_portal = return_portal

        clock = Mock()
        clock.get_time.return_value = 0

        warrior = Mock()

        # Act
        manager.update(clock, warrior, 0.016)

        # Assert
        active_portal.update.assert_called_once_with(0.016)
        return_portal.update.assert_called_once_with(0.016)

    def test_show_message(self):
        """Test showing a message."""
        # Arrange
        manager = GameStateManager()

        # Act
        manager.show_message("Test message")

        # Assert
        assert manager.message == "Test message"
        assert manager.message_timer == 3000

    @patch("game_state_manager.Portal")
    def test_use_town_portal_success(self, mock_portal):
        """Test successfully using a town portal."""
        # Arrange
        manager = GameStateManager()

        warrior = Mock()
        warrior.count_town_portals.return_value = 1
        warrior.use_town_portal.return_value = True
        warrior.grid_x = 10
        warrior.grid_y = 15

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "dungeon"
        dungeon_manager.get_current_map.return_value.spawn_point = (5, 5)

        # Act
        success, message = manager.use_town_portal(warrior, dungeon_manager)

        # Assert
        assert success is True
        assert "town" in message.lower()
        assert manager.portal_return_location == ("dungeon", 10, 15)
        assert dungeon_manager.current_map_id == "town"
        assert warrior.grid_x == 6  # spawn_x + 1
        assert warrior.grid_y == 5
        assert manager.portal_cooldown == 500
        assert manager.state == config.STATE_PLAYING

    def test_use_town_portal_no_portals(self):
        """Test using town portal when none available."""
        # Arrange
        manager = GameStateManager()

        warrior = Mock()
        warrior.count_town_portals.return_value = 0
        warrior.use_town_portal.return_value = False

        dungeon_manager = Mock()

        # Act
        success, message = manager.use_town_portal(warrior, dungeon_manager)

        # Assert
        assert success is False
        assert "No town portals" in message

    def test_use_town_portal_cannot_use(self):
        """Test using town portal when not allowed."""
        # Arrange
        manager = GameStateManager()

        warrior = Mock()
        warrior.count_town_portals.return_value = 2
        warrior.use_town_portal.return_value = False

        dungeon_manager = Mock()

        # Act
        success, message = manager.use_town_portal(warrior, dungeon_manager)

        # Assert
        assert success is False
        assert "cannot use them here" in message

    def test_use_return_portal_success(self):
        """Test successfully using return portal."""
        # Arrange
        manager = GameStateManager()
        manager.return_portal = Mock()
        manager.portal_return_location = ("dungeon", 10, 15)

        warrior = Mock()

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "town"

        # Act
        success, message = manager.use_return_portal(warrior, dungeon_manager)

        # Assert
        assert success is True
        assert "return" in message.lower()
        assert warrior.grid_x == 10
        assert warrior.grid_y == 15
        assert dungeon_manager.current_map_id == "dungeon"
        assert manager.portal_cooldown == 500
        assert manager.state == config.STATE_PLAYING
        assert manager.return_portal is None
        assert manager.active_portal is None

    def test_use_return_portal_no_portal(self):
        """Test using return portal when none exists."""
        # Arrange
        manager = GameStateManager()
        manager.return_portal = None

        warrior = Mock()
        dungeon_manager = Mock()

        # Act
        success, message = manager.use_return_portal(warrior, dungeon_manager)

        # Assert
        assert success is False
        assert "No return portal" in message

    def test_use_return_portal_same_map(self):
        """Test return portal when already on same map."""
        # Arrange
        manager = GameStateManager()
        manager.return_portal = Mock()
        manager.portal_return_location = ("town", 5, 5)

        warrior = Mock()

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "town"

        # Act
        success, message = manager.use_return_portal(warrior, dungeon_manager)

        # Assert
        assert success is True
        assert warrior.grid_x == 5
        assert warrior.grid_y == 5

    def test_check_return_portal_collision_true(self):
        """Test checking return portal collision when true."""
        # Arrange
        manager = GameStateManager()
        portal = Mock()
        portal.grid_x = 5
        portal.grid_y = 10
        manager.return_portal = portal
        manager.portal_cooldown = 0

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10

        # Act
        result = manager.check_return_portal_collision(warrior)

        # Assert
        assert result is True

    def test_check_return_portal_collision_false_no_portal(self):
        """Test checking collision when no portal exists."""
        # Arrange
        manager = GameStateManager()
        manager.return_portal = None

        warrior = Mock()

        # Act
        result = manager.check_return_portal_collision(warrior)

        # Assert
        assert result is False

    def test_check_return_portal_collision_false_cooldown(self):
        """Test checking collision during cooldown."""
        # Arrange
        manager = GameStateManager()
        manager.return_portal = Mock()
        manager.portal_cooldown = 500

        warrior = Mock()

        # Act
        result = manager.check_return_portal_collision(warrior)

        # Assert
        assert result is False

    def test_check_return_portal_collision_false_wrong_position(self):
        """Test checking collision at wrong position."""
        # Arrange
        manager = GameStateManager()
        portal = Mock()
        portal.grid_x = 5
        portal.grid_y = 10
        manager.return_portal = portal
        manager.portal_cooldown = 0

        warrior = Mock()
        warrior.grid_x = 7
        warrior.grid_y = 12

        # Act
        result = manager.check_return_portal_collision(warrior)

        # Assert
        assert result is False

    def test_close_portals(self):
        """Test closing all portals."""
        # Arrange
        manager = GameStateManager()
        manager.active_portal = Mock()
        manager.return_portal = Mock()
        manager.portal_return_location = ("test", 1, 1)

        # Act
        manager.close_portals()

        # Assert
        assert manager.active_portal is None
        assert manager.return_portal is None
        assert manager.portal_return_location is None

    def test_transition_to_inventory_from_playing(self):
        """Test transitioning to inventory from playing state."""
        # Arrange
        manager = GameStateManager()
        manager.state = config.STATE_PLAYING

        # Act
        manager.transition_to_inventory()

        # Assert
        assert manager.state == config.STATE_INVENTORY

    def test_transition_to_inventory_from_shop(self):
        """Test transitioning to inventory from shop state."""
        # Arrange
        manager = GameStateManager()
        manager.state = config.STATE_SHOP

        # Act
        manager.transition_to_inventory()

        # Assert
        assert manager.state == config.STATE_INVENTORY

    def test_transition_from_inventory_to_playing(self):
        """Test transitioning from inventory to playing."""
        # Arrange
        manager = GameStateManager()
        manager.state = config.STATE_INVENTORY
        manager.return_portal = None

        # Act
        manager.transition_from_inventory()

        # Assert
        assert manager.state == config.STATE_PLAYING

    def test_transition_from_inventory_to_shop(self):
        """Test transitioning from inventory to shop."""
        # Arrange
        manager = GameStateManager()
        manager.state = config.STATE_INVENTORY
        manager.return_portal = Mock()  # Indicates came from shop

        # Act
        manager.transition_from_inventory()

        # Assert
        assert manager.state == config.STATE_SHOP

    def test_transition_to_shop_success(self):
        """Test transitioning to shop when near."""
        # Arrange
        manager = GameStateManager()
        manager.state = config.STATE_PLAYING

        # Act
        result = manager.transition_to_shop(is_near_shop=True)

        # Assert
        assert result is True
        assert manager.state == config.STATE_SHOP

    def test_transition_to_shop_fail(self):
        """Test transitioning to shop when not near."""
        # Arrange
        manager = GameStateManager()
        manager.state = config.STATE_PLAYING

        # Act
        result = manager.transition_to_shop(is_near_shop=False)

        # Assert
        assert result is False
        assert manager.state == config.STATE_PLAYING

    def test_transition_from_shop(self):
        """Test transitioning from shop to playing."""
        # Arrange
        manager = GameStateManager()
        manager.state = config.STATE_SHOP

        # Act
        manager.transition_from_shop()

        # Assert
        assert manager.state == config.STATE_PLAYING

    def test_transition_to_game_over(self):
        """Test transitioning to game over state."""
        # Arrange
        manager = GameStateManager()
        manager.state = config.STATE_PLAYING
        manager.active_portal = Mock()
        manager.return_portal = Mock()

        # Act
        manager.transition_to_game_over()

        # Assert
        assert manager.state == config.STATE_GAME_OVER
        assert manager.active_portal is None
        assert manager.return_portal is None

    def test_reset(self):
        """Test resetting state manager."""
        # Arrange
        manager = GameStateManager()
        manager.state = config.STATE_GAME_OVER
        manager.message = "Test"
        manager.message_timer = 1000
        manager.active_portal = Mock()

        # Act
        manager.reset()

        # Assert
        assert manager.state == config.STATE_PLAYING
        assert manager.message == ""
        assert manager.message_timer == 0
        assert manager.active_portal is None
