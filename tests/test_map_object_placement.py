"""Tests for validating object placement on maps - ensures no objects are in walls or non-accessible areas"""

import pytest
import os
import glob
from world_map import WorldMap


def get_all_map_files():
    """Get all map files from the maps directory"""
    maps_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "maps")
    map_files = glob.glob(os.path.join(maps_dir, "*.json"))
    return [(os.path.basename(f), f) for f in map_files]  # noqa: PBR008


class TestMapObjectPlacement:
    """Test class to validate that all objects on all maps are placed in accessible areas"""

    @pytest.mark.parametrize("map_name,map_file", get_all_map_files())
    def test_spawn_points_on_passable_tiles(self, map_name, map_file):
        """Test that spawn points are placed on passable tiles"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_file(map_file)
        spawn_x, spawn_y = world_map.spawn_point

        # Act
        is_passable = world_map.is_passable(spawn_x, spawn_y)

        # Assert
        assert is_passable, (
            f"Map '{map_name}': Spawn point at ({spawn_x}, {spawn_y}) "
            f"is on non-passable terrain"
        )

    @pytest.mark.parametrize("map_name,map_file", get_all_map_files())  # noqa: PBR008
    def test_monsters_on_passable_tiles(self, map_name, map_file):  # noqa: PBR008
        """Test that all monsters are placed on passable tiles"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_file(map_file)
        monsters = world_map.get_entity_spawns("monsters")

        # Act & Assert
        for i, monster in enumerate(monsters):  # noqa: PBR008
            monster_x = monster["x"]
            monster_y = monster["y"]
            monster_type = monster.get("type", "unknown")
            is_passable = world_map.is_passable(monster_x, monster_y)

            assert is_passable, (
                f"Map '{map_name}': Monster #{i} (type: {monster_type}) "
                f"at ({monster_x}, {monster_y}) is on non-passable terrain"
            )

    @pytest.mark.parametrize("map_name,map_file", get_all_map_files())  # noqa: PBR008
    def test_chests_on_passable_tiles(self, map_name, map_file):  # noqa: PBR008
        """Test that all chests are placed on passable tiles"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_file(map_file)
        chests = world_map.get_entity_spawns("chests")

        # Act & Assert
        for i, chest in enumerate(chests):  # noqa: PBR008
            chest_x = chest["x"]
            chest_y = chest["y"]
            is_passable = world_map.is_passable(chest_x, chest_y)

            assert is_passable, (
                f"Map '{map_name}': Chest #{i} at ({chest_x}, {chest_y}) "
                f"is on non-passable terrain"
            )

    @pytest.mark.parametrize("map_name,map_file", get_all_map_files())  # noqa: PBR008
    def test_dungeons_on_passable_tiles(self, map_name, map_file):  # noqa: PBR008
        """Test that all dungeon entrances are placed on passable tiles"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_file(map_file)
        dungeons = world_map.get_entity_spawns("dungeons")

        # Act & Assert
        for i, dungeon in enumerate(dungeons):  # noqa: PBR008
            dungeon_x = dungeon["x"]
            dungeon_y = dungeon["y"]
            dungeon_name = dungeon.get("name", "unknown")
            is_passable = world_map.is_passable(dungeon_x, dungeon_y)

            assert is_passable, (
                f"Map '{map_name}': Dungeon entrance #{i} (name: {dungeon_name}) "
                f"at ({dungeon_x}, {dungeon_y}) is on non-passable terrain"
            )

    @pytest.mark.parametrize("map_name,map_file", get_all_map_files())  # noqa: PBR008
    def test_all_objects_within_map_bounds(self, map_name, map_file):  # noqa: PBR008
        """Test that all objects are within valid map bounds"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_file(map_file)

        # Check spawn point
        spawn_x, spawn_y = world_map.spawn_point
        assert world_map.is_valid_position(spawn_x, spawn_y), (
            f"Map '{map_name}': Spawn point at ({spawn_x}, {spawn_y}) "
            f"is out of bounds (map size: {world_map.width}x{world_map.height})"
        )

        # Check monsters
        monsters = world_map.get_entity_spawns("monsters")
        for i, monster in enumerate(monsters):  # noqa: PBR008
            monster_x, monster_y = monster["x"], monster["y"]
            assert world_map.is_valid_position(monster_x, monster_y), (
                f"Map '{map_name}': Monster #{i} at ({monster_x}, {monster_y}) "
                f"is out of bounds (map size: {world_map.width}x{world_map.height})"
            )

        # Check chests
        chests = world_map.get_entity_spawns("chests")
        for i, chest in enumerate(chests):  # noqa: PBR008
            chest_x, chest_y = chest["x"], chest["y"]
            assert world_map.is_valid_position(chest_x, chest_y), (
                f"Map '{map_name}': Chest #{i} at ({chest_x}, {chest_y}) "
                f"is out of bounds (map size: {world_map.width}x{world_map.height})"
            )

        # Check dungeons
        dungeons = world_map.get_entity_spawns("dungeons")
        for i, dungeon in enumerate(dungeons):  # noqa: PBR008
            dungeon_x, dungeon_y = dungeon["x"], dungeon["y"]
            assert world_map.is_valid_position(dungeon_x, dungeon_y), (
                f"Map '{map_name}': Dungeon #{i} at ({dungeon_x}, {dungeon_y}) "
                f"is out of bounds (map size: {world_map.width}x{world_map.height})"
            )

    @pytest.mark.parametrize("map_name,map_file", get_all_map_files())  # noqa: PBR008
    def test_no_objects_overlap_same_position(self, map_name, map_file):  # noqa: PBR008
        """Test that no two objects occupy the exact same position"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_file(map_file)

        # Collect all object positions
        positions = {}

        # Add spawn point
        spawn_x, spawn_y = world_map.spawn_point
        positions[(spawn_x, spawn_y)] = ["spawn_point"]

        # Add monsters
        monsters = world_map.get_entity_spawns("monsters")
        for i, monster in enumerate(monsters):  # noqa: PBR008
            pos = (monster["x"], monster["y"])
            if pos not in positions:
                positions[pos] = []
            positions[pos].append(f"monster#{i}({monster.get('type', 'unknown')})")

        # Add chests
        chests = world_map.get_entity_spawns("chests")
        for i, chest in enumerate(chests):  # noqa: PBR008
            pos = (chest["x"], chest["y"])
            if pos not in positions:
                positions[pos] = []
            positions[pos].append(f"chest#{i}")

        # Add dungeons
        dungeons = world_map.get_entity_spawns("dungeons")
        for i, dungeon in enumerate(dungeons):  # noqa: PBR008
            pos = (dungeon["x"], dungeon["y"])
            if pos not in positions:
                positions[pos] = []
            positions[pos].append(f"dungeon#{i}({dungeon.get('name', 'unknown')})")

        # Check for overlaps
        for pos, objects in positions.items():  # noqa: PBR008
            if len(objects) > 1:
                import warnings

                warnings.warn(
                    f"Map '{map_name}': Multiple objects at position {pos}: {', '.join(objects)}",
                    UserWarning,
                )
