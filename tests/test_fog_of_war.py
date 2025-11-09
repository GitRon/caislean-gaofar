"""Tests for the FogOfWar class."""

from fog_of_war import FogOfWar


class TestFogOfWar:
    """Test suite for FogOfWar class."""

    def test_initialization_default_radius(self):
        """Test FogOfWar initializes with default visibility radius."""
        fog = FogOfWar()
        assert fog.visibility_radius == 2
        assert fog.discovered_tiles == {}
        assert fog.visible_tiles == set()

    def test_initialization_custom_radius(self):
        """Test FogOfWar initializes with custom visibility radius."""
        fog = FogOfWar(visibility_radius=3)
        assert fog.visibility_radius == 3

    def test_update_visibility_creates_visible_tiles(self):
        """Test that update_visibility creates visible tiles around player."""
        fog = FogOfWar(visibility_radius=2)
        fog.update_visibility(5, 5, "dungeon1")

        # Check that tiles within 2-tile radius are visible
        assert (5, 5) in fog.visible_tiles  # Player position
        assert (3, 3) in fog.visible_tiles  # 2 tiles away diagonally
        assert (7, 7) in fog.visible_tiles  # 2 tiles away diagonally
        assert (5, 3) in fog.visible_tiles  # 2 tiles north
        assert (5, 7) in fog.visible_tiles  # 2 tiles south
        assert (3, 5) in fog.visible_tiles  # 2 tiles west
        assert (7, 5) in fog.visible_tiles  # 2 tiles east

        # Check that tiles outside radius are not visible
        assert (2, 2) not in fog.visible_tiles  # 3 tiles away
        assert (8, 8) not in fog.visible_tiles  # 3 tiles away

    def test_update_visibility_creates_discovered_tiles(self):
        """Test that update_visibility marks tiles as discovered."""
        fog = FogOfWar(visibility_radius=2)
        fog.update_visibility(5, 5, "dungeon1")

        # Check that visible tiles are also discovered
        assert (5, 5) in fog.discovered_tiles["dungeon1"]
        assert (3, 3) in fog.discovered_tiles["dungeon1"]
        assert (7, 7) in fog.discovered_tiles["dungeon1"]

    def test_update_visibility_accumulates_discovered_tiles(self):
        """Test that discovered tiles persist when player moves."""
        fog = FogOfWar(visibility_radius=2)

        # Player at (5, 5)
        fog.update_visibility(5, 5, "dungeon1")
        assert (5, 5) in fog.discovered_tiles["dungeon1"]
        assert (3, 3) in fog.discovered_tiles["dungeon1"]

        # Player moves to (10, 10) - old tiles should still be discovered
        fog.update_visibility(10, 10, "dungeon1")
        assert (5, 5) in fog.discovered_tiles["dungeon1"]  # Still discovered
        assert (10, 10) in fog.discovered_tiles["dungeon1"]  # New discovery

    def test_update_visibility_clears_previous_visible_tiles(self):
        """Test that visible tiles are recalculated when player moves."""
        fog = FogOfWar(visibility_radius=2)

        # Player at (5, 5)
        fog.update_visibility(5, 5, "dungeon1")
        assert (5, 5) in fog.visible_tiles

        # Player moves to (10, 10)
        fog.update_visibility(10, 10, "dungeon1")
        assert (5, 5) not in fog.visible_tiles  # No longer visible
        assert (10, 10) in fog.visible_tiles  # Now visible

    def test_update_visibility_different_maps(self):
        """Test that different maps have separate discovered tiles."""
        fog = FogOfWar(visibility_radius=2)

        fog.update_visibility(5, 5, "dungeon1")
        fog.update_visibility(10, 10, "dungeon2")

        assert (5, 5) in fog.discovered_tiles["dungeon1"]
        assert (5, 5) not in fog.discovered_tiles.get("dungeon2", set())
        assert (10, 10) in fog.discovered_tiles["dungeon2"]
        assert (10, 10) not in fog.discovered_tiles.get("dungeon1", set())

    def test_is_visible_returns_true_for_visible_tiles(self):
        """Test is_visible returns True for tiles in visibility radius."""
        fog = FogOfWar(visibility_radius=2)
        fog.update_visibility(5, 5, "dungeon1")

        assert fog.is_visible(5, 5) is True
        assert fog.is_visible(3, 3) is True
        assert fog.is_visible(7, 7) is True

    def test_is_visible_returns_false_for_non_visible_tiles(self):
        """Test is_visible returns False for tiles outside visibility radius."""
        fog = FogOfWar(visibility_radius=2)
        fog.update_visibility(5, 5, "dungeon1")

        assert fog.is_visible(10, 10) is False
        assert fog.is_visible(0, 0) is False

    def test_is_discovered_returns_true_for_discovered_tiles(self):
        """Test is_discovered returns True for previously discovered tiles."""
        fog = FogOfWar(visibility_radius=2)
        fog.update_visibility(5, 5, "dungeon1")

        # Move player away
        fog.update_visibility(10, 10, "dungeon1")

        # Old tiles should still be discovered
        assert fog.is_discovered(5, 5, "dungeon1") is True
        assert fog.is_discovered(3, 3, "dungeon1") is True

    def test_is_discovered_returns_false_for_undiscovered_tiles(self):
        """Test is_discovered returns False for never-visited tiles."""
        fog = FogOfWar(visibility_radius=2)
        fog.update_visibility(5, 5, "dungeon1")

        assert fog.is_discovered(20, 20, "dungeon1") is False

    def test_is_discovered_returns_false_for_unknown_map(self):
        """Test is_discovered returns False for maps not yet visited."""
        fog = FogOfWar(visibility_radius=2)
        fog.update_visibility(5, 5, "dungeon1")

        assert fog.is_discovered(5, 5, "unknown_map") is False

    def test_reset_for_map_clears_discovered_tiles(self):
        """Test reset_for_map clears discovered tiles for a specific map."""
        fog = FogOfWar(visibility_radius=2)
        fog.update_visibility(5, 5, "dungeon1")
        fog.update_visibility(10, 10, "dungeon2")

        # Reset dungeon1
        fog.reset_for_map("dungeon1")

        # dungeon1 tiles should be cleared
        assert (5, 5) not in fog.discovered_tiles.get("dungeon1", set())

        # dungeon2 tiles should remain
        assert (10, 10) in fog.discovered_tiles["dungeon2"]

    def test_reset_for_map_handles_non_existent_map(self):
        """Test reset_for_map handles maps that don't exist."""
        fog = FogOfWar(visibility_radius=2)
        fog.update_visibility(5, 5, "dungeon1")

        # Reset a map that was never initialized
        fog.reset_for_map("unknown_map")

        # Should not raise error and dungeon1 should be unaffected
        assert (5, 5) in fog.discovered_tiles["dungeon1"]

    def test_is_fog_enabled_for_map_world(self):
        """Test fog is disabled for world/overworld map."""
        fog = FogOfWar()

        assert fog.is_fog_enabled_for_map("world") is False
        assert fog.is_fog_enabled_for_map("overworld") is False

    def test_is_fog_enabled_for_map_dungeons(self):
        """Test fog is enabled for dungeon maps."""
        fog = FogOfWar()

        assert fog.is_fog_enabled_for_map("dungeon1") is True
        assert fog.is_fog_enabled_for_map("dark_cave") is True
        assert fog.is_fog_enabled_for_map("ancient_castle") is True
        assert fog.is_fog_enabled_for_map("town") is True

    def test_visibility_radius_coverage(self):
        """Test different visibility radius values."""
        # Radius 1
        fog1 = FogOfWar(visibility_radius=1)
        fog1.update_visibility(5, 5, "dungeon1")
        assert (5, 5) in fog1.visible_tiles
        assert (6, 6) in fog1.visible_tiles
        assert (7, 7) not in fog1.visible_tiles

        # Radius 3
        fog3 = FogOfWar(visibility_radius=3)
        fog3.update_visibility(5, 5, "dungeon1")
        assert (5, 5) in fog3.visible_tiles
        assert (8, 8) in fog3.visible_tiles
        assert (9, 9) not in fog3.visible_tiles

    def test_visibility_includes_negative_coordinates(self):
        """Test that visibility works with coordinates near origin."""
        fog = FogOfWar(visibility_radius=2)
        fog.update_visibility(1, 1, "dungeon1")

        # Should include negative coordinates
        assert (-1, -1) in fog.visible_tiles
        assert (0, 0) in fog.visible_tiles
        assert (1, 1) in fog.visible_tiles
        assert (3, 3) in fog.visible_tiles
