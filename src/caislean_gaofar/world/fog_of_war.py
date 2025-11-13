"""
Fog of War system for dungeon exploration.

This module manages tile visibility and discovery in dungeons. Players can only see
tiles within a certain radius (visibility range), and discovered tiles remain visible
but darkened when outside the current view.
"""


class FogOfWar:
    """Manages fog of war for map exploration.

    Tracks which tiles have been discovered and which are currently visible.
    Discovered tiles persist across the session, while visible tiles are
    recalculated based on player position.
    """

    def __init__(self, visibility_radius: int = 2):
        """Initialize the fog of war system.

        Args:
            visibility_radius: Number of tiles around the player that are visible (default: 2)
        """
        self.visibility_radius = visibility_radius
        # Maps map_id -> set of (x, y) tuples for discovered tiles
        self.discovered_tiles = {}
        # Currently visible tiles (recalculated each frame)
        self.visible_tiles = set()

    def reset_for_map(self, map_id: str):
        """Reset discovered tiles for a specific map.

        Args:
            map_id: Identifier for the map to reset
        """
        if map_id in self.discovered_tiles:
            self.discovered_tiles[map_id] = set()

    def update_visibility(self, player_grid_x: int, player_grid_y: int, map_id: str):
        """Update visible and discovered tiles based on player position.

        Args:
            player_grid_x: Player's grid X coordinate
            player_grid_y: Player's grid Y coordinate
            map_id: Current map identifier
        """
        # Initialize discovered tiles for this map if needed
        if map_id not in self.discovered_tiles:
            self.discovered_tiles[map_id] = set()

        # Clear current visible tiles
        self.visible_tiles.clear()

        # Calculate visible tiles within radius (using Chebyshev distance)
        for dx in range(-self.visibility_radius, self.visibility_radius + 1):
            for dy in range(-self.visibility_radius, self.visibility_radius + 1):
                tile_x = player_grid_x + dx
                tile_y = player_grid_y + dy

                # Add to visible tiles
                self.visible_tiles.add((tile_x, tile_y))

                # Add to discovered tiles (permanent for this map)
                self.discovered_tiles[map_id].add((tile_x, tile_y))

    def is_visible(self, grid_x: int, grid_y: int) -> bool:
        """Check if a tile is currently visible.

        Args:
            grid_x: Grid X coordinate
            grid_y: Grid Y coordinate

        Returns:
            True if the tile is currently visible
        """
        return (grid_x, grid_y) in self.visible_tiles

    def is_discovered(self, grid_x: int, grid_y: int, map_id: str) -> bool:
        """Check if a tile has been discovered.

        Args:
            grid_x: Grid X coordinate
            grid_y: Grid Y coordinate
            map_id: Current map identifier

        Returns:
            True if the tile has been discovered
        """
        if map_id not in self.discovered_tiles:
            return False
        return (grid_x, grid_y) in self.discovered_tiles[map_id]

    def is_fog_enabled_for_map(self, map_id: str) -> bool:
        """Check if fog of war should be enabled for a map.

        Args:
            map_id: Map identifier

        Returns:
            True if fog of war is enabled (dungeons only, not world map)
        """
        # Fog of war is enabled for all maps except the world/overworld
        return map_id != "world" and map_id != "overworld"
