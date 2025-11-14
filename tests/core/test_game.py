"""Tests for game.py - Game class"""

from unittest.mock import patch, MagicMock
import pygame
import os
from caislean_gaofar.core.game import Game
from caislean_gaofar.core import config
from caislean_gaofar.objects.item import Item, ItemType


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
        assert game.state_manager.state == config.STATE_PLAYING
        assert game.warrior is not None
        assert game.entity_manager.monsters is not None
        assert len(game.entity_manager.monsters) > 0
        assert game.renderer.combat_system is not None
        assert game.renderer.inventory_ui is not None
        assert game.world_map is not None
        assert game.camera is not None

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_game_initialization_with_custom_map(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test Game initialization with custom map file"""
        # Arrange
        custom_map = os.path.join("data", "maps", "town.json")

        # Act
        game = Game(map_file=custom_map)

        # Assert
        assert game.warrior is not None
        assert game.world_map is not None

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
        assert game.state_manager.state == config.STATE_PLAYING

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
        assert (
            game.state_manager.message
            == "The temple's divine power restores your health!"
        )
        assert game.state_manager.message_timer > 0

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_drop_item(self, mock_caption, mock_clock, mock_display):
        """Test dropping an item"""
        # Arrange
        game = Game()
        item = Item(
            name="Test Item", item_type=ItemType.MISC, description="A test item"
        )

        # Act
        game.drop_item(item, 5, 5)

        # Assert
        dropped_item = game.get_item_at_position(5, 5)
        assert dropped_item is not None
        assert dropped_item.item.name == "Test Item"

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_get_item_at_position_returns_none_when_no_item(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test get_item_at_position returns None when no item exists"""
        # Arrange
        game = Game()

        # Act
        result = game.get_item_at_position(99, 99)

        # Assert
        assert result is None

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_pickup_item_at_position_success(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test picking up an item successfully"""
        # Arrange
        game = Game()
        item = Item(
            name="Test Item", item_type=ItemType.MISC, description="A test item"
        )
        game.drop_item(item, 5, 5)

        # Act
        success = game.pickup_item_at_position(5, 5)

        # Assert
        assert success is True
        assert game.get_item_at_position(5, 5) is None

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_pickup_item_at_position_failure(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test picking up an item when none exists"""
        # Arrange
        game = Game()

        # Act
        success = game.pickup_item_at_position(99, 99)

        # Assert
        assert success is False

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    @patch("pygame.event.get")
    def test_handle_events_with_skill_ui_left_click(
        self, mock_event_get, mock_caption, mock_clock, mock_display
    ):
        """Test handle_events with skill UI left click"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_SKILLS

        # Create mock event
        mock_event = MagicMock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event.button = 1  # Left click
        mock_event.pos = (100, 100)
        mock_event_get.return_value = [mock_event]

        # Act
        game.handle_events()

        # Assert - should not crash and handle click
        assert game.state_manager.state == config.STATE_SKILLS

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    @patch("pygame.event.get")
    def test_handle_events_with_skill_ui_right_click(
        self, mock_event_get, mock_caption, mock_clock, mock_display
    ):
        """Test handle_events with skill UI right click"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_SKILLS

        # Create mock event
        mock_event = MagicMock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event.button = 3  # Right click
        mock_event.pos = (100, 100)
        mock_event_get.return_value = [mock_event]

        # Act
        game.handle_events()

        # Assert - should not crash and handle click
        assert game.state_manager.state == config.STATE_SKILLS

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_restart(self, mock_caption, mock_clock, mock_display):
        """Test game restart"""
        # Arrange
        game = Game()
        game.warrior.health = 50
        game.warrior.gold = 500
        original_warrior = game.warrior

        # Act
        game.restart()

        # Assert - should be a new warrior
        assert game.warrior is not original_warrior
        assert game.warrior.health == game.warrior.max_health
        assert game.state_manager.state == config.STATE_PLAYING
        assert game.dungeon_manager.current_map_id == "world"
        assert game.dungeon_manager.return_location is None

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_update_playing_state(self, mock_caption, mock_clock, mock_display):
        """Test update in PLAYING state"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_PLAYING
        game.turn_processor.waiting_for_player_input = True

        # Act
        game.update(0.016)

        # Assert - should update without error
        assert game.state_manager.state == config.STATE_PLAYING

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_update_non_playing_state(self, mock_caption, mock_clock, mock_display):
        """Test update in non-PLAYING state"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_INVENTORY

        # Act
        game.update(0.016)

        # Assert - should return early
        assert game.state_manager.state == config.STATE_INVENTORY

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_update_with_turn_processing(self, mock_caption, mock_clock, mock_display):
        """Test update processes turn when not waiting for player input"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_PLAYING
        game.turn_processor.waiting_for_player_input = False

        # Act
        game.update(0.016)

        # Assert - should process turn and wait for input again
        assert game.turn_processor.waiting_for_player_input is True

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_update_triggers_game_over_when_warrior_dies(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test update triggers game over when warrior dies"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_PLAYING
        # Kill the warrior properly by taking fatal damage
        game.warrior.take_damage(game.warrior.max_health + 100)

        # Act
        game.update(0.016)

        # Assert
        assert game.state_manager.state == config.STATE_GAME_OVER

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_update_temple_healing_in_town(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test update triggers temple healing when warrior is on temple"""
        # Arrange
        game = Game()
        game.dungeon_manager.current_map_id = "town"
        game.warrior.grid_x = game.temple.grid_x
        game.warrior.grid_y = game.temple.grid_y
        game.warrior.health = 50

        # Act
        game.update(0.016)

        # Assert
        assert game.warrior.health == game.warrior.max_health

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_process_turn(self, mock_caption, mock_clock, mock_display):
        """Test process_turn delegates to turn_processor"""
        # Arrange
        game = Game()
        game.turn_processor.waiting_for_player_input = False

        # Act
        game.process_turn()

        # Assert
        assert game.turn_processor.waiting_for_player_input is True

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_check_dungeon_transition_entering_dungeon(  # noqa: PBR008
        self, mock_caption, mock_clock, mock_display
    ):
        """Test entering a dungeon"""
        # Arrange
        game = Game()
        # Position warrior on a dungeon entrance
        for spawn in game.world_map.get_entity_spawns("dungeons"):  # noqa: PBR008
            game.warrior.grid_x = spawn["x"]
            game.warrior.grid_y = spawn["y"]
            break

        initial_map_id = game.dungeon_manager.current_map_id

        # Act
        game._check_dungeon_transition()

        # Assert - should have entered a dungeon
        assert game.dungeon_manager.current_map_id != initial_map_id

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_check_dungeon_transition_exiting_dungeon(  # noqa: PBR008
        self, mock_caption, mock_clock, mock_display
    ):  # noqa: PBR008
        """Test exiting a dungeon"""
        # Arrange
        game = Game()
        # First enter a dungeon
        for spawn in game.world_map.get_entity_spawns("dungeons"):  # noqa: PBR008
            dungeon_id = spawn["id"]
            spawn_x, spawn_y = game.dungeon_manager.enter_dungeon(
                dungeon_id, spawn["x"], spawn["y"]
            )
            game.warrior.grid_x = spawn_x
            game.warrior.grid_y = spawn_y
            game.world_map = game.dungeon_manager.get_current_map()
            break

        # Position warrior on exit (use check_for_exit to find exit location)
        # Exit is typically at position 1,1 in dark_cave.json
        game.warrior.grid_x = 1
        game.warrior.grid_y = 1

        # Act
        game._check_dungeon_transition()

        # Assert - should have exited to world map
        assert game.dungeon_manager.current_map_id == "world"

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_chest_opened(self, mock_caption, mock_clock, mock_display):
        """Test chest opened event handler"""
        # Arrange
        game = Game()
        item = Item(
            name="Treasure", item_type=ItemType.MISC, description="Valuable treasure"
        )

        # Act
        game._handle_chest_opened(item)

        # Assert
        assert "You open the chest" in game.state_manager.message
        assert "Treasure" in game.state_manager.message

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_monster_death_with_level_up(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test monster death event handler with level up"""
        # Arrange
        game = Game()
        item = Item(name="Loot", item_type=ItemType.MISC, description="Monster loot")
        # Give warrior enough XP to level up (level 1->2 requires 100 XP, give 95 + 10 = 105)
        game.warrior.experience.current_xp = 95

        # Act
        game._handle_monster_death(item, "skeleton", 10)

        # Assert
        assert "Level Up" in game.state_manager.message
        assert "Loot" in game.state_manager.message

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_monster_death_without_level_up(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test monster death event handler without level up"""
        # Arrange
        game = Game()
        item = Item(name="Loot", item_type=ItemType.MISC, description="Monster loot")

        # Act
        game._handle_monster_death(item, "skeleton", 5)

        # Assert
        assert "Level Up" not in game.state_manager.message
        assert "Loot" in game.state_manager.message
        assert "skeleton" in game.state_manager.message

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_pickup_item(self, mock_caption, mock_clock, mock_display):
        """Test pickup item event handler"""
        # Arrange
        game = Game()
        item = Item(
            name="Test Item", item_type=ItemType.MISC, description="A test item"
        )
        game.drop_item(item, 5, 5)

        # Act
        game._handle_pickup_item(5, 5)

        # Assert
        assert game.get_item_at_position(5, 5) is None

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_use_potion_success(self, mock_caption, mock_clock, mock_display):
        """Test using a health potion successfully"""
        # Arrange
        game = Game()
        game.warrior.health = 50  # Damage the warrior

        # Act
        game._handle_use_potion()

        # Assert
        assert game.warrior.health > 50
        assert "Used health potion" in game.state_manager.message

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_use_potion_no_potions(self, mock_caption, mock_clock, mock_display):  # noqa: PBR008
        """Test using a health potion when none available"""
        # Arrange
        game = Game()
        # Remove all health potions from backpack
        for i in range(len(game.warrior.inventory.backpack_slots)):  # noqa: PBR008
            item = game.warrior.inventory.backpack_slots[i]
            if item and item.item_type == ItemType.CONSUMABLE:
                game.warrior.inventory.backpack_slots[i] = None

        # Act
        game._handle_use_potion()

        # Assert
        assert "No health potions" in game.state_manager.message

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_use_potion_full_health(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test using a health potion when already at full health"""
        # Arrange
        game = Game()
        game.warrior.health = game.warrior.max_health

        # Act
        game._handle_use_potion()

        # Assert
        assert "already full" in game.state_manager.message

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_use_town_portal_success(  # noqa: PBR008
        self, mock_caption, mock_clock, mock_display
    ):  # noqa: PBR008
        """Test using town portal successfully"""
        # Arrange
        game = Game()
        # Enter a dungeon first
        for spawn in game.world_map.get_entity_spawns("dungeons"):  # noqa: PBR008
            dungeon_id = spawn["id"]
            spawn_x, spawn_y = game.dungeon_manager.enter_dungeon(
                dungeon_id, spawn["x"], spawn["y"]
            )
            game.warrior.grid_x = spawn_x
            game.warrior.grid_y = spawn_y
            game.world_map = game.dungeon_manager.get_current_map()
            break

        # Act
        game._handle_use_town_portal()

        # Assert
        assert game.dungeon_manager.current_map_id == "town"

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_use_town_portal_failure(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test using town portal when already in town"""
        # Arrange
        game = Game()
        game.dungeon_manager.current_map_id = "town"
        game.world_map = game.dungeon_manager.get_current_map()

        # Act
        game._handle_use_town_portal()

        # Assert - Check if success was False by verifying message indicates being in town
        assert "town" in game.state_manager.message.lower()

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_use_return_portal_success(  # noqa: PBR008
        self, mock_caption, mock_clock, mock_display
    ):  # noqa: PBR008
        """Test using return portal successfully"""
        # Arrange
        game = Game()
        # Enter dungeon, use town portal, then use return portal
        for spawn in game.world_map.get_entity_spawns("dungeons"):  # noqa: PBR008
            dungeon_id = spawn["id"]
            spawn_x, spawn_y = game.dungeon_manager.enter_dungeon(
                dungeon_id, spawn["x"], spawn["y"]
            )
            game.warrior.grid_x = spawn_x
            game.warrior.grid_y = spawn_y
            game.world_map = game.dungeon_manager.get_current_map()
            break

        # Use town portal
        game._handle_use_town_portal()

        # Act - Use return portal
        game._handle_use_return_portal()

        # Assert - Should be back in dungeon
        assert game.dungeon_manager.current_map_id != "town"

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_use_return_portal_failure(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test using return portal when no return location exists"""
        # Arrange
        game = Game()

        # Act
        game._handle_use_return_portal()

        # Assert
        assert "No return portal" in game.state_manager.message

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_shop_check_near_shop(self, mock_caption, mock_clock, mock_display):
        """Test shop check when near shop"""
        # Arrange
        game = Game()
        game.dungeon_manager.current_map_id = "town"
        game.warrior.grid_x = game.shop.grid_x + 1
        game.warrior.grid_y = game.shop.grid_y

        # Act
        is_near, message = game._handle_shop_check()

        # Assert
        assert is_near is True
        assert message == ""

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_shop_check_not_near_shop(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test shop check when not near shop"""
        # Arrange
        game = Game()
        game.dungeon_manager.current_map_id = "town"
        game.warrior.grid_x = game.shop.grid_x + 10
        game.warrior.grid_y = game.shop.grid_y + 10

        # Act
        is_near, message = game._handle_shop_check()

        # Assert
        assert is_near is False
        assert message == "No shop nearby!"

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_shop_check_not_in_town(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test shop check when not in town"""
        # Arrange
        game = Game()
        game.dungeon_manager.current_map_id = "world"

        # Act
        is_near, message = game._handle_shop_check()

        # Assert
        assert is_near is False
        assert message == "No shop nearby!"

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_is_near_shop_adjacent(self, mock_caption, mock_clock, mock_display):
        """Test _is_near_shop when warrior is adjacent to shop"""
        # Arrange
        game = Game()
        game.warrior.grid_x = game.shop.grid_x + 1
        game.warrior.grid_y = game.shop.grid_y

        # Act
        result = game._is_near_shop()

        # Assert
        assert result is True

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_is_near_shop_same_position(self, mock_caption, mock_clock, mock_display):
        """Test _is_near_shop when warrior is on shop"""
        # Arrange
        game = Game()
        game.warrior.grid_x = game.shop.grid_x
        game.warrior.grid_y = game.shop.grid_y

        # Act
        result = game._is_near_shop()

        # Assert
        assert result is True

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_is_near_shop_far_away(self, mock_caption, mock_clock, mock_display):
        """Test _is_near_shop when warrior is far from shop"""
        # Arrange
        game = Game()
        game.warrior.grid_x = game.shop.grid_x + 10
        game.warrior.grid_y = game.shop.grid_y + 10

        # Act
        result = game._is_near_shop()

        # Assert
        assert result is False

    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_draw_playing_state(self, mock_caption, mock_clock):
        """Test draw method in PLAYING state"""
        # Arrange
        # Set display mode before creating game (needed for font rendering)
        pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        game = Game()
        game.state_manager.state = config.STATE_PLAYING

        # Act
        game.draw()

        # Assert - should not crash
        assert game.state_manager.state == config.STATE_PLAYING

    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_draw_inventory_state(self, mock_caption, mock_clock):
        """Test draw method in INVENTORY state"""
        # Arrange
        # Set display mode before creating game (needed for font rendering)
        pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        game = Game()
        game.state_manager.state = config.STATE_INVENTORY

        # Act
        game.draw()

        # Assert - should not crash
        assert game.state_manager.state == config.STATE_INVENTORY

    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_draw_shop_state(self, mock_caption, mock_clock):
        """Test draw method in SHOP state"""
        # Arrange
        # Set display mode before creating game (needed for font rendering)
        pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        game = Game()
        game.state_manager.state = config.STATE_SHOP

        # Act
        game.draw()

        # Assert - should not crash
        assert game.state_manager.state == config.STATE_SHOP

    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    @patch("pygame.display.flip")
    def test_draw_skills_state(self, mock_flip, mock_caption, mock_clock):
        """Test draw method in SKILLS state"""
        # Arrange
        # Create real pygame surface
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        with patch("pygame.display.set_mode", return_value=screen):
            game = Game()
            game.state_manager.state = config.STATE_SKILLS

            # Act
            game.draw()

            # Assert - should not crash and flip display
            assert game.state_manager.state == config.STATE_SKILLS
            mock_flip.assert_called()

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    @patch("pygame.display.flip")
    def test_draw_game_over_state(
        self, mock_flip, mock_caption, mock_clock, mock_display
    ):
        """Test draw method in GAME_OVER state"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_GAME_OVER

        # Act
        game.draw()

        # Assert - should not crash
        assert game.state_manager.state == config.STATE_GAME_OVER

    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_draw_game_over_screen(self, mock_caption, mock_clock):
        """Test draw_game_over_screen method"""
        # Arrange
        # Set display mode before creating game (needed for font rendering)
        pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        game = Game()

        # Act
        game.draw_game_over_screen("VICTORY!", config.GREEN)

        # Assert - should not crash
        assert game is not None

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_add_starting_items(self, mock_caption, mock_clock, mock_display):  # noqa: PBR008
        """Test _add_starting_items adds items to inventory"""
        # Arrange
        game = Game()

        # Assert - starting items should be in inventory
        # Count items in backpack and equipped slots
        total_items = sum(
            1
            for item in game.warrior.inventory.backpack_slots
            if item is not None  # noqa: PBR008
        )
        if game.warrior.inventory.weapon_slot:
            total_items += 1
        if game.warrior.inventory.armor_slot:
            total_items += 1

        assert total_items > 0
        assert game.warrior.gold == 100

        # Check for specific starting items
        item_names = []
        if game.warrior.inventory.weapon_slot:
            item_names.append(game.warrior.inventory.weapon_slot.name)
        if game.warrior.inventory.armor_slot:
            item_names.append(game.warrior.inventory.armor_slot.name)
        for item in game.warrior.inventory.backpack_slots:  # noqa: PBR008
            if item:
                item_names.append(item.name)

        assert "Short Sword" in item_names
        assert "Woolen Tunic" in item_names
        assert "Health Potion" in item_names

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_save_game_success(self, mock_caption, mock_clock, mock_display):
        """Test saving game successfully"""
        # Arrange
        game = Game()

        # Act
        result = game.save_game("test_save")

        # Assert
        assert result is True
        assert "Game saved" in game.state_manager.message

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    @patch("caislean_gaofar.systems.save_game.SaveGame.save_game", return_value=False)
    def test_save_game_failure(self, mock_save, mock_caption, mock_clock, mock_display):
        """Test save game failure"""
        # Arrange
        game = Game()

        # Act
        result = game.save_game("test_save")

        # Assert
        assert result is False
        assert "Failed to save" in game.state_manager.message

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_load_game_state(self, mock_caption, mock_clock, mock_display):
        """Test loading game state"""
        # Arrange
        game = Game()

        # Create save data
        save_data = {
            "player": {
                "grid_x": 10,
                "grid_y": 15,
                "health": 75,
                "max_health": 100,
                "gold": 500,
                "inventory": {
                    "equipped_weapon": None,
                    "equipped_armor": None,
                    "items": [],
                },
            },
            "current_map_id": "world",
            "return_location": None,
            "killed_monsters": [],
            "opened_chests": [],
            "ground_items": [],
        }

        # Act
        game.load_game_state(save_data)

        # Assert
        assert game.warrior.grid_x == 10
        assert game.warrior.grid_y == 15
        assert game.warrior.health == 75
        assert game.warrior.max_health == 100
        assert game.warrior.gold == 500
        assert game.dungeon_manager.current_map_id == "world"

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_load_game_state_with_ground_items(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test loading game state with ground items"""
        # Arrange
        game = Game()

        # Create save data with ground items
        save_data = {
            "player": {
                "grid_x": 10,
                "grid_y": 15,
                "health": 100,
                "max_health": 100,
                "gold": 100,
                "inventory": {
                    "equipped_weapon": None,
                    "equipped_armor": None,
                    "items": [],
                },
            },
            "current_map_id": "world",
            "return_location": None,
            "killed_monsters": [],
            "opened_chests": [],
            "ground_items": [
                {
                    "map_id": "world",
                    "grid_x": 5,
                    "grid_y": 5,
                    "item": {
                        "name": "Test Item",
                        "item_type": "misc",  # lowercase - matches ItemType enum
                        "description": "A test item",
                        "attack_bonus": 0,
                        "defense_bonus": 0,
                        "health_bonus": 0,
                        "gold_value": 10,
                    },
                }
            ],
        }

        # Act
        game.load_game_state(save_data)

        # Assert
        assert len(game.entity_manager.ground_items) == 1
        assert game.entity_manager.ground_items[0].grid_x == 5
        assert game.entity_manager.ground_items[0].grid_y == 5

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    @patch("pygame.quit")
    def test_run_game_loop(self, mock_quit, mock_caption, mock_clock, mock_display):
        """Test main game loop runs"""
        # Arrange
        game = Game()
        game.event_dispatcher.running = False  # Stop immediately

        # Act
        game.run()

        # Assert
        mock_quit.assert_called_once()

    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    def test_update_return_portal_collision(self, mock_caption, mock_display):  # noqa: PBR008
        """Test update handles return portal collision"""
        # Arrange
        # Create a mock clock that returns proper time
        mock_clock = MagicMock()
        mock_clock_instance = MagicMock()
        mock_clock_instance.get_time.return_value = 16  # 16 milliseconds
        mock_clock.return_value = mock_clock_instance

        with patch("pygame.time.Clock", mock_clock):
            game = Game()
            game.state_manager.state = config.STATE_PLAYING

            # Set up portal by entering dungeon and using town portal
            for spawn in game.world_map.get_entity_spawns("dungeons"):  # noqa: PBR008
                dungeon_id = spawn["id"]
                spawn_x, spawn_y = game.dungeon_manager.enter_dungeon(
                    dungeon_id, spawn["x"], spawn["y"]
                )
                game.warrior.grid_x = spawn_x
                game.warrior.grid_y = spawn_y
                game.world_map = game.dungeon_manager.get_current_map()
                break

            # Use town portal - this should create a return portal
            original_map_id = game.dungeon_manager.current_map_id
            game._handle_use_town_portal()

            # Verify we're in town now
            assert game.dungeon_manager.current_map_id == "town"

            # Test that return portal exists
            assert game.state_manager.return_portal is not None

            # Manually trigger return portal (simpler than collision detection)
            game._handle_use_return_portal()

            # Assert - should have used return portal and be back in original map
            assert game.dungeon_manager.current_map_id == original_map_id

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    @patch("pygame.event.get")
    def test_handle_events_non_skill_state(
        self, mock_event_get, mock_caption, mock_clock, mock_display
    ):
        """Test handle_events when not in SKILLS state"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_PLAYING

        # Create mock event
        mock_event = MagicMock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event.button = 1
        mock_event.pos = (100, 100)
        mock_event_get.return_value = [mock_event]

        # Act
        game.handle_events()

        # Assert - should not crash when not in SKILLS state
        assert game.state_manager.state == config.STATE_PLAYING

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_update_when_temple_is_none(self, mock_caption, mock_clock, mock_display):
        """Test update when temple is None"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_PLAYING
        game.temple = None

        # Act
        game.update(0.016)

        # Assert - should not crash
        assert game.state_manager.state == config.STATE_PLAYING

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_load_game_state_with_ground_items_on_different_map(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test loading game state with ground items on different map"""
        # Arrange
        game = Game()

        # Create save data with ground items on different map
        save_data = {
            "player": {
                "grid_x": 10,
                "grid_y": 15,
                "health": 100,
                "max_health": 100,
                "gold": 100,
                "inventory": {
                    "equipped_weapon": None,
                    "equipped_armor": None,
                    "items": [],
                },
            },
            "current_map_id": "world",
            "return_location": None,
            "killed_monsters": [],
            "opened_chests": [],
            "ground_items": [
                {
                    "map_id": "town",  # Different map
                    "grid_x": 5,
                    "grid_y": 5,
                    "item": {
                        "name": "Test Item",
                        "item_type": "misc",
                        "description": "A test item",
                        "attack_bonus": 0,
                        "defense_bonus": 0,
                        "health_bonus": 0,
                        "gold_value": 10,
                    },
                }
            ],
        }

        # Act
        game.load_game_state(save_data)

        # Assert - ground items on different map should not be loaded
        assert len(game.entity_manager.ground_items) == 0

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    @patch("pygame.event.get")
    def test_handle_events_skill_ui_non_mouse_event(
        self, mock_event_get, mock_caption, mock_clock, mock_display
    ):
        """Test handle_events with skill UI and non-mouse event"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_SKILLS

        # Create mock event that's not a mouse button
        mock_event = MagicMock()
        mock_event.type = pygame.KEYDOWN
        mock_event_get.return_value = [mock_event]

        # Act
        game.handle_events()

        # Assert - should not crash
        assert game.state_manager.state == config.STATE_SKILLS

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    @patch("pygame.event.get")
    def test_handle_events_skill_ui_middle_mouse_button(
        self, mock_event_get, mock_caption, mock_clock, mock_display
    ):
        """Test handle_events with skill UI middle mouse button"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_SKILLS

        # Create mock event with middle mouse button
        mock_event = MagicMock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event.button = 2  # Middle mouse button
        mock_event.pos = (100, 100)
        mock_event_get.return_value = [mock_event]

        # Act
        game.handle_events()

        # Assert - should not crash
        assert game.state_manager.state == config.STATE_SKILLS

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_update_with_return_portal_collision(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test update() when return portal collision is detected (lines 248-249)"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_PLAYING

        # Mock check_return_portal_collision to return True
        with patch.object(
            game.state_manager, "check_return_portal_collision", return_value=True
        ):
            # Mock _handle_use_return_portal to track if it's called
            with patch.object(game, "_handle_use_return_portal") as mock_portal:
                # Act
                game.update(0.016)

                # Assert
                mock_portal.assert_called_once()

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_check_dungeon_transition_exit_returns_none(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test _check_dungeon_transition when exit_dungeon returns None (branch 285->304)"""
        # Arrange
        game = Game()

        # Mock check_for_exit to return True
        with patch.object(game.dungeon_manager, "check_for_exit", return_value=True):
            # Mock exit_dungeon to return None
            with patch.object(game.dungeon_manager, "exit_dungeon", return_value=None):
                # Act
                game._check_dungeon_transition()

                # Assert - should continue without error
                # The code should continue to check for entering dungeon
                assert game.dungeon_manager is not None

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_check_dungeon_transition_dungeon_entry_loop_no_match(  # noqa: PBR008
        self, mock_caption, mock_clock, mock_display
    ):  # noqa: PBR008
        """Test dungeon entry loop when spawn list doesn't contain matching ID (branches 327-331)"""
        # Arrange
        game = Game()

        # Position warrior on a dungeon entrance
        for spawn in game.world_map.get_entity_spawns("dungeons"):  # noqa: PBR008
            dungeon_id = spawn["id"]
            # Enter dungeon
            spawn_x, spawn_y = game.dungeon_manager.enter_dungeon(
                dungeon_id, spawn["x"], spawn["y"]
            )
            game.warrior.grid_x = spawn_x
            game.warrior.grid_y = spawn_y
            game.world_map = game.dungeon_manager.get_current_map()
            break

        # Mock get_entity_spawns to return empty list (no matching ID)
        with patch.object(
            game.dungeon_manager.world_map,
            "get_entity_spawns",
            return_value=[],
        ):
            # Act - this should not break, loop exhausts without finding match
            game._check_dungeon_transition()

            # Assert - should not crash
            assert game.warrior is not None

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_check_dungeon_transition_dungeon_entry_loop_with_match(  # noqa: PBR008
        self, mock_caption, mock_clock, mock_display
    ):  # noqa: PBR008
        """Test dungeon entry loop when spawn ID matches (break at line 331)"""
        # Arrange
        game = Game()

        # Position warrior on a dungeon entrance
        for spawn in game.world_map.get_entity_spawns("dungeons"):  # noqa: PBR008
            game.warrior.grid_x = spawn["x"]
            game.warrior.grid_y = spawn["y"]
            break

        # Act - enter dungeon which triggers the loop and break
        game._check_dungeon_transition()

        # Assert - should have entered dungeon and found matching spawn
        assert game.dungeon_manager.current_map_id != "world"

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_use_town_portal_failure_branch(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test _handle_use_town_portal when it fails (branch 392->399)"""
        # Arrange
        game = Game()

        # Mock use_town_portal to return failure
        with patch.object(
            game.state_manager,
            "use_town_portal",
            return_value=(False, "Cannot use town portal here"),
        ):
            # Store original references
            original_world_map = game.world_map
            original_camera = game.camera

            # Act
            game._handle_use_town_portal()

            # Assert - world_map and camera should NOT be updated
            assert game.world_map is original_world_map
            assert game.camera is original_camera
            assert "Cannot use town portal here" in game.state_manager.message

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_handle_use_return_portal_returning_to_town(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test _handle_use_return_portal when returning to town (branch 413->416)"""
        # Arrange
        game = Game()

        # Mock use_return_portal to return success
        with patch.object(
            game.state_manager,
            "use_return_portal",
            return_value=(True, "Returned successfully"),
        ):
            # Set current_map_id to "town"
            game.dungeon_manager.current_map_id = "town"

            # Mock spawn_chests to track if it's called
            with patch.object(game.entity_manager, "spawn_chests") as mock_spawn:
                # Act
                game._handle_use_return_portal()

                # Assert - spawn_chests should NOT be called when in town
                mock_spawn.assert_not_called()
                assert "Returned successfully" in game.state_manager.message

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_run_method_loop_execution(self, mock_caption, mock_clock, mock_display):
        """Test run() method executes the game loop (lines 608-612)"""
        # Arrange
        game = Game()

        # Mock clock tick
        mock_clock_instance = MagicMock()
        mock_clock.return_value = mock_clock_instance
        mock_clock_instance.tick.return_value = 16  # 60 FPS = 16ms per frame

        # Track number of loop iterations
        iteration_count = [0]

        def mock_handle_events():
            iteration_count[0] += 1
            if iteration_count[0] >= 2:
                # Stop after 2 iterations
                game.event_dispatcher.running = False
            # Call original (which is also mocked)
            pass

        with patch.object(game, "handle_events", side_effect=mock_handle_events):
            with patch.object(game, "update"):
                with patch.object(game, "draw"):
                    with patch("pygame.quit"):
                        # Act
                        game.run()

                        # Assert - loop executed at least twice
                        assert iteration_count[0] == 2

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_check_dungeon_transition_no_dungeon_name_found(
        self, mock_caption, mock_clock, mock_display
    ):
        """Test dungeon entry when no matching dungeon name is found (branch 327->exit)"""
        # Arrange
        game = Game()

        # Mock dungeon_manager to simulate entering a dungeon
        with patch.object(game.dungeon_manager, "check_for_exit", return_value=False):
            with patch.object(
                game.dungeon_manager,
                "get_dungeon_at_position",
                return_value="unknown_dungeon_id",
            ):
                with patch.object(
                    game.dungeon_manager, "enter_dungeon", return_value=(5, 5)
                ):
                    # Mock entity spawning to avoid KeyError
                    with patch.object(game.entity_manager, "spawn_monsters"):
                        with patch.object(game.entity_manager, "spawn_chests"):
                            with patch.object(
                                game.entity_manager, "clear_ground_items"
                            ):
                                # Mock world_map.get_entity_spawns to return spawns that don't match
                                with patch.object(
                                    game.dungeon_manager.world_map,
                                    "get_entity_spawns",
                                    return_value=[
                                        {
                                            "id": "different_dungeon_1",
                                            "name": "Different Dungeon 1",
                                        },
                                        {
                                            "id": "different_dungeon_2",
                                            "name": "Different Dungeon 2",
                                        },
                                    ],
                                ):
                                    # Act
                                    game._check_dungeon_transition()

                                    # Assert - should complete without error (loop exits without break)
                                    # The message won't be shown since no match was found
                                    assert game.warrior.grid_x == 5
                                    assert game.warrior.grid_y == 5

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_draw_game_over_state_branch(self, mock_caption, mock_clock, mock_display):
        """Test draw() method with STATE_GAME_OVER (branch 486->exit)"""
        # Arrange
        game = Game()
        game.state_manager.state = config.STATE_GAME_OVER

        # Mock the renderer
        with patch.object(game.renderer, "draw_game_over_state") as mock_draw_game_over:
            # Act
            game.draw()

            # Assert
            mock_draw_game_over.assert_called_once_with("GAME OVER!", config.RED)

    @patch("pygame.display.set_mode")
    @patch("pygame.time.Clock")
    @patch("pygame.display.set_caption")
    def test_draw_with_unknown_state(self, mock_caption, mock_clock, mock_display):
        """Test draw() method with an unknown/unhandled state"""
        # Arrange
        game = Game()
        game.state_manager.state = 999  # Unknown state

        # Act
        game.draw()

        # Assert - should complete without error (no elif matches, just exits)
        # This tests the exit path when no state matches
