"""Tests for dungeon_transition_manager.py"""

from unittest.mock import MagicMock, patch
import pygame
from caislean_gaofar.world.dungeon_transition_manager import DungeonTransitionManager
from caislean_gaofar.world.camera import Camera
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.entities.entity_manager import EntityManager
from caislean_gaofar.world.dungeon_manager import DungeonManager
from caislean_gaofar.core import config
import os

# Initialize pygame
pygame.init()


class TestDungeonTransitionManager:
    """Tests for DungeonTransitionManager class"""

    def test_check_and_handle_transition_no_transition(self):
        """Test when no transition occurs"""
        # Arrange
        manager = DungeonTransitionManager()
        warrior = Warrior(5, 5)
        entity_manager = EntityManager()

        # Create dungeon manager with world map
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()

        on_camera_update = MagicMock(return_value=Camera(100, 100))
        on_message = MagicMock()

        # Act
        new_camera, transition_occurred = manager.check_and_handle_transition(
            warrior=warrior,
            dungeon_manager=dungeon_manager,
            entity_manager=entity_manager,
            on_camera_update=on_camera_update,
            on_message=on_message,
        )

        # Assert
        assert new_camera is None
        assert transition_occurred is False
        on_camera_update.assert_not_called()
        on_message.assert_not_called()

    def test_check_and_handle_transition_entering_dungeon(self):  # noqa: PBR008
        """Test entering a dungeon"""
        # Arrange
        manager = DungeonTransitionManager()
        warrior = Warrior(5, 5)
        entity_manager = EntityManager()

        # Create dungeon manager with world map
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()

        # Load a dungeon using the actual ID from the spawn
        dark_cave_path = config.resource_path(
            os.path.join("data", "maps", "dark_cave.json")
        )

        # Get the first dungeon spawn and load it
        dungeon_spawns = dungeon_manager.world_map.get_entity_spawns("dungeons")
        first_spawn = dungeon_spawns[0]
        dungeon_id = first_spawn["id"]
        dungeon_manager.load_dungeon(dungeon_id, dark_cave_path)
        warrior.grid_x = first_spawn["x"]
        warrior.grid_y = first_spawn["y"]

        on_camera_update = MagicMock(return_value=Camera(100, 100))
        on_message = MagicMock()

        # Act
        new_camera, transition_occurred = manager.check_and_handle_transition(
            warrior=warrior,
            dungeon_manager=dungeon_manager,
            entity_manager=entity_manager,
            on_camera_update=on_camera_update,
            on_message=on_message,
        )

        # Assert
        assert new_camera is not None
        assert transition_occurred is True
        on_camera_update.assert_called_once()
        on_message.assert_called_once()
        assert "enter" in on_message.call_args[0][0].lower()

    def test_check_and_handle_transition_exiting_dungeon(self):  # noqa: PBR008
        """Test exiting a dungeon"""
        # Arrange
        manager = DungeonTransitionManager()
        warrior = Warrior(5, 5)
        entity_manager = EntityManager()

        # Create dungeon manager with world map
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()

        # Load a dungeon using the actual ID from the spawn
        dark_cave_path = config.resource_path(
            os.path.join("data", "maps", "dark_cave.json")
        )

        # Enter dungeon first - use actual spawn ID
        dungeon_spawns = dungeon_manager.world_map.get_entity_spawns("dungeons")
        first_spawn = dungeon_spawns[0]
        dungeon_id = first_spawn["id"]
        dungeon_manager.load_dungeon(dungeon_id, dark_cave_path)
        spawn_x, spawn_y = dungeon_manager.enter_dungeon(
            dungeon_id, first_spawn["x"], first_spawn["y"]
        )
        warrior.grid_x = spawn_x
        warrior.grid_y = spawn_y

        # Position warrior on exit (1,1 in dark_cave.json)
        warrior.grid_x = 1
        warrior.grid_y = 1

        on_camera_update = MagicMock(return_value=Camera(100, 100))
        on_message = MagicMock()

        # Act
        new_camera, transition_occurred = manager.check_and_handle_transition(
            warrior=warrior,
            dungeon_manager=dungeon_manager,
            entity_manager=entity_manager,
            on_camera_update=on_camera_update,
            on_message=on_message,
        )

        # Assert
        assert new_camera is not None
        assert transition_occurred is True
        on_camera_update.assert_called_once()
        on_message.assert_called_once()
        assert "return" in on_message.call_args[0][0].lower()

    def test_handle_dungeon_exit_with_no_return_position(self):
        """Test exiting dungeon when exit_dungeon returns None"""
        # Arrange
        manager = DungeonTransitionManager()
        warrior = Warrior(5, 5)
        entity_manager = EntityManager()

        # Mock dungeon manager
        dungeon_manager = MagicMock()
        dungeon_manager.exit_dungeon.return_value = None

        on_camera_update = MagicMock()
        on_message = MagicMock()

        # Act
        new_camera, transition_occurred = manager._handle_dungeon_exit(
            warrior=warrior,
            dungeon_manager=dungeon_manager,
            entity_manager=entity_manager,
            on_camera_update=on_camera_update,
            on_message=on_message,
        )

        # Assert
        assert new_camera is None
        assert transition_occurred is False
        on_camera_update.assert_not_called()
        on_message.assert_not_called()

    def test_handle_dungeon_entry_without_matching_spawn_name(self):
        """Test entering dungeon when spawn list doesn't contain matching ID"""
        # Arrange
        manager = DungeonTransitionManager()
        warrior = Warrior(5, 5)
        entity_manager = EntityManager()

        # Create dungeon manager with world map
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()

        # Load a dungeon
        dark_cave_path = config.resource_path(
            os.path.join("data", "maps", "dark_cave.json")
        )
        dungeon_manager.load_dungeon("unknown_dungeon_id", dark_cave_path)

        on_camera_update = MagicMock(return_value=Camera(100, 100))
        on_message = MagicMock()

        # Mock get_entity_spawns to return empty list
        with patch.object(
            dungeon_manager.world_map,
            "get_entity_spawns",
            return_value=[],
        ):
            # Act
            new_camera, transition_occurred = manager._handle_dungeon_entry(
                warrior=warrior,
                dungeon_manager=dungeon_manager,
                entity_manager=entity_manager,
                on_camera_update=on_camera_update,
                on_message=on_message,
                dungeon_id="unknown_dungeon_id",
                player_x=5,
                player_y=5,
            )

        # Assert
        assert new_camera is not None
        assert transition_occurred is True
        on_camera_update.assert_called_once()
        # on_message should not be called when no matching spawn is found
        on_message.assert_not_called()

    def test_check_and_handle_transition_entering_town(self):
        """Test entering town from world map"""
        # Arrange
        manager = DungeonTransitionManager()
        warrior = Warrior(8, 5)  # Town entrance position
        entity_manager = EntityManager()

        # Create dungeon manager with world map
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()

        # Load town map
        town_path = config.resource_path(os.path.join("data", "maps", "town.json"))
        dungeon_manager.load_dungeon("town", town_path)

        on_camera_update = MagicMock(return_value=Camera(100, 100))
        on_message = MagicMock()

        # Act
        new_camera, transition_occurred = manager.check_and_handle_transition(
            warrior=warrior,
            dungeon_manager=dungeon_manager,
            entity_manager=entity_manager,
            on_camera_update=on_camera_update,
            on_message=on_message,
        )

        # Assert
        assert new_camera is not None
        assert transition_occurred is True
        on_camera_update.assert_called_once()
        on_message.assert_called_once()
        assert "town" in on_message.call_args[0][0].lower()
        assert dungeon_manager.current_map_id == "town"
        assert len(entity_manager.monsters) == 0  # Town is safe

    def test_check_and_handle_transition_exiting_town(self):
        """Test exiting town to world map"""
        # Arrange
        manager = DungeonTransitionManager()
        warrior = Warrior(7, 6)  # Town exit position
        entity_manager = EntityManager()

        # Create dungeon manager with world map
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()

        # Load town map
        town_path = config.resource_path(os.path.join("data", "maps", "town.json"))
        dungeon_manager.load_dungeon("town", town_path)

        # Enter town first
        dungeon_manager.enter_town(8, 5)
        warrior.grid_x = 7
        warrior.grid_y = 6

        on_camera_update = MagicMock(return_value=Camera(100, 100))
        on_message = MagicMock()

        # Act
        new_camera, transition_occurred = manager.check_and_handle_transition(
            warrior=warrior,
            dungeon_manager=dungeon_manager,
            entity_manager=entity_manager,
            on_camera_update=on_camera_update,
            on_message=on_message,
        )

        # Assert
        assert new_camera is not None
        assert transition_occurred is True
        on_camera_update.assert_called_once()
        on_message.assert_called_once()
        assert "wilderness" in on_message.call_args[0][0].lower()
        assert dungeon_manager.current_map_id == "world"

    def test_handle_town_exit_with_no_return_position(self):
        """Test exiting town when exit_town returns None"""
        # Arrange
        manager = DungeonTransitionManager()
        warrior = Warrior(5, 5)
        entity_manager = EntityManager()

        # Mock dungeon manager
        dungeon_manager = MagicMock()
        dungeon_manager.exit_town.return_value = None

        on_camera_update = MagicMock()
        on_message = MagicMock()

        # Act
        new_camera, transition_occurred = manager._handle_town_exit(
            warrior=warrior,
            dungeon_manager=dungeon_manager,
            entity_manager=entity_manager,
            on_camera_update=on_camera_update,
            on_message=on_message,
        )

        # Assert
        assert new_camera is None
        assert transition_occurred is False
        on_camera_update.assert_not_called()
        on_message.assert_not_called()
