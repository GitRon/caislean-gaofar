"""Tests for terrain.py - Terrain system"""

import pytest
from terrain import TerrainType, TerrainManager


class TestTerrainType:
    """Tests for TerrainType dataclass"""

    def test_terrain_type_initialization(self):
        """Test TerrainType initialization"""
        # Arrange & Act
        terrain = TerrainType(
            name="meadow", character=".", passable=True, color=(50, 220, 50)
        )

        # Assert
        assert terrain.name == "meadow"
        assert terrain.character == "."
        assert terrain.passable is True
        assert terrain.color == (50, 220, 50)

    def test_terrain_type_hashable(self):
        """Test TerrainType is hashable"""
        # Arrange
        terrain1 = TerrainType(
            name="meadow", character=".", passable=True, color=(50, 220, 50)
        )
        terrain2 = TerrainType(
            name="stone", character="#", passable=False, color=(128, 128, 128)
        )

        # Act & Assert
        terrain_map = {terrain1: "grass", terrain2: "wall"}
        assert terrain_map[terrain1] == "grass"
        assert terrain_map[terrain2] == "wall"


class TestTerrainManager:
    """Tests for TerrainManager class"""

    def test_terrain_manager_initialization(self):
        """Test TerrainManager initialization"""
        # Arrange & Act
        manager = TerrainManager()

        # Assert
        assert manager.terrain_types == {}

    def test_load_from_legend_single_terrain(self):
        """Test loading single terrain type from legend"""
        # Arrange
        manager = TerrainManager()
        legend = {".": {"name": "meadow", "passable": True, "color": [50, 220, 50]}}

        # Act
        manager.load_from_legend(legend)

        # Assert
        assert len(manager.terrain_types) == 1
        assert "." in manager.terrain_types
        terrain = manager.terrain_types["."]
        assert terrain.name == "meadow"
        assert terrain.passable is True
        assert terrain.color == (50, 220, 50)

    def test_load_from_legend_multiple_terrains(self):
        """Test loading multiple terrain types from legend"""
        # Arrange
        manager = TerrainManager()
        legend = {
            ".": {"name": "meadow", "passable": True, "color": [50, 220, 50]},
            "#": {"name": "stone", "passable": False, "color": [128, 128, 128]},
            "~": {"name": "water", "passable": False, "color": [50, 50, 220]},
        }

        # Act
        manager.load_from_legend(legend)

        # Assert
        assert len(manager.terrain_types) == 3
        assert "." in manager.terrain_types
        assert "#" in manager.terrain_types
        assert "~" in manager.terrain_types

    def test_get_terrain_valid_character(self):
        """Test getting terrain by valid character"""
        # Arrange
        manager = TerrainManager()
        legend = {".": {"name": "meadow", "passable": True, "color": [50, 220, 50]}}
        manager.load_from_legend(legend)

        # Act
        terrain = manager.get_terrain(".")

        # Assert
        assert terrain.name == "meadow"
        assert terrain.character == "."

    def test_get_terrain_invalid_character(self):
        """Test getting terrain with invalid character raises ValueError"""
        # Arrange
        manager = TerrainManager()
        legend = {".": {"name": "meadow", "passable": True, "color": [50, 220, 50]}}
        manager.load_from_legend(legend)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            manager.get_terrain("X")

        assert "Unknown terrain character: 'X'" in str(exc_info.value)

    def test_is_passable_true(self):
        """Test is_passable returns True for passable terrain"""
        # Arrange
        manager = TerrainManager()
        legend = {".": {"name": "meadow", "passable": True, "color": [50, 220, 50]}}
        manager.load_from_legend(legend)

        # Act
        result = manager.is_passable(".")

        # Assert
        assert result is True

    def test_is_passable_false(self):
        """Test is_passable returns False for impassable terrain"""
        # Arrange
        manager = TerrainManager()
        legend = {"#": {"name": "stone", "passable": False, "color": [128, 128, 128]}}
        manager.load_from_legend(legend)

        # Act
        result = manager.is_passable("#")

        # Assert
        assert result is False

    def test_load_from_legend_replaces_existing(self):
        """Test loading legend replaces existing terrain types"""
        # Arrange
        manager = TerrainManager()
        legend1 = {".": {"name": "meadow", "passable": True, "color": [50, 220, 50]}}
        legend2 = {"#": {"name": "stone", "passable": False, "color": [128, 128, 128]}}
        manager.load_from_legend(legend1)

        # Act
        manager.load_from_legend(legend2)

        # Assert
        assert len(manager.terrain_types) == 1
        assert "." not in manager.terrain_types
        assert "#" in manager.terrain_types
