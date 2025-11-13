"""Tests for camera.py - Camera system"""

from caislean_gaofar.world.camera import Camera
from caislean_gaofar.core import config


class TestCamera:
    """Tests for Camera class"""

    def test_camera_initialization(self):
        """Test Camera initialization"""
        # Arrange & Act
        camera = Camera(40, 30)

        # Assert
        assert camera.world_width == 40
        assert camera.world_height == 30
        assert camera.x == 0
        assert camera.y == 0
        assert camera.viewport_width == config.GAME_GRID_WIDTH
        assert camera.viewport_height == config.GAME_GRID_HEIGHT

    def test_update_centers_on_player(self):
        """Test camera centers on player position"""
        # Arrange
        camera = Camera(40, 30)
        player_x = 20
        player_y = 15

        # Act
        camera.update(player_x, player_y)

        # Assert
        # Camera should center on player
        expected_x = player_x - camera.viewport_width // 2
        expected_y = player_y - camera.viewport_height // 2
        assert camera.x == expected_x
        assert camera.y == expected_y

    def test_update_clamps_at_left_edge(self):
        """Test camera clamps at left edge of world"""
        # Arrange
        camera = Camera(40, 30)
        player_x = 2
        player_y = 15

        # Act
        camera.update(player_x, player_y)

        # Assert
        # Camera should be clamped to 0
        assert camera.x == 0

    def test_update_clamps_at_top_edge(self):
        """Test camera clamps at top edge of world"""
        # Arrange
        camera = Camera(40, 30)
        player_x = 20
        player_y = 2

        # Act
        camera.update(player_x, player_y)

        # Assert
        # Camera should be clamped to 0
        assert camera.y == 0

    def test_update_clamps_at_right_edge(self):
        """Test camera clamps at right edge of world"""
        # Arrange
        camera = Camera(40, 30)
        player_x = 38
        player_y = 15

        # Act
        camera.update(player_x, player_y)

        # Assert
        # Camera should be clamped to world_width - viewport_width
        expected_x = 40 - camera.viewport_width
        assert camera.x == expected_x

    def test_update_clamps_at_bottom_edge(self):
        """Test camera clamps at bottom edge of world"""
        # Arrange
        camera = Camera(40, 30)
        player_x = 20
        player_y = 28

        # Act
        camera.update(player_x, player_y)

        # Assert
        # Camera should be clamped to world_height - viewport_height
        expected_y = 30 - camera.viewport_height
        assert camera.y == expected_y

    def test_world_to_screen(self):
        """Test converting world coordinates to screen coordinates"""
        # Arrange
        camera = Camera(40, 30)
        camera.x = 10
        camera.y = 5

        # Act
        screen_x, screen_y = camera.world_to_screen(15, 8)

        # Assert
        assert screen_x == 5  # 15 - 10
        assert screen_y == 3  # 8 - 5

    def test_screen_to_world(self):
        """Test converting screen coordinates to world coordinates"""
        # Arrange
        camera = Camera(40, 30)
        camera.x = 10
        camera.y = 5

        # Act
        world_x, world_y = camera.screen_to_world(5, 3)

        # Assert
        assert world_x == 15  # 5 + 10
        assert world_y == 8  # 3 + 5

    def test_is_visible_true(self):
        """Test is_visible returns True for visible position"""
        # Arrange
        camera = Camera(40, 30)
        camera.x = 10
        camera.y = 5

        # Act
        result = camera.is_visible(15, 8)

        # Assert
        assert result is True

    def test_is_visible_false_left(self):
        """Test is_visible returns False for position left of viewport"""
        # Arrange
        camera = Camera(40, 30)
        camera.x = 10
        camera.y = 5

        # Act
        result = camera.is_visible(5, 8)

        # Assert
        assert result is False

    def test_is_visible_false_right(self):
        """Test is_visible returns False for position right of viewport"""
        # Arrange
        camera = Camera(40, 30)
        camera.x = 10
        camera.y = 5

        # Act
        result = camera.is_visible(30, 8)

        # Assert
        assert result is False

    def test_is_visible_false_above(self):
        """Test is_visible returns False for position above viewport"""
        # Arrange
        camera = Camera(40, 30)
        camera.x = 10
        camera.y = 5

        # Act
        result = camera.is_visible(15, 2)

        # Assert
        assert result is False

    def test_is_visible_false_below(self):
        """Test is_visible returns False for position below viewport"""
        # Arrange
        camera = Camera(40, 30)
        camera.x = 10
        camera.y = 5

        # Act
        result = camera.is_visible(15, 20)

        # Assert
        assert result is False

    def test_get_visible_bounds(self):
        """Test getting visible bounds in world coordinates"""
        # Arrange
        camera = Camera(40, 30)
        camera.x = 10
        camera.y = 5

        # Act
        min_x, min_y, max_x, max_y = camera.get_visible_bounds()

        # Assert
        assert min_x == 10
        assert min_y == 5
        assert max_x == 10 + camera.viewport_width
        assert max_y == 5 + camera.viewport_height

    def test_update_with_small_world(self):
        """Test camera with world smaller than viewport"""
        # Arrange
        # Create a world smaller than the viewport
        camera = Camera(8, 6)  # Smaller than GAME_GRID_WIDTH and GAME_GRID_HEIGHT
        player_x = 4
        player_y = 3

        # Act
        camera.update(player_x, player_y)

        # Assert
        # Camera should be clamped to 0 since world is smaller than viewport
        assert camera.x == 0
        assert camera.y == 0
