"""Grid system for managing tile-based positioning."""

import config
from typing import Tuple


class Grid:
    """Manages the grid system for tile-based positioning."""

    @staticmethod
    def grid_to_pixel(grid_x: int, grid_y: int) -> Tuple[int, int]:
        """
        Convert grid coordinates to pixel coordinates.

        Args:
            grid_x: Grid x coordinate
            grid_y: Grid y coordinate

        Returns:
            Tuple of (pixel_x, pixel_y)
        """
        return (grid_x * config.TILE_SIZE, grid_y * config.TILE_SIZE)

    @staticmethod
    def pixel_to_grid(pixel_x: float, pixel_y: float) -> Tuple[int, int]:
        """
        Convert pixel coordinates to grid coordinates.

        Args:
            pixel_x: Pixel x coordinate
            pixel_y: Pixel y coordinate

        Returns:
            Tuple of (grid_x, grid_y)
        """
        return (int(pixel_x // config.TILE_SIZE), int(pixel_y // config.TILE_SIZE))

    @staticmethod
    def is_valid_position(grid_x: int, grid_y: int) -> bool:
        """
        Check if a grid position is valid (within bounds).

        Args:
            grid_x: Grid x coordinate
            grid_y: Grid y coordinate

        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= grid_x < config.GRID_WIDTH and 0 <= grid_y < config.GRID_HEIGHT

    @staticmethod
    def manhattan_distance(
        grid_x1: int, grid_y1: int, grid_x2: int, grid_y2: int
    ) -> int:
        """
        Calculate Manhattan distance between two grid positions.

        Args:
            grid_x1: First position x
            grid_y1: First position y
            grid_x2: Second position x
            grid_y2: Second position y

        Returns:
            Manhattan distance in tiles
        """
        return abs(grid_x1 - grid_x2) + abs(grid_y1 - grid_y2)

    @staticmethod
    def get_adjacent_positions(grid_x: int, grid_y: int) -> list:
        """
        Get all valid adjacent positions (4-directional).

        Args:
            grid_x: Center grid x coordinate
            grid_y: Center grid y coordinate

        Returns:
            List of valid adjacent (grid_x, grid_y) tuples
        """
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
        adjacent = []

        for dx, dy in directions:
            new_x = grid_x + dx
            new_y = grid_y + dy
            if Grid.is_valid_position(new_x, new_y):
                adjacent.append((new_x, new_y))

        return adjacent
