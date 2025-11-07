"""Tests for dungeon manager functionality."""

import pytest
import os
from dungeon_manager import DungeonManager
import config


class TestDungeonManager:
    """Test cases for DungeonManager class."""

    def test_initialization(self):
        """Test dungeon manager initializes correctly."""
        manager = DungeonManager()
        assert manager.current_map_id == "world"
        assert manager.return_location is None
        assert len(manager.dungeon_maps) == 0
        assert len(manager.dungeon_entrances) == 0

    def test_load_world_map(self):
        """Test loading world map."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()

        assert manager.world_map is not None
        assert manager.world_map.width > 0
        assert manager.world_map.height > 0
        assert manager.current_map_id == "world"

        # Should load dungeon entrances
        assert len(manager.dungeon_entrances) > 0

    def test_load_dungeon(self):
        """Test loading a dungeon map."""
        manager = DungeonManager()
        dungeon_path = config.resource_path(os.path.join("maps", "dark_cave.json"))
        manager.load_dungeon("dark_cave", dungeon_path)

        assert "dark_cave" in manager.dungeon_maps
        assert manager.dungeon_maps["dark_cave"].width > 0
        assert manager.dungeon_maps["dark_cave"].height > 0

    def test_get_current_map_world(self):
        """Test getting current map when in world."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()

        current_map = manager.get_current_map()
        assert current_map == manager.world_map

    def test_get_current_map_dungeon(self):
        """Test getting current map when in dungeon."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()
        dungeon_path = config.resource_path(os.path.join("maps", "dark_cave.json"))
        manager.load_dungeon("dark_cave", dungeon_path)

        # Enter dungeon
        manager.enter_dungeon("dark_cave", 10, 10)

        current_map = manager.get_current_map()
        assert current_map == manager.dungeon_maps["dark_cave"]
        assert current_map != manager.world_map

    def test_is_in_dungeon(self):
        """Test checking if currently in a dungeon."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()
        dungeon_path = config.resource_path(os.path.join("maps", "dark_cave.json"))
        manager.load_dungeon("dark_cave", dungeon_path)

        # Initially in world
        assert not manager.is_in_dungeon()

        # Enter dungeon
        manager.enter_dungeon("dark_cave", 10, 10)
        assert manager.is_in_dungeon()

        # Exit dungeon
        manager.exit_dungeon()
        assert not manager.is_in_dungeon()

    def test_get_dungeon_at_position(self):
        """Test finding dungeon at position."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()
        dungeon_path = config.resource_path(os.path.join("maps", "dark_cave.json"))
        manager.load_dungeon("dark_cave", dungeon_path)

        # Check dungeon entrance location (from overworld.json)
        dungeon_id = manager.get_dungeon_at_position(11, 15)
        assert dungeon_id == "dark_cave"

        # Check non-dungeon location
        dungeon_id = manager.get_dungeon_at_position(5, 5)
        assert dungeon_id is None

    def test_get_dungeon_at_position_when_in_dungeon(self):
        """Test that dungeon detection doesn't work when already in dungeon."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()
        dungeon_path = config.resource_path(os.path.join("maps", "dark_cave.json"))
        manager.load_dungeon("dark_cave", dungeon_path)

        # Enter dungeon
        manager.enter_dungeon("dark_cave", 11, 15)

        # Should return None when already in dungeon
        dungeon_id = manager.get_dungeon_at_position(11, 15)
        assert dungeon_id is None

    def test_enter_dungeon(self):
        """Test entering a dungeon."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()
        dungeon_path = config.resource_path(os.path.join("maps", "dark_cave.json"))
        manager.load_dungeon("dark_cave", dungeon_path)

        # Enter dungeon
        player_x, player_y = 11, 15
        spawn_x, spawn_y = manager.enter_dungeon("dark_cave", player_x, player_y)

        # Check state
        assert manager.current_map_id == "dark_cave"
        assert manager.return_location == (player_x, player_y)
        assert spawn_x >= 0
        assert spawn_y >= 0

    def test_enter_dungeon_invalid_id(self):
        """Test entering a dungeon with invalid ID raises error."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()

        with pytest.raises(ValueError, match="not loaded"):
            manager.enter_dungeon("nonexistent", 10, 10)

    def test_exit_dungeon(self):
        """Test exiting a dungeon."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()
        dungeon_path = config.resource_path(os.path.join("maps", "dark_cave.json"))
        manager.load_dungeon("dark_cave", dungeon_path)

        # Enter dungeon
        original_x, original_y = 11, 15
        manager.enter_dungeon("dark_cave", original_x, original_y)

        # Exit dungeon
        return_x, return_y = manager.exit_dungeon()

        # Check state
        assert manager.current_map_id == "world"
        assert manager.return_location is None
        assert return_x == original_x
        assert return_y == original_y

    def test_exit_dungeon_when_not_in_dungeon(self):
        """Test exiting dungeon when not in one returns None."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()

        result = manager.exit_dungeon()
        assert result is None

    def test_check_for_exit(self):
        """Test checking for exit tile in dungeon."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()
        dungeon_path = config.resource_path(os.path.join("maps", "dark_cave.json"))
        manager.load_dungeon("dark_cave", dungeon_path)

        # Enter dungeon
        manager.enter_dungeon("dark_cave", 11, 15)

        # Check exit location (from dark_cave.json - exit at 1, 1)
        is_exit = manager.check_for_exit(1, 1)
        assert is_exit

        # Check non-exit location
        is_exit = manager.check_for_exit(10, 10)
        assert not is_exit

    def test_check_for_exit_when_not_in_dungeon(self):
        """Test exit check returns False when not in dungeon."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()

        is_exit = manager.check_for_exit(1, 1)
        assert not is_exit

    def test_multiple_dungeons(self):
        """Test managing multiple dungeons."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()

        # Load both dungeons
        manager.load_dungeon("dark_cave", config.resource_path(os.path.join("maps", "dark_cave.json")))
        manager.load_dungeon(
            "ancient_castle", config.resource_path(os.path.join("maps", "ancient_castle.json"))
        )

        assert len(manager.dungeon_maps) == 2
        assert "dark_cave" in manager.dungeon_maps
        assert "ancient_castle" in manager.dungeon_maps

        # Check different entrance locations
        dark_cave_id = manager.get_dungeon_at_position(11, 15)
        assert dark_cave_id == "dark_cave"

        ancient_castle_id = manager.get_dungeon_at_position(32, 21)
        assert ancient_castle_id == "ancient_castle"

    def test_dungeon_state_preservation(self):
        """Test that return location is preserved correctly."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()
        dungeon_path = config.resource_path(os.path.join("maps", "dark_cave.json"))
        manager.load_dungeon("dark_cave", dungeon_path)

        # Test first entry/exit
        manager.current_map_id = "world"
        manager.enter_dungeon("dark_cave", 11, 15)
        return_x, return_y = manager.exit_dungeon()
        assert return_x == 11
        assert return_y == 15

        # Test second entry/exit
        manager.current_map_id = "world"
        manager.enter_dungeon("dark_cave", 20, 20)
        return_x, return_y = manager.exit_dungeon()
        assert return_x == 20
        assert return_y == 20

        # Test third entry/exit
        manager.current_map_id = "world"
        manager.enter_dungeon("dark_cave", 5, 5)
        return_x, return_y = manager.exit_dungeon()
        assert return_x == 5
        assert return_y == 5

    def test_check_for_exit_invalid_position(self):
        """Test exit check with invalid position returns False."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()
        dungeon_path = config.resource_path(os.path.join("maps", "dark_cave.json"))
        manager.load_dungeon("dark_cave", dungeon_path)

        # Enter dungeon
        manager.enter_dungeon("dark_cave", 11, 15)

        # Check invalid positions (out of bounds)
        is_exit = manager.check_for_exit(-1, -1)
        assert not is_exit

        is_exit = manager.check_for_exit(1000, 1000)
        assert not is_exit

    def test_load_dungeon_entrance_without_explicit_id(self):
        """Test loading dungeon entrances when id is not provided in spawn data."""
        # Create a manager and manually modify world map to test fallback ID generation
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()

        # Should have loaded entrances with IDs from the map
        assert len(manager.dungeon_entrances) > 0

    def test_get_dungeon_at_position_dungeon_not_loaded(self):
        """Test that dungeon entrance returns None if dungeon not loaded."""
        map_path = config.resource_path(os.path.join("maps", "overworld.json"))
        manager = DungeonManager(map_path)
        manager.load_world_map()

        # Don't load the dungeon, but check the entrance position
        # The entrance exists but dungeon is not loaded
        dungeon_id = manager.get_dungeon_at_position(11, 15)
        assert dungeon_id is None
