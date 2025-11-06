"""Tests for grid.py - Grid class"""

from grid import Grid
import config


class TestGrid:
    """Tests for Grid class"""

    def test_grid_to_pixel_origin(self):
        """Test converting grid origin to pixel coordinates"""
        # Arrange & Act
        pixel_x, pixel_y = Grid.grid_to_pixel(0, 0)

        # Assert
        assert pixel_x == 0
        assert pixel_y == 0

    def test_grid_to_pixel_positive_coordinates(self):
        """Test converting positive grid coordinates to pixels"""
        # Arrange & Act
        pixel_x, pixel_y = Grid.grid_to_pixel(5, 3)

        # Assert
        assert pixel_x == 5 * config.TILE_SIZE
        assert pixel_y == 3 * config.TILE_SIZE

    def test_grid_to_pixel_single_tile(self):
        """Test converting single tile coordinates"""
        # Arrange & Act
        pixel_x, pixel_y = Grid.grid_to_pixel(1, 1)

        # Assert
        assert pixel_x == config.TILE_SIZE
        assert pixel_y == config.TILE_SIZE

    def test_pixel_to_grid_origin(self):
        """Test converting pixel origin to grid coordinates"""
        # Arrange & Act
        grid_x, grid_y = Grid.pixel_to_grid(0, 0)

        # Assert
        assert grid_x == 0
        assert grid_y == 0

    def test_pixel_to_grid_exact_tile_boundary(self):
        """Test converting pixels on exact tile boundary"""
        # Arrange
        pixel_x = 5 * config.TILE_SIZE
        pixel_y = 3 * config.TILE_SIZE

        # Act
        grid_x, grid_y = Grid.pixel_to_grid(pixel_x, pixel_y)

        # Assert
        assert grid_x == 5
        assert grid_y == 3

    def test_pixel_to_grid_within_tile(self):
        """Test converting pixels within a tile"""
        # Arrange
        pixel_x = 5 * config.TILE_SIZE + 10
        pixel_y = 3 * config.TILE_SIZE + 20

        # Act
        grid_x, grid_y = Grid.pixel_to_grid(pixel_x, pixel_y)

        # Assert
        assert grid_x == 5
        assert grid_y == 3

    def test_pixel_to_grid_float_coordinates(self):
        """Test converting float pixel coordinates"""
        # Arrange & Act
        grid_x, grid_y = Grid.pixel_to_grid(125.7, 87.3)

        # Assert
        assert isinstance(grid_x, int)
        assert isinstance(grid_y, int)
        assert grid_x == 125 // config.TILE_SIZE
        assert grid_y == 87 // config.TILE_SIZE

    def test_is_valid_position_origin(self):
        """Test origin is valid position"""
        # Arrange & Act
        result = Grid.is_valid_position(0, 0)

        # Assert
        assert result is True

    def test_is_valid_position_within_bounds(self):
        """Test position within bounds is valid"""
        # Arrange & Act
        result = Grid.is_valid_position(5, 5)

        # Assert
        assert result is True

    def test_is_valid_position_at_right_edge(self):
        """Test position at right edge boundary"""
        # Arrange & Act
        result = Grid.is_valid_position(config.GRID_WIDTH - 1, 0)

        # Assert
        assert result is True

    def test_is_valid_position_at_bottom_edge(self):
        """Test position at bottom edge boundary"""
        # Arrange & Act
        result = Grid.is_valid_position(0, config.GRID_HEIGHT - 1)

        # Assert
        assert result is True

    def test_is_valid_position_negative_x(self):
        """Test negative x is invalid"""
        # Arrange & Act
        result = Grid.is_valid_position(-1, 0)

        # Assert
        assert result is False

    def test_is_valid_position_negative_y(self):
        """Test negative y is invalid"""
        # Arrange & Act
        result = Grid.is_valid_position(0, -1)

        # Assert
        assert result is False

    def test_is_valid_position_x_too_large(self):
        """Test x beyond grid width is invalid"""
        # Arrange & Act
        result = Grid.is_valid_position(config.GRID_WIDTH, 0)

        # Assert
        assert result is False

    def test_is_valid_position_y_too_large(self):
        """Test y beyond grid height is invalid"""
        # Arrange & Act
        result = Grid.is_valid_position(0, config.GRID_HEIGHT)

        # Assert
        assert result is False

    def test_manhattan_distance_same_position(self):
        """Test Manhattan distance for same position"""
        # Arrange & Act
        distance = Grid.manhattan_distance(5, 5, 5, 5)

        # Assert
        assert distance == 0

    def test_manhattan_distance_horizontal(self):
        """Test Manhattan distance for horizontal movement"""
        # Arrange & Act
        distance = Grid.manhattan_distance(2, 5, 7, 5)

        # Assert
        assert distance == 5

    def test_manhattan_distance_vertical(self):
        """Test Manhattan distance for vertical movement"""
        # Arrange & Act
        distance = Grid.manhattan_distance(5, 2, 5, 8)

        # Assert
        assert distance == 6

    def test_manhattan_distance_diagonal(self):
        """Test Manhattan distance for diagonal movement"""
        # Arrange & Act
        distance = Grid.manhattan_distance(1, 1, 4, 5)

        # Assert
        assert distance == 7  # 3 + 4

    def test_manhattan_distance_negative_delta(self):
        """Test Manhattan distance with negative delta"""
        # Arrange & Act
        distance = Grid.manhattan_distance(7, 8, 3, 2)

        # Assert
        assert distance == 10  # 4 + 6

    def test_get_adjacent_positions_center(self):
        """Test getting adjacent positions from center of grid"""
        # Arrange & Act
        adjacent = Grid.get_adjacent_positions(5, 5)

        # Assert
        assert len(adjacent) == 4
        assert (5, 4) in adjacent  # up
        assert (5, 6) in adjacent  # down
        assert (4, 5) in adjacent  # left
        assert (6, 5) in adjacent  # right

    def test_get_adjacent_positions_top_left_corner(self):
        """Test getting adjacent positions from top-left corner"""
        # Arrange & Act
        adjacent = Grid.get_adjacent_positions(0, 0)

        # Assert
        assert len(adjacent) == 2
        assert (0, 1) in adjacent  # down
        assert (1, 0) in adjacent  # right

    def test_get_adjacent_positions_top_right_corner(self):
        """Test getting adjacent positions from top-right corner"""
        # Arrange & Act
        adjacent = Grid.get_adjacent_positions(config.GRID_WIDTH - 1, 0)

        # Assert
        assert len(adjacent) == 2
        assert (config.GRID_WIDTH - 1, 1) in adjacent  # down
        assert (config.GRID_WIDTH - 2, 0) in adjacent  # left

    def test_get_adjacent_positions_bottom_left_corner(self):
        """Test getting adjacent positions from bottom-left corner"""
        # Arrange & Act
        adjacent = Grid.get_adjacent_positions(0, config.GRID_HEIGHT - 1)

        # Assert
        assert len(adjacent) == 2
        assert (0, config.GRID_HEIGHT - 2) in adjacent  # up
        assert (1, config.GRID_HEIGHT - 1) in adjacent  # right

    def test_get_adjacent_positions_bottom_right_corner(self):
        """Test getting adjacent positions from bottom-right corner"""
        # Arrange & Act
        adjacent = Grid.get_adjacent_positions(
            config.GRID_WIDTH - 1, config.GRID_HEIGHT - 1
        )

        # Assert
        assert len(adjacent) == 2
        assert (config.GRID_WIDTH - 1, config.GRID_HEIGHT - 2) in adjacent  # up
        assert (config.GRID_WIDTH - 2, config.GRID_HEIGHT - 1) in adjacent  # left

    def test_get_adjacent_positions_top_edge(self):
        """Test getting adjacent positions from top edge"""
        # Arrange & Act
        adjacent = Grid.get_adjacent_positions(5, 0)

        # Assert
        assert len(adjacent) == 3
        assert (5, 1) in adjacent  # down
        assert (4, 0) in adjacent  # left
        assert (6, 0) in adjacent  # right

    def test_get_adjacent_positions_bottom_edge(self):
        """Test getting adjacent positions from bottom edge"""
        # Arrange & Act
        adjacent = Grid.get_adjacent_positions(5, config.GRID_HEIGHT - 1)

        # Assert
        assert len(adjacent) == 3
        assert (5, config.GRID_HEIGHT - 2) in adjacent  # up
        assert (4, config.GRID_HEIGHT - 1) in adjacent  # left
        assert (6, config.GRID_HEIGHT - 1) in adjacent  # right

    def test_get_adjacent_positions_left_edge(self):
        """Test getting adjacent positions from left edge"""
        # Arrange & Act
        adjacent = Grid.get_adjacent_positions(0, 5)

        # Assert
        assert len(adjacent) == 3
        assert (0, 4) in adjacent  # up
        assert (0, 6) in adjacent  # down
        assert (1, 5) in adjacent  # right

    def test_get_adjacent_positions_right_edge(self):
        """Test getting adjacent positions from right edge"""
        # Arrange & Act
        adjacent = Grid.get_adjacent_positions(config.GRID_WIDTH - 1, 5)

        # Assert
        assert len(adjacent) == 3
        assert (config.GRID_WIDTH - 1, 4) in adjacent  # up
        assert (config.GRID_WIDTH - 1, 6) in adjacent  # down
        assert (config.GRID_WIDTH - 2, 5) in adjacent  # left
