"""Unit tests for WorldRenderer class."""

from unittest.mock import Mock, patch
import pygame
from world_renderer import WorldRenderer
import config


class TestWorldRenderer:
    """Test cases for WorldRenderer class."""

    @classmethod
    def setup_class(cls):
        """Initialize pygame for all tests."""
        pygame.init()

    @classmethod
    def teardown_class(cls):
        """Quit pygame after all tests."""
        pygame.quit()

    def test_initialization(self):
        """Test WorldRenderer initialization."""
        # Arrange
        screen = pygame.Surface((800, 600))

        # Act
        renderer = WorldRenderer(screen)

        # Assert
        assert renderer.screen == screen
        assert renderer.combat_system is not None
        assert renderer.inventory_ui is not None
        assert renderer.shop_ui is not None
        assert renderer.hud is not None

    @patch("pygame.display.flip")
    def test_draw_playing_state_without_fog(self, mock_flip):
        """Test drawing playing state without fog of war."""
        # Arrange
        screen = pygame.Surface((800, 600))
        renderer = WorldRenderer(screen)

        world_map = Mock()
        world_map.draw = Mock()

        camera = Mock()
        camera.x = 0
        camera.y = 0
        camera.viewport_width = 800
        camera.viewport_height = 600
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (10, 20)

        entity_manager = Mock()
        entity_manager.chests = []
        entity_manager.ground_items = []
        entity_manager.monsters = []
        entity_manager.get_nearest_alive_monster.return_value = None

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10
        warrior.health = 100
        warrior.max_health = 100
        warrior.gold = 50
        warrior.draw = Mock()
        warrior.inventory = Mock()
        warrior.inventory.get_all_items.return_value = []

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test"

        shop = Mock()
        shop.grid_x = 1
        shop.grid_y = 1

        # Act
        renderer.draw_playing_state(
            world_map=world_map,
            camera=camera,
            entity_manager=entity_manager,
            warrior=warrior,
            dungeon_manager=dungeon_manager,
            shop=shop,
            active_portal=None,
            return_portal=None,
            message="",
            fog_of_war=None,
        )

        # Assert
        world_map.draw.assert_called_once_with(screen, 0, 0, 800, 600)
        mock_flip.assert_called_once()

    @patch("pygame.display.flip")
    def test_draw_playing_state_with_fog(self, mock_flip):
        """Test drawing playing state with fog of war."""
        # Arrange
        screen = pygame.Surface((800, 600))
        renderer = WorldRenderer(screen)

        world_map = Mock()
        world_map.draw = Mock()

        camera = Mock()
        camera.x = 0
        camera.y = 0
        camera.viewport_width = 800
        camera.viewport_height = 600
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (10, 20)

        entity_manager = Mock()
        entity_manager.chests = []
        entity_manager.ground_items = []
        entity_manager.monsters = []
        entity_manager.get_nearest_alive_monster.return_value = None

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10
        warrior.health = 100
        warrior.max_health = 100
        warrior.gold = 50
        warrior.draw = Mock()
        warrior.inventory = Mock()
        warrior.inventory.get_all_items.return_value = []

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test"

        shop = Mock()
        shop.grid_x = 1
        shop.grid_y = 1
        fog_of_war = Mock()

        # Act
        renderer.draw_playing_state(
            world_map=world_map,
            camera=camera,
            entity_manager=entity_manager,
            warrior=warrior,
            dungeon_manager=dungeon_manager,
            shop=shop,
            active_portal=None,
            return_portal=None,
            message="",
            fog_of_war=fog_of_war,
        )

        # Assert
        world_map.draw.assert_called_once_with(screen, 0, 0, 800, 600, fog_of_war)

    @patch("pygame.display.flip")
    def test_draw_playing_state_with_message(self, mock_flip):
        """Test drawing playing state with a message."""
        # Arrange
        screen = pygame.Surface((800, 600))
        renderer = WorldRenderer(screen)

        world_map = Mock()
        camera = Mock()
        camera.x = 0
        camera.y = 0
        camera.viewport_width = 800
        camera.viewport_height = 600
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (10, 20)

        entity_manager = Mock()
        entity_manager.chests = []
        entity_manager.ground_items = []
        entity_manager.monsters = []
        entity_manager.get_nearest_alive_monster.return_value = None

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10
        warrior.health = 100
        warrior.max_health = 100
        warrior.gold = 50
        warrior.draw = Mock()
        warrior.inventory = Mock()
        warrior.inventory.get_all_items.return_value = []

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test"

        shop = Mock()
        shop.grid_x = 1
        shop.grid_y = 1

        # Act
        with patch.object(renderer, "_draw_message") as mock_draw_message:
            renderer.draw_playing_state(
                world_map=world_map,
                camera=camera,
                entity_manager=entity_manager,
                warrior=warrior,
                dungeon_manager=dungeon_manager,
                shop=shop,
                active_portal=None,
                return_portal=None,
                message="Test message",
            )

            # Assert
            mock_draw_message.assert_called_once_with("Test message")

    @patch("pygame.display.flip")
    def test_draw_inventory_state(self, mock_flip):
        """Test drawing inventory state."""
        # Arrange
        screen = pygame.Surface((800, 600))
        renderer = WorldRenderer(screen)

        world_map = Mock()
        camera = Mock()
        camera.x = 0
        camera.y = 0
        camera.viewport_width = 800
        camera.viewport_height = 600
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (10, 20)

        entity_manager = Mock()
        entity_manager.chests = []
        entity_manager.ground_items = []
        entity_manager.monsters = []
        entity_manager.get_nearest_alive_monster.return_value = None

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10
        warrior.health = 100
        warrior.max_health = 100
        warrior.gold = 50
        warrior.inventory = Mock()
        warrior.inventory.get_all_items.return_value = []
        warrior.inventory.weapon_slot = None
        warrior.inventory.armor_slot = None
        warrior.inventory.backpack_slots = [None] * 13  # 13 backpack slots
        warrior.draw = Mock()

        # Act
        with patch.object(renderer.inventory_ui, "draw") as mock_inventory_draw:
            renderer.draw_inventory_state(
                world_map=world_map,
                camera=camera,
                entity_manager=entity_manager,
                warrior=warrior,
            )

            # Assert
            mock_inventory_draw.assert_called_once_with(screen, warrior.inventory)
            mock_flip.assert_called_once()

    @patch("pygame.display.flip")
    def test_draw_shop_state(self, mock_flip):
        """Test drawing shop state."""
        # Arrange
        screen = pygame.Surface((800, 600))
        renderer = WorldRenderer(screen)

        shop = Mock()
        shop.get_available_items.return_value = []
        warrior = Mock()
        warrior.health = 100
        warrior.max_health = 100
        warrior.gold = 50
        warrior.inventory = Mock()
        warrior.inventory.get_all_items.return_value = []

        # Act
        with patch.object(renderer.shop_ui, "draw") as mock_shop_draw:
            renderer.draw_shop_state(shop=shop, warrior=warrior)

            # Assert
            mock_shop_draw.assert_called_once_with(screen, shop, warrior)
            mock_flip.assert_called_once()

    @patch("pygame.display.flip")
    @patch("pygame.font.Font")
    def test_draw_game_over_state(self, mock_font, mock_flip):
        """Test drawing game over state."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance
        mock_text_surface = Mock()
        mock_text_surface.get_rect.return_value = pygame.Rect(0, 0, 100, 50)
        mock_font_instance.render.return_value = mock_text_surface

        # Act
        renderer.draw_game_over_state("GAME OVER!", config.RED)

        # Assert
        screen.fill.assert_called_once_with(config.BLACK)
        assert mock_font_instance.render.call_count >= 1
        mock_flip.assert_called_once()

    def test_draw_world_objects_with_camera(self):
        """Test drawing world objects with camera transformation."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (10, 20)

        chest = Mock()
        chest.grid_x = 5
        chest.grid_y = 10
        chest.draw = Mock()

        ground_item = Mock()
        ground_item.grid_x = 7
        ground_item.grid_y = 12
        ground_item.draw = Mock()

        entity_manager = Mock()
        entity_manager.chests = [chest]
        entity_manager.ground_items = [ground_item]

        # Act
        renderer._draw_world_objects_with_camera(camera, entity_manager)

        # Assert
        chest.draw.assert_called_once_with(screen)
        ground_item.draw.assert_called_once_with(screen)
        assert chest.grid_x == 5  # Restored after drawing
        assert chest.grid_y == 10
        assert ground_item.grid_x == 7
        assert ground_item.grid_y == 12

    def test_draw_entities_with_camera(self):
        """Test drawing entities with camera transformation."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (15, 25)

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10
        warrior.draw = Mock()

        monster = Mock()
        monster.is_alive = True
        monster.grid_x = 7
        monster.grid_y = 12
        monster.draw = Mock()

        entity_manager = Mock()
        entity_manager.monsters = [monster]

        # Act
        renderer._draw_entities_with_camera(camera, warrior, entity_manager)

        # Assert
        warrior.draw.assert_called_once_with(screen)
        monster.draw.assert_called_once_with(screen)
        assert warrior.grid_x == 5  # Restored
        assert warrior.grid_y == 10
        assert monster.grid_x == 7
        assert monster.grid_y == 12

    def test_draw_portal_with_camera(self):
        """Test drawing portal with camera transformation."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (20, 30)

        portal = Mock()
        portal.grid_x = 10
        portal.grid_y = 15
        portal.draw = Mock()

        # Act
        renderer._draw_portal_with_camera(camera, portal)

        # Assert
        portal.draw.assert_called_once_with(screen)
        assert portal.grid_x == 10  # Restored
        assert portal.grid_y == 15

    def test_draw_portal_not_visible(self):
        """Test that portal is not drawn when not visible."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = False

        portal = Mock()
        portal.grid_x = 10
        portal.grid_y = 15
        portal.draw = Mock()

        # Act
        renderer._draw_portal_with_camera(camera, portal)

        # Assert
        portal.draw.assert_not_called()

    @patch("pygame.draw.rect")
    @patch("pygame.draw.polygon")
    @patch("pygame.draw.circle")
    def test_draw_shop_building(self, mock_circle, mock_polygon, mock_rect):
        """Test drawing shop building."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (5, 10)

        shop = Mock()
        shop.grid_x = 4
        shop.grid_y = 3

        warrior = Mock()
        warrior.grid_x = 4
        warrior.grid_y = 4

        # Act
        renderer._draw_shop_building(camera, shop, warrior)

        # Assert
        assert mock_rect.call_count >= 4  # Building, door, windows
        mock_polygon.assert_called_once()  # Roof
        assert mock_circle.call_count >= 1  # Sign

    @patch("pygame.font.Font")
    def test_draw_message(self, mock_font):
        """Test drawing a message."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance
        mock_text_surface = Mock()
        mock_text_surface.get_rect.return_value = pygame.Rect(0, 0, 200, 30)
        mock_font_instance.render.return_value = mock_text_surface

        # Act
        renderer._draw_message("Test message")

        # Assert
        mock_font_instance.render.assert_called_once_with(
            "Test message", True, config.WHITE
        )
        assert screen.blit.call_count >= 2  # Background and text
