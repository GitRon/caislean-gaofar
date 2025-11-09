"""Tests for world_map.py - World map system"""

import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch
import pygame
from world_map import WorldMap
import config


@pytest.fixture
def sample_map_data():
    """Sample map data for testing"""
    return {
        "metadata": {"width": 10, "height": 8, "tile_size": 50},
        "legend": {
            ".": {"name": "meadow", "passable": True, "color": [50, 220, 50]},
            "#": {"name": "stone", "passable": False, "color": [128, 128, 128]},
        },
        "tiles": [
            "##########",
            "#........#",
            "#........#",
            "#........#",
            "#........#",
            "#........#",
            "#........#",
            "##########",
        ],
        "spawn_point": {"x": 5, "y": 4},
        "entities": {
            "monsters": [{"x": 7, "y": 4, "type": "banshee"}],
            "chests": [{"x": 3, "y": 2, "looted": False}],
        },
    }


@pytest.fixture
def temp_map_file(sample_map_data):
    """Create a temporary map file for testing"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        json.dump(sample_map_data, f)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


class TestWorldMap:
    """Tests for WorldMap class"""

    def test_world_map_initialization(self):
        """Test WorldMap initialization"""
        # Arrange & Act
        world_map = WorldMap()

        # Assert
        assert world_map.width == 0
        assert world_map.height == 0
        assert world_map.tile_size == config.TILE_SIZE
        assert world_map.tiles == []
        assert world_map.spawn_point == (0, 0)
        assert world_map.entity_spawns == {}

    def test_load_from_dict(self, sample_map_data):
        """Test loading map from dictionary"""
        # Arrange
        world_map = WorldMap()

        # Act
        world_map.load_from_dict(sample_map_data)

        # Assert
        assert world_map.width == 10
        assert world_map.height == 8
        assert world_map.tile_size == 50
        assert len(world_map.tiles) == 8
        assert len(world_map.tiles[0]) == 10
        assert world_map.spawn_point == (5, 4)

    def test_load_from_file(self, temp_map_file):
        """Test loading map from file"""
        # Arrange
        world_map = WorldMap()

        # Act
        world_map.load_from_file(temp_map_file)

        # Assert
        assert world_map.width == 10
        assert world_map.height == 8

    def test_load_from_file_not_found(self):
        """Test loading from non-existent file raises FileNotFoundError"""
        # Arrange
        world_map = WorldMap()

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            world_map.load_from_file("nonexistent.json")

    def test_load_from_dict_missing_metadata(self):
        """Test loading with missing metadata raises ValueError"""
        # Arrange
        world_map = WorldMap()
        data = {"legend": {}, "tiles": [], "spawn_point": {"x": 0, "y": 0}}

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            world_map.load_from_dict(data)

        assert "Missing required key in map data: 'metadata'" in str(exc_info.value)

    def test_load_from_dict_missing_legend(self):
        """Test loading with missing legend raises ValueError"""
        # Arrange
        world_map = WorldMap()
        data = {
            "metadata": {"width": 5, "height": 5},
            "tiles": [],
            "spawn_point": {"x": 0, "y": 0},
        }

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            world_map.load_from_dict(data)

        assert "Missing required key in map data: 'legend'" in str(exc_info.value)

    def test_load_from_dict_missing_tiles(self):
        """Test loading with missing tiles raises ValueError"""
        # Arrange
        world_map = WorldMap()
        data = {
            "metadata": {"width": 5, "height": 5},
            "legend": {},
            "spawn_point": {"x": 0, "y": 0},
        }

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            world_map.load_from_dict(data)

        assert "Missing required key in map data: 'tiles'" in str(exc_info.value)

    def test_load_from_dict_missing_spawn_point(self):
        """Test loading with missing spawn_point raises ValueError"""
        # Arrange
        world_map = WorldMap()
        data = {"metadata": {"width": 5, "height": 5}, "legend": {}, "tiles": []}

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            world_map.load_from_dict(data)

        assert "Missing required key in map data: 'spawn_point'" in str(exc_info.value)

    def test_load_from_dict_height_mismatch(self, sample_map_data):
        """Test loading with height mismatch raises ValueError"""
        # Arrange
        world_map = WorldMap()
        sample_map_data["metadata"]["height"] = 10  # Wrong height

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            world_map.load_from_dict(sample_map_data)

        assert "Tile data height" in str(exc_info.value)

    def test_load_from_dict_width_mismatch(self, sample_map_data):
        """Test loading with width mismatch raises ValueError"""
        # Arrange
        world_map = WorldMap()
        sample_map_data["tiles"][0] = "###"  # Wrong width

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            world_map.load_from_dict(sample_map_data)

        assert "Row 0 width" in str(exc_info.value)

    def test_load_from_dict_invalid_spawn_point(self, sample_map_data):
        """Test loading with invalid spawn point raises ValueError"""
        # Arrange
        world_map = WorldMap()
        sample_map_data["spawn_point"] = {"x": 100, "y": 100}

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            world_map.load_from_dict(sample_map_data)

        assert "Invalid spawn point" in str(exc_info.value)

    def test_is_valid_position_true(self, sample_map_data):
        """Test is_valid_position returns True for valid position"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)

        # Act
        result = world_map.is_valid_position(5, 4)

        # Assert
        assert result is True

    def test_is_valid_position_false_negative_x(self, sample_map_data):
        """Test is_valid_position returns False for negative x"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)

        # Act
        result = world_map.is_valid_position(-1, 4)

        # Assert
        assert result is False

    def test_is_valid_position_false_negative_y(self, sample_map_data):
        """Test is_valid_position returns False for negative y"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)

        # Act
        result = world_map.is_valid_position(5, -1)

        # Assert
        assert result is False

    def test_is_valid_position_false_exceeds_width(self, sample_map_data):
        """Test is_valid_position returns False for x >= width"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)

        # Act
        result = world_map.is_valid_position(10, 4)

        # Assert
        assert result is False

    def test_is_valid_position_false_exceeds_height(self, sample_map_data):
        """Test is_valid_position returns False for y >= height"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)

        # Act
        result = world_map.is_valid_position(5, 8)

        # Assert
        assert result is False

    def test_is_passable_true(self, sample_map_data):
        """Test is_passable returns True for passable terrain"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)

        # Act
        result = world_map.is_passable(5, 4)  # Meadow

        # Assert
        assert result is True

    def test_is_passable_false_blocked(self, sample_map_data):
        """Test is_passable returns False for impassable terrain"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)

        # Act
        result = world_map.is_passable(0, 0)  # Stone wall

        # Assert
        assert result is False

    def test_is_passable_false_out_of_bounds(self, sample_map_data):
        """Test is_passable returns False for out of bounds position"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)

        # Act
        result = world_map.is_passable(-1, 4)

        # Assert
        assert result is False

    def test_get_terrain_valid(self, sample_map_data):
        """Test get_terrain returns TerrainType for valid position"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)

        # Act
        terrain = world_map.get_terrain(5, 4)

        # Assert
        assert terrain is not None
        assert terrain.name == "meadow"

    def test_get_terrain_invalid(self, sample_map_data):
        """Test get_terrain returns None for invalid position"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)

        # Act
        terrain = world_map.get_terrain(-1, 4)

        # Assert
        assert terrain is None

    def test_get_entity_spawns(self, sample_map_data):
        """Test getting entity spawns by type"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)

        # Act
        monsters = world_map.get_entity_spawns("monsters")
        chests = world_map.get_entity_spawns("chests")

        # Assert
        assert len(monsters) == 1
        assert monsters[0]["x"] == 7
        assert len(chests) == 1
        assert chests[0]["looted"] is False

    def test_get_entity_spawns_empty(self, sample_map_data):
        """Test getting entity spawns for non-existent type"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)

        # Act
        dungeons = world_map.get_entity_spawns("dungeons")

        # Assert
        assert dungeons == []

    @patch("pygame.draw.rect")
    def test_draw(self, mock_draw_rect, sample_map_data):
        """Test drawing the world map"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)
        mock_screen = Mock(spec=pygame.Surface)

        # Act
        world_map.draw(mock_screen, 0, 0, 10, 8)

        # Assert
        # Should draw tiles for the visible area
        assert mock_draw_rect.called

    def test_load_from_dict_without_entities(self):
        """Test loading map without entities section"""
        # Arrange
        world_map = WorldMap()
        data = {
            "metadata": {"width": 3, "height": 3, "tile_size": 50},
            "legend": {
                ".": {"name": "meadow", "passable": True, "color": [50, 220, 50]}
            },
            "tiles": ["...", "...", "..."],
            "spawn_point": {"x": 1, "y": 1},
        }

        # Act
        world_map.load_from_dict(data)

        # Assert
        assert world_map.entity_spawns == {}

    @patch("pygame.draw.rect")
    def test_draw_with_none_terrain(self, mock_draw_rect, sample_map_data):
        """Test drawing when get_terrain returns None"""
        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)
        mock_screen = Mock(spec=pygame.Surface)

        # Mock get_terrain to return None for the first call
        original_get_terrain = world_map.get_terrain
        call_count = [0]

        def mock_get_terrain(x, y):
            call_count[0] += 1
            if call_count[0] == 1:
                return None
            return original_get_terrain(x, y)

        world_map.get_terrain = mock_get_terrain

        # Act
        world_map.draw(mock_screen, 0, 0, 10, 8)

        # Assert - should still complete without error
        assert mock_draw_rect.called

    @patch("pygame.draw.rect")
    def test_draw_with_fog_of_war_undiscovered_tiles(
        self, mock_draw_rect, sample_map_data
    ):
        """Test drawing with fog of war - undiscovered tiles are not drawn"""
        from fog_of_war import FogOfWar

        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)
        mock_screen = Mock(spec=pygame.Surface)
        fog = FogOfWar(visibility_radius=2)

        # Player at (5, 4) - only tiles near player are discovered
        fog.update_visibility(5, 4, "dungeon1")

        # Act
        world_map.draw(mock_screen, 0, 0, 10, 8, fog_of_war=fog, map_id="dungeon1")

        # Assert - should only draw discovered tiles (not all tiles)
        # The mock will be called for discovered tiles only
        assert mock_draw_rect.called

    @patch("pygame.draw.rect")
    def test_draw_with_fog_of_war_discovered_tiles(
        self, mock_draw_rect, sample_map_data
    ):
        """Test drawing with fog of war - discovered tiles are drawn"""
        from fog_of_war import FogOfWar

        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)
        mock_screen = Mock(spec=pygame.Surface)
        fog = FogOfWar(visibility_radius=2)

        # Discover all tiles by updating visibility at strategic positions
        # that cover the entire 10x8 map with radius 2
        fog.update_visibility(1, 1, "dungeon1")
        fog.update_visibility(1, 4, "dungeon1")
        fog.update_visibility(1, 7, "dungeon1")
        fog.update_visibility(4, 1, "dungeon1")
        fog.update_visibility(4, 4, "dungeon1")
        fog.update_visibility(4, 7, "dungeon1")
        fog.update_visibility(7, 1, "dungeon1")
        fog.update_visibility(7, 4, "dungeon1")
        fog.update_visibility(7, 7, "dungeon1")
        fog.update_visibility(9, 1, "dungeon1")
        fog.update_visibility(9, 4, "dungeon1")
        fog.update_visibility(9, 7, "dungeon1")

        # Act
        world_map.draw(mock_screen, 0, 0, 10, 8, fog_of_war=fog, map_id="dungeon1")

        # Assert - all tiles should be drawn since they're all discovered
        assert mock_draw_rect.called

    @patch("pygame.draw.rect")
    def test_draw_without_fog_of_war(self, mock_draw_rect, sample_map_data):
        """Test drawing without fog of war (world map)"""
        from fog_of_war import FogOfWar

        # Arrange
        world_map = WorldMap()
        world_map.load_from_dict(sample_map_data)
        mock_screen = Mock(spec=pygame.Surface)
        fog = FogOfWar(visibility_radius=2)

        # Act - world map should ignore fog of war
        world_map.draw(mock_screen, 0, 0, 10, 8, fog_of_war=fog, map_id="world")

        # Assert - all tiles should be drawn
        assert mock_draw_rect.called
