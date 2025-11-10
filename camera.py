"""Camera system for viewport scrolling."""

from typing import Tuple
import config


class Camera:
    """Manages the viewport camera that follows the player."""

    def __init__(self, world_width: int, world_height: int):
        """
        Initialize the camera.

        Args:
            world_width: Width of the world in tiles
            world_height: Height of the world in tiles
        """
        self.world_width = world_width
        self.world_height = world_height
        self.x = 0  # Camera position in grid coordinates
        self.y = 0

        # Viewport dimensions in tiles (use game area, not full screen)
        self.viewport_width = config.GAME_GRID_WIDTH
        self.viewport_height = config.GAME_GRID_HEIGHT

    def update(self, player_grid_x: int, player_grid_y: int) -> None:
        """
        Update camera position to center on player.

        Camera is clamped at world edges to prevent showing empty space.

        Args:
            player_grid_x: Player's grid x position
            player_grid_y: Player's grid y position
        """
        # Center camera on player
        target_x = player_grid_x - self.viewport_width // 2
        target_y = player_grid_y - self.viewport_height // 2

        # Clamp camera to world bounds (using max/min pattern)
        # If world is smaller than viewport, camera stays at 0
        max_x = max(0, self.world_width - self.viewport_width)
        max_y = max(0, self.world_height - self.viewport_height)

        self.x = max(0, min(target_x, max_x))
        self.y = max(0, min(target_y, max_y))

    def world_to_screen(self, world_x: int, world_y: int) -> Tuple[int, int]:
        """
        Convert world grid coordinates to screen grid coordinates.

        Args:
            world_x: World grid x coordinate
            world_y: World grid y coordinate

        Returns:
            Tuple of (screen_x, screen_y) in grid coordinates
        """
        return (world_x - self.x, world_y - self.y)

    def screen_to_world(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """
        Convert screen grid coordinates to world grid coordinates.

        Args:
            screen_x: Screen grid x coordinate
            screen_y: Screen grid y coordinate

        Returns:
            Tuple of (world_x, world_y) in grid coordinates
        """
        return (screen_x + self.x, screen_y + self.y)

    def is_visible(self, world_x: int, world_y: int) -> bool:
        """
        Check if a world position is visible in the viewport.

        Args:
            world_x: World grid x coordinate
            world_y: World grid y coordinate

        Returns:
            True if position is visible, False otherwise
        """
        return (
            self.x <= world_x < self.x + self.viewport_width
            and self.y <= world_y < self.y + self.viewport_height
        )

    def get_visible_bounds(self) -> Tuple[int, int, int, int]:
        """
        Get the bounds of the visible area in world coordinates.

        Returns:
            Tuple of (min_x, min_y, max_x, max_y) in grid coordinates
        """
        return (
            self.x,
            self.y,
            self.x + self.viewport_width,
            self.y + self.viewport_height,
        )
