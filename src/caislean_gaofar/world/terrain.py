"""Terrain types and properties for the game world."""

from typing import Tuple, Dict
from dataclasses import dataclass


@dataclass(kw_only=True)
class TerrainType:
    """Defines properties of a terrain type."""

    name: str
    character: str
    passable: bool
    color: Tuple[int, int, int]

    def __hash__(self):
        """Make TerrainType hashable for use in dictionaries."""
        return hash(self.character)


class TerrainManager:
    """Manages terrain types loaded from JSON legend."""

    def __init__(self):
        """Initialize empty terrain manager."""
        self.terrain_types: Dict[str, TerrainType] = {}

    def load_from_legend(self, legend: Dict[str, Dict]) -> None:
        """
        Load terrain types from JSON legend.

        Args:
            legend: Dictionary mapping character to terrain properties
                   Format: {"char": {"name": str, "passable": bool, "color": [r, g, b]}}
        """
        self.terrain_types = {}
        for char, properties in legend.items():
            terrain = TerrainType(
                name=properties["name"],
                character=char,
                passable=properties["passable"],
                color=tuple(properties["color"]),
            )
            self.terrain_types[char] = terrain

    def get_terrain(self, character: str) -> TerrainType:
        """
        Get terrain type by character.

        Args:
            character: Single character representing the terrain

        Returns:
            TerrainType object

        Raises:
            ValueError: If character not found in legend
        """
        if character not in self.terrain_types:
            raise ValueError(f"Unknown terrain character: '{character}'")
        return self.terrain_types[character]

    def is_passable(self, character: str) -> bool:
        """
        Check if terrain character is passable.

        Args:
            character: Single character representing the terrain

        Returns:
            True if passable, False otherwise
        """
        return self.get_terrain(character).passable
