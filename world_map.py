"""World map system for loading and managing game maps."""

import json
from typing import Tuple, List, Dict, Any, Optional
import pygame
from terrain import TerrainManager, TerrainType
import config


class WorldMap:
    """Manages the game world map including terrain and entities."""

    def __init__(self):
        """Initialize an empty world map."""
        self.width = 0
        self.height = 0
        self.tile_size = config.TILE_SIZE
        self.tiles: List[List[str]] = []  # 2D array of terrain characters
        self.terrain_manager = TerrainManager()
        self.spawn_point: Tuple[int, int] = (0, 0)
        self.entity_spawns: Dict[str, List[Dict[str, Any]]] = {}

    def load_from_file(self, filepath: str) -> None:
        """
        Load map from JSON file.

        Args:
            filepath: Path to the JSON map file

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON format is invalid
        """
        with open(filepath, "r") as f:
            data = json.load(f)

        self.load_from_dict(data)

    def load_from_dict(self, data: Dict[str, Any]) -> None:
        """
        Load map from dictionary.

        Args:
            data: Map data dictionary

        Raises:
            ValueError: If required keys are missing or data is invalid
        """
        # Validate required keys
        required_keys = ["metadata", "legend", "tiles", "spawn_point"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key in map data: '{key}'")

        # Load metadata
        metadata = data["metadata"]
        self.width = metadata["width"]
        self.height = metadata["height"]
        self.tile_size = metadata.get("tile_size", config.TILE_SIZE)

        # Load terrain legend
        self.terrain_manager.load_from_legend(data["legend"])

        # Load tiles - convert list of strings to 2D array
        tile_strings = data["tiles"]
        if len(tile_strings) != self.height:
            raise ValueError(
                f"Tile data height ({len(tile_strings)}) doesn't match "
                f"metadata height ({self.height})"
            )

        self.tiles = []
        for row_idx, row_string in enumerate(tile_strings):
            if len(row_string) != self.width:
                raise ValueError(
                    f"Row {row_idx} width ({len(row_string)}) doesn't match "
                    f"metadata width ({self.width})"
                )
            self.tiles.append(list(row_string))

        # Load spawn point
        spawn = data["spawn_point"]
        self.spawn_point = (spawn["x"], spawn["y"])

        # Validate spawn point
        if not self.is_valid_position(self.spawn_point[0], self.spawn_point[1]):
            raise ValueError(
                f"Invalid spawn point: {self.spawn_point} "
                f"(map size: {self.width}x{self.height})"
            )

        # Load entity spawns (optional)
        self.entity_spawns = data.get("entities", {})

    def is_valid_position(self, grid_x: int, grid_y: int) -> bool:
        """
        Check if a position is within map bounds.

        Args:
            grid_x: Grid x coordinate
            grid_y: Grid y coordinate

        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= grid_x < self.width and 0 <= grid_y < self.height

    def is_passable(self, grid_x: int, grid_y: int) -> bool:
        """
        Check if a position is passable (within bounds and not blocked).

        Args:
            grid_x: Grid x coordinate
            grid_y: Grid y coordinate

        Returns:
            True if position is passable, False otherwise
        """
        if not self.is_valid_position(grid_x, grid_y):
            return False

        terrain_char = self.tiles[grid_y][grid_x]
        return self.terrain_manager.is_passable(terrain_char)

    def get_terrain(self, grid_x: int, grid_y: int) -> Optional[TerrainType]:
        """
        Get terrain type at position.

        Args:
            grid_x: Grid x coordinate
            grid_y: Grid y coordinate

        Returns:
            TerrainType object or None if position invalid
        """
        if not self.is_valid_position(grid_x, grid_y):
            return None

        terrain_char = self.tiles[grid_y][grid_x]
        return self.terrain_manager.get_terrain(terrain_char)

    def draw(
        self, screen: pygame.Surface, camera_x: int, camera_y: int, viewport_width: int, viewport_height: int
    ) -> None:
        """
        Draw visible portion of the map.

        Args:
            screen: Pygame surface to draw on
            camera_x: Camera x position in grid coordinates
            camera_y: Camera y position in grid coordinates
            viewport_width: Width of viewport in tiles
            viewport_height: Height of viewport in tiles
        """
        # Calculate visible tile range
        start_x = max(0, camera_x)
        start_y = max(0, camera_y)
        end_x = min(self.width, camera_x + viewport_width)
        end_y = min(self.height, camera_y + viewport_height)

        # Draw visible tiles
        for world_y in range(start_y, end_y):
            for world_x in range(start_x, end_x):
                terrain = self.get_terrain(world_x, world_y)
                if terrain:
                    # Convert world coordinates to screen coordinates
                    screen_x = (world_x - camera_x) * self.tile_size
                    screen_y = (world_y - camera_y) * self.tile_size

                    # Draw tile
                    pygame.draw.rect(
                        screen,
                        terrain.color,
                        (screen_x, screen_y, self.tile_size, self.tile_size),
                    )

                    # Draw grid lines (optional)
                    pygame.draw.rect(
                        screen,
                        (50, 50, 50),  # Dark grey for grid lines
                        (screen_x, screen_y, self.tile_size, self.tile_size),
                        1,
                    )

    def get_entity_spawns(self, entity_type: str) -> List[Dict[str, Any]]:
        """
        Get spawn locations for a specific entity type.

        Args:
            entity_type: Type of entity (e.g., "monsters", "chests", "dungeons")

        Returns:
            List of spawn dictionaries with position and properties
        """
        return self.entity_spawns.get(entity_type, [])
