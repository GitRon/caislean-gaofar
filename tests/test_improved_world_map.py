"""
Tests for the improved world map features including:
- Tree terrain (impassible)
- Ghost village area
- Forest with paths
- Additional dungeons and chests
"""

import pytest
from world_map import WorldMap


class TestImprovedWorldMap:
    """Test suite for improved world map features"""

    @pytest.fixture
    def overworld_map(self):
        """Load the overworld map for testing"""
        world_map = WorldMap()
        world_map.load_from_file("maps/overworld.json")
        return world_map

    def test_tree_terrain_exists(self, overworld_map):  # noqa: PBR008
        """Test that tree terrain ('T') exists on the map"""
        # Arrange & Act
        trees_found = False
        for row in overworld_map.tiles:  # noqa: PBR008
            if "T" in row:
                trees_found = True
                break

        # Assert
        assert trees_found, "No tree terrain found on the map"

    def test_tree_terrain_is_impassable(self, overworld_map):  # noqa: PBR008
        """Test that tree terrain is impassable"""
        # Arrange - Find a tree tile
        tree_x, tree_y = None, None
        for y, row in enumerate(overworld_map.tiles):  # noqa: PBR008
            for x, tile in enumerate(row):  # noqa: PBR008
                if tile == "T":
                    tree_x, tree_y = x, y
                    break
            if tree_x is not None:
                break

        # Act
        assert tree_x is not None, "No tree found to test"
        is_passable = overworld_map.is_passable(tree_x, tree_y)

        # Assert
        assert not is_passable, f"Tree at ({tree_x}, {tree_y}) should be impassable"

    def test_ghost_village_ground_exists(self, overworld_map):  # noqa: PBR008
        """Test that ghost village ground ('G') exists on the map"""
        # Arrange & Act
        ghost_ground_found = False
        for row in overworld_map.tiles:  # noqa: PBR008
            if "G" in row:
                ghost_ground_found = True
                break

        # Assert
        assert ghost_ground_found, "No ghost village ground found on the map"

    def test_ghost_village_ground_is_passable(self, overworld_map):  # noqa: PBR008
        """Test that ghost village ground is passable"""
        # Arrange - Find a ghost village ground tile
        ghost_x, ghost_y = None, None
        for y, row in enumerate(overworld_map.tiles):  # noqa: PBR008
            for x, tile in enumerate(row):  # noqa: PBR008
                if tile == "G":
                    ghost_x, ghost_y = x, y
                    break
            if ghost_x is not None:
                break

        # Act
        assert ghost_x is not None, "No ghost village ground found to test"
        is_passable = overworld_map.is_passable(ghost_x, ghost_y)

        # Assert
        assert is_passable, (
            f"Ghost village ground at ({ghost_x}, {ghost_y}) should be passable"
        )

    def test_minimum_dungeon_count(self, overworld_map):
        """Test that overworld has at least 7 dungeons"""
        # Arrange & Act
        dungeons = overworld_map.get_entity_spawns("dungeons")

        # Assert
        assert len(dungeons) >= 7, (
            f"Expected at least 7 dungeons, found {len(dungeons)}"
        )

    def test_all_dungeons_have_required_fields(self, overworld_map):  # noqa: PBR008
        """Test that all dungeons have x, y, name, and id fields"""
        # Arrange & Act
        dungeons = overworld_map.get_entity_spawns("dungeons")

        # Assert
        for i, dungeon in enumerate(dungeons):  # noqa: PBR008
            assert "x" in dungeon, f"Dungeon #{i} missing 'x' field"
            assert "y" in dungeon, f"Dungeon #{i} missing 'y' field"
            assert "name" in dungeon, f"Dungeon #{i} missing 'name' field"
            assert "id" in dungeon, f"Dungeon #{i} missing 'id' field"
            assert isinstance(dungeon["name"], str), (
                f"Dungeon #{i} name should be string"
            )
            assert isinstance(dungeon["id"], str), f"Dungeon #{i} id should be string"
            assert len(dungeon["name"]) > 0, f"Dungeon #{i} name should not be empty"
            assert len(dungeon["id"]) > 0, f"Dungeon #{i} id should not be empty"

    def test_minimum_chest_count(self, overworld_map):
        """Test that overworld has at least 10 chests"""
        # Arrange & Act
        chests = overworld_map.get_entity_spawns("chests")

        # Assert
        assert len(chests) >= 10, f"Expected at least 10 chests, found {len(chests)}"

    def test_minimum_monster_count(self, overworld_map):
        """Test that overworld has at least 10 monsters"""
        # Arrange & Act
        monsters = overworld_map.get_entity_spawns("monsters")

        # Assert
        assert len(monsters) >= 10, (
            f"Expected at least 10 monsters, found {len(monsters)}"
        )

    def test_forest_area_has_trees(self, overworld_map):  # noqa: PBR008
        """Test that there are connected tree areas (forest)"""
        # Arrange & Act
        tree_count = 0
        for row in overworld_map.tiles:  # noqa: PBR008
            tree_count += row.count("T")

        # Assert
        assert tree_count >= 20, (
            f"Expected at least 20 tree tiles for a forest, found {tree_count}"
        )

    def test_ghost_village_has_structures(self, overworld_map):  # noqa: PBR008
        """Test that ghost village area has stone structures"""
        # Arrange - Find ghost village area (where G exists)
        ghost_area_rows = []
        for y, row in enumerate(overworld_map.tiles):  # noqa: PBR008
            if "G" in row:
                ghost_area_rows.append(y)

        # Act - Check if there are stone structures (#) near ghost village ground
        assert len(ghost_area_rows) > 0, "No ghost village area found"

        has_structures = False
        for y in ghost_area_rows:  # noqa: PBR008
            row = overworld_map.tiles[y]
            if "#" in row:
                has_structures = True
                break

        # Assert
        assert has_structures, "Ghost village should have stone structures"

    def test_dungeon_names_are_unique(self, overworld_map):  # noqa: PBR008
        """Test that all dungeon names are unique"""
        # Arrange & Act
        dungeons = overworld_map.get_entity_spawns("dungeons")
        names = [d["name"] for d in dungeons]

        # Assert
        assert len(names) == len(set(names)), (
            f"Dungeon names should be unique. Found duplicates: "
            f"{[name for name in names if names.count(name) > 1]}"
        )

    def test_dungeon_ids_are_unique(self, overworld_map):  # noqa: PBR008
        """Test that all dungeon IDs are unique"""
        # Arrange & Act
        dungeons = overworld_map.get_entity_spawns("dungeons")
        ids = [d["id"] for d in dungeons]

        # Assert
        assert len(ids) == len(set(ids)), (
            f"Dungeon IDs should be unique. Found duplicates: "
            f"{[id for id in ids if ids.count(id) > 1]}"
        )

    def test_terrain_legend_contains_new_types(self, overworld_map):
        """Test that terrain legend includes tree and ghost village ground"""
        # Arrange & Act
        terrain_manager = overworld_map.terrain_manager

        # Assert
        assert terrain_manager.get_terrain("T") is not None, (
            "Terrain legend should contain 'T' for trees"
        )
        assert terrain_manager.get_terrain("G") is not None, (
            "Terrain legend should contain 'G' for ghost village ground"
        )

    def test_tree_terrain_has_correct_properties(self, overworld_map):
        """Test that tree terrain has correct name, passable status, and color"""
        # Arrange & Act
        terrain_manager = overworld_map.terrain_manager
        tree_terrain = terrain_manager.get_terrain("T")

        # Assert
        assert tree_terrain is not None, "Tree terrain should exist"
        assert tree_terrain.name == "tree", (
            f"Tree terrain name should be 'tree', got '{tree_terrain.name}'"
        )
        assert not tree_terrain.passable, "Tree terrain should not be passable"
        assert tree_terrain.color is not None, "Tree terrain should have a color"
        assert len(tree_terrain.color) == 3, "Tree terrain color should be RGB tuple"

    def test_ghost_village_ground_has_correct_properties(self, overworld_map):
        """Test that ghost village ground has correct name, passable status, and color"""
        # Arrange & Act
        terrain_manager = overworld_map.terrain_manager
        ghost_ground = terrain_manager.get_terrain("G")

        # Assert
        assert ghost_ground is not None, "Ghost village ground should exist"
        assert ghost_ground.name == "ghost_village_ground", (
            f"Ghost village ground name should be 'ghost_village_ground', got '{ghost_ground.name}'"
        )
        assert ghost_ground.passable, "Ghost village ground should be passable"
        assert ghost_ground.color is not None, (
            "Ghost village ground should have a color"
        )
        assert len(ghost_ground.color) == 3, (
            "Ghost village ground color should be RGB tuple"
        )

    def test_chests_are_strategically_placed(self, overworld_map):  # noqa: PBR008
        """Test that chests are not all clustered in one area"""
        # Arrange & Act
        chests = overworld_map.get_entity_spawns("chests")

        # Calculate distribution across quadrants
        quadrant_counts = {"nw": 0, "ne": 0, "sw": 0, "se": 0}
        mid_x = overworld_map.width // 2
        mid_y = overworld_map.height // 2

        for chest in chests:  # noqa: PBR008
            x, y = chest["x"], chest["y"]
            if x < mid_x and y < mid_y:
                quadrant_counts["nw"] += 1
            elif x >= mid_x and y < mid_y:
                quadrant_counts["ne"] += 1
            elif x < mid_x and y >= mid_y:
                quadrant_counts["sw"] += 1
            else:
                quadrant_counts["se"] += 1

        # Assert - At least 2 quadrants should have chests
        quadrants_with_chests = sum(
            1 for count in quadrant_counts.values() if count > 0
        )
        assert quadrants_with_chests >= 2, (
            f"Chests should be distributed across at least 2 quadrants. "
            f"Distribution: {quadrant_counts}"
        )

    def test_monsters_are_distributed(self, overworld_map):  # noqa: PBR008
        """Test that monsters are distributed across the map"""
        # Arrange & Act
        monsters = overworld_map.get_entity_spawns("monsters")

        # Calculate distribution across quadrants
        quadrant_counts = {"nw": 0, "ne": 0, "sw": 0, "se": 0}
        mid_x = overworld_map.width // 2
        mid_y = overworld_map.height // 2

        for monster in monsters:  # noqa: PBR008
            x, y = monster["x"], monster["y"]
            if x < mid_x and y < mid_y:
                quadrant_counts["nw"] += 1
            elif x >= mid_x and y < mid_y:
                quadrant_counts["ne"] += 1
            elif x < mid_x and y >= mid_y:
                quadrant_counts["sw"] += 1
            else:
                quadrant_counts["se"] += 1

        # Assert - At least 3 quadrants should have monsters
        quadrants_with_monsters = sum(
            1 for count in quadrant_counts.values() if count > 0
        )
        assert quadrants_with_monsters >= 3, (
            f"Monsters should be distributed across at least 3 quadrants. "
            f"Distribution: {quadrant_counts}"
        )
