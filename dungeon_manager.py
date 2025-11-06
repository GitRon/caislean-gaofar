"""Dungeon manager for handling multiple maps and transitions."""

from typing import Dict, Optional, Tuple
from world_map import WorldMap
import os


class DungeonManager:
    """Manages dungeon maps and transitions between world and dungeons."""

    def __init__(self, world_map_path: str = None):
        """
        Initialize the dungeon manager.

        Args:
            world_map_path: Path to the world map file
        """
        self.world_map = WorldMap()
        self.dungeon_maps: Dict[str, WorldMap] = {}
        self.current_map_id = "world"
        self.world_map_path = world_map_path or os.path.join("maps", "sample_map.json")

        # Track return location when exiting dungeons
        self.return_location: Optional[Tuple[int, int]] = None

        # Track dungeon entrance locations on world map
        self.dungeon_entrances: Dict[str, Tuple[int, int]] = {}

    def load_world_map(self) -> None:
        """Load the world map from file."""
        self.world_map.load_from_file(self.world_map_path)
        self.current_map_id = "world"

        # Load dungeon entrance locations from world map
        self._load_dungeon_entrances()

    def _load_dungeon_entrances(self) -> None:
        """Load dungeon entrance locations from world map entities."""
        dungeon_spawns = self.world_map.get_entity_spawns("dungeons")
        for spawn in dungeon_spawns:
            dungeon_name = spawn.get("name", "unknown")
            dungeon_id = spawn.get("id", dungeon_name.lower().replace(" ", "_"))
            x, y = spawn["x"], spawn["y"]
            self.dungeon_entrances[dungeon_id] = (x, y)

    def load_dungeon(self, dungeon_id: str, dungeon_path: str) -> None:
        """
        Load a dungeon map from file.

        Args:
            dungeon_id: Unique identifier for the dungeon
            dungeon_path: Path to the dungeon map file
        """
        dungeon_map = WorldMap()
        dungeon_map.load_from_file(dungeon_path)
        self.dungeon_maps[dungeon_id] = dungeon_map

    def get_current_map(self) -> WorldMap:
        """
        Get the currently active map.

        Returns:
            The current WorldMap object
        """
        if self.current_map_id == "world":
            return self.world_map
        return self.dungeon_maps.get(self.current_map_id, self.world_map)

    def is_in_dungeon(self) -> bool:
        """
        Check if currently in a dungeon.

        Returns:
            True if in a dungeon, False if in world map
        """
        return self.current_map_id != "world"

    def get_dungeon_at_position(self, grid_x: int, grid_y: int) -> Optional[str]:
        """
        Check if there's a dungeon entrance at the given position.

        Args:
            grid_x: Grid x coordinate
            grid_y: Grid y coordinate

        Returns:
            Dungeon ID if entrance found, None otherwise
        """
        if self.current_map_id != "world":
            return None

        for dungeon_id, (entrance_x, entrance_y) in self.dungeon_entrances.items():
            if grid_x == entrance_x and grid_y == entrance_y:
                if dungeon_id in self.dungeon_maps:
                    return dungeon_id
        return None

    def enter_dungeon(self, dungeon_id: str, player_x: int, player_y: int) -> Tuple[int, int]:
        """
        Enter a dungeon and return spawn point.

        Args:
            dungeon_id: ID of the dungeon to enter
            player_x: Player's current x position (for return)
            player_y: Player's current y position (for return)

        Returns:
            Tuple of (spawn_x, spawn_y) in the dungeon

        Raises:
            ValueError: If dungeon_id doesn't exist
        """
        if dungeon_id not in self.dungeon_maps:
            raise ValueError(f"Dungeon '{dungeon_id}' not loaded")

        # Save return location
        self.return_location = (player_x, player_y)

        # Switch to dungeon map
        self.current_map_id = dungeon_id

        # Return dungeon spawn point
        dungeon = self.dungeon_maps[dungeon_id]
        return dungeon.spawn_point

    def exit_dungeon(self) -> Optional[Tuple[int, int]]:
        """
        Exit current dungeon and return to world map.

        Returns:
            Tuple of (return_x, return_y) in world map, or None if not in dungeon
        """
        if not self.is_in_dungeon():
            return None

        # Switch back to world map
        self.current_map_id = "world"

        # Get return location
        return_pos = self.return_location
        self.return_location = None

        return return_pos

    def check_for_exit(self, grid_x: int, grid_y: int) -> bool:
        """
        Check if player is standing on an exit tile.

        Args:
            grid_x: Grid x coordinate
            grid_y: Grid y coordinate

        Returns:
            True if on exit tile, False otherwise
        """
        if not self.is_in_dungeon():
            return False

        current_map = self.get_current_map()

        # Check if position is an exit tile (marked with '<' character)
        if current_map.is_valid_position(grid_x, grid_y):
            terrain_char = current_map.tiles[grid_y][grid_x]
            return terrain_char == '<'

        return False
