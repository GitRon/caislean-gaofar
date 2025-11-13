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
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

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
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

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
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

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
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

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

    @patch("pygame.display.flip")
    def test_draw_playing_state_with_active_portal_not_in_town(self, mock_flip):
        """Test drawing active portal when not in town."""
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
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "dungeon_level_1"

        shop = Mock()
        shop.grid_x = 1
        shop.grid_y = 1

        active_portal = Mock()
        active_portal.grid_x = 8
        active_portal.grid_y = 8
        active_portal.draw = Mock()

        # Act
        with patch.object(renderer, "_draw_portal_with_camera") as mock_draw_portal:
            renderer.draw_playing_state(
                world_map=world_map,
                camera=camera,
                entity_manager=entity_manager,
                warrior=warrior,
                dungeon_manager=dungeon_manager,
                shop=shop,
                active_portal=active_portal,
                return_portal=None,
                message="",
                fog_of_war=None,
            )

            # Assert
            mock_draw_portal.assert_called_once_with(camera, active_portal)

    @patch("pygame.display.flip")
    def test_draw_playing_state_with_return_portal_in_town(self, mock_flip):
        """Test drawing return portal when in town."""
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
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "town"

        shop = Mock()
        shop.grid_x = 1
        shop.grid_y = 1

        return_portal = Mock()
        return_portal.grid_x = 12
        return_portal.grid_y = 12
        return_portal.draw = Mock()

        # Act
        with patch.object(renderer, "_draw_portal_with_camera") as mock_draw_portal:
            renderer.draw_playing_state(
                world_map=world_map,
                camera=camera,
                entity_manager=entity_manager,
                warrior=warrior,
                dungeon_manager=dungeon_manager,
                shop=shop,
                active_portal=None,
                return_portal=return_portal,
                message="",
                fog_of_war=None,
            )

            # Assert
            mock_draw_portal.assert_called_once_with(camera, return_portal)

    @patch("pygame.display.flip")
    def test_draw_playing_state_with_shop_in_town(self, mock_flip):
        """Test drawing shop building when in town."""
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
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "town"

        shop = Mock()
        shop.grid_x = 1
        shop.grid_y = 1

        # Act
        with patch.object(renderer, "_draw_shop_building") as mock_draw_shop:
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
            mock_draw_shop.assert_called_once_with(camera, shop, warrior)

    @patch("pygame.display.flip")
    def test_draw_playing_state_with_nearest_monster(self, mock_flip):
        """Test drawing combat UI when nearest monster exists."""
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

        nearest_monster = Mock()
        nearest_monster.is_alive = True

        entity_manager = Mock()
        entity_manager.chests = []
        entity_manager.ground_items = []
        entity_manager.monsters = [nearest_monster]
        entity_manager.get_nearest_alive_monster.return_value = nearest_monster

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10
        warrior.health = 100
        warrior.max_health = 100
        warrior.gold = 50
        warrior.draw = Mock()
        warrior.inventory = Mock()
        warrior.inventory.get_all_items.return_value = []
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test"

        shop = Mock()
        shop.grid_x = 1
        shop.grid_y = 1

        # Act
        with patch.object(renderer.combat_system, "draw_combat_ui") as mock_draw_combat:
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
            mock_draw_combat.assert_called_once_with(screen, warrior, nearest_monster)

    @patch("pygame.display.flip")
    def test_draw_inventory_state_with_fog(self, mock_flip):
        """Test drawing inventory state with fog of war."""
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
        warrior.inventory = Mock()
        warrior.inventory.get_all_items.return_value = []
        warrior.inventory.weapon_slot = None
        warrior.inventory.armor_slot = None
        warrior.inventory.backpack_slots = [None] * 13
        warrior.draw = Mock()
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

        fog_of_war = Mock()

        # Act
        renderer.draw_inventory_state(
            world_map=world_map,
            camera=camera,
            entity_manager=entity_manager,
            warrior=warrior,
            fog_of_war=fog_of_war,
        )

        # Assert
        world_map.draw.assert_called_once_with(screen, 0, 0, 800, 600, fog_of_war)

    @patch("pygame.display.flip")
    def test_draw_inventory_state_with_nearest_monster(self, mock_flip):
        """Test drawing combat UI in inventory state when nearest monster exists."""
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

        nearest_monster = Mock()
        nearest_monster.is_alive = True

        entity_manager = Mock()
        entity_manager.chests = []
        entity_manager.ground_items = []
        entity_manager.monsters = [nearest_monster]
        entity_manager.get_nearest_alive_monster.return_value = nearest_monster

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
        warrior.inventory.backpack_slots = [None] * 13
        warrior.draw = Mock()
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

        # Act
        with patch.object(renderer.combat_system, "draw_combat_ui") as mock_draw_combat:
            renderer.draw_inventory_state(
                world_map=world_map,
                camera=camera,
                entity_manager=entity_manager,
                warrior=warrior,
            )

            # Assert
            mock_draw_combat.assert_called_once_with(screen, warrior, nearest_monster)

    def test_draw_shop_building_not_visible(self):
        """Test that shop building is not drawn when not visible."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = False

        shop = Mock()
        shop.grid_x = 4
        shop.grid_y = 3

        warrior = Mock()
        warrior.grid_x = 4
        warrior.grid_y = 4

        # Act
        renderer._draw_shop_building(camera, shop, warrior)

        # Assert
        camera.world_to_screen.assert_not_called()

    @patch("pygame.draw.rect")
    @patch("pygame.draw.polygon")
    @patch("pygame.draw.circle")
    @patch("pygame.font.Font")
    def test_draw_shop_building_with_nearby_warrior(
        self, mock_font, mock_circle, mock_polygon, mock_rect
    ):
        """Test drawing shop building with 'Press S' text when warrior is nearby."""
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
        warrior.grid_x = 4  # Distance = 0, which is <= 1
        warrior.grid_y = 3

        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance
        mock_text_surface = Mock()
        mock_text_surface.get_width.return_value = 50
        mock_text_surface.get_height.return_value = 20
        mock_font_instance.render.return_value = mock_text_surface

        # Act
        renderer._draw_shop_building(camera, shop, warrior)

        # Assert
        # Verify that "Press S" text was rendered
        mock_font_instance.render.assert_called_once_with("Press S", True, config.WHITE)
        # Verify text was drawn
        assert screen.blit.call_count >= 1

    def test_draw_world_objects_with_camera_not_visible(self):
        """Test drawing world objects when not visible to camera."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = False  # Not visible

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

        # Assert - nothing should be drawn
        chest.draw.assert_not_called()
        ground_item.draw.assert_not_called()

    def test_draw_entities_with_camera_warrior_not_visible(self):
        """Test drawing entities when warrior is not visible."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = False  # Not visible

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10
        warrior.draw = Mock()

        entity_manager = Mock()
        entity_manager.monsters = []

        # Act
        renderer._draw_entities_with_camera(camera, warrior, entity_manager)

        # Assert - warrior should not be drawn
        warrior.draw.assert_not_called()

    def test_draw_entities_with_camera_monster_not_visible(self):
        """Test drawing entities when monster is not visible."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()

        def is_visible_check(x, y):
            # Warrior visible, monster not visible
            return x == 5 and y == 10

        camera.is_visible.side_effect = is_visible_check
        camera.world_to_screen.return_value = (15, 25)

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10
        warrior.draw = Mock()

        monster = Mock()
        monster.is_alive = True
        monster.grid_x = 20
        monster.grid_y = 30
        monster.draw = Mock()

        entity_manager = Mock()
        entity_manager.monsters = [monster]

        # Act
        renderer._draw_entities_with_camera(camera, warrior, entity_manager)

        # Assert
        warrior.draw.assert_called_once()  # Warrior drawn
        monster.draw.assert_not_called()  # Monster not drawn

    def test_draw_entities_with_camera_dead_monster(self):
        """Test drawing entities skips dead monsters."""
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
        monster.is_alive = False  # Dead
        monster.grid_x = 7
        monster.grid_y = 12
        monster.draw = Mock()

        entity_manager = Mock()
        entity_manager.monsters = [monster]

        # Act
        renderer._draw_entities_with_camera(camera, warrior, entity_manager)

        # Assert
        warrior.draw.assert_called_once()
        monster.draw.assert_not_called()  # Dead monster not drawn

    @patch("pygame.display.flip")
    def test_draw_playing_state_with_temple_in_town(self, mock_flip):
        """Test drawing temple when in town."""
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
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "town"

        shop = Mock()
        shop.grid_x = 4
        shop.grid_y = 3

        temple = Mock()
        temple.grid_x = 8
        temple.grid_y = 1
        temple.draw = Mock()

        # Act
        with patch.object(renderer, "_draw_temple_with_camera") as mock_draw_temple:
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
                temple=temple,
            )

            # Assert
            mock_draw_temple.assert_called_once_with(camera, temple)

    @patch("pygame.display.flip")
    def test_draw_playing_state_without_temple(self, mock_flip):
        """Test drawing when temple is None."""
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
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "town"

        shop = Mock()
        shop.grid_x = 4
        shop.grid_y = 3

        # Act
        with patch.object(renderer, "_draw_temple_with_camera") as mock_draw_temple:
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
                temple=None,
            )

            # Assert - temple drawing should not be called
            mock_draw_temple.assert_not_called()

    def test_draw_temple_with_camera(self):
        """Test drawing temple with camera transformation."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (20, 30)

        temple = Mock()
        temple.grid_x = 8
        temple.grid_y = 1
        temple.draw = Mock()

        # Act
        renderer._draw_temple_with_camera(camera, temple)

        # Assert
        temple.draw.assert_called_once_with(screen)
        assert temple.grid_x == 8  # Restored
        assert temple.grid_y == 1

    def test_draw_temple_not_visible(self):
        """Test that temple is not drawn when not visible."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = False

        temple = Mock()
        temple.grid_x = 8
        temple.grid_y = 1
        temple.draw = Mock()

        # Act
        renderer._draw_temple_with_camera(camera, temple)

        # Assert
        temple.draw.assert_not_called()

    @patch("pygame.display.flip")
    def test_draw_playing_state_with_dungeons_on_world_map(self, mock_flip):
        """Test drawing dungeon icons when on world map."""
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
        warrior.experience = Mock()
        warrior.experience.get_xp_progress.return_value = 0.5
        warrior.experience.current_level = 1
        warrior.experience.get_available_skill_points.return_value = 0

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "world"

        shop = Mock()
        shop.grid_x = 1
        shop.grid_y = 1

        # Act
        with patch.object(renderer, "_draw_dungeons_with_camera") as mock_draw_dungeons:
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
            mock_draw_dungeons.assert_called_once_with(camera, dungeon_manager, warrior)

    def test_draw_dungeons_with_camera_cave_entrance(self):
        """Test drawing cave entrance dungeon icons."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (5, 10)

        world_map = Mock()
        world_map.tiles = [
            [".", ".", "."],
            [".", "C", "."],  # Cave entrance at (1, 1)
            [".", ".", "."],
        ]
        world_map.get_entity_spawns.return_value = [
            {"id": "cave_dungeon", "name": "Dark Cave", "x": 1, "y": 1}
        ]

        dungeon_manager = Mock()
        dungeon_manager.dungeon_entrances = {"cave_dungeon": (1, 1)}
        dungeon_manager.world_map = world_map

        warrior = Mock()
        warrior.grid_x = 10  # Far away
        warrior.grid_y = 10

        # Act
        with patch.object(renderer, "_draw_cave_entrance") as mock_draw_cave:
            renderer._draw_dungeons_with_camera(camera, dungeon_manager, warrior)

            # Assert
            mock_draw_cave.assert_called_once()

    def test_draw_dungeons_with_camera_castle_entrance(self):
        """Test drawing castle entrance dungeon icons."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (5, 10)

        world_map = Mock()
        world_map.tiles = [
            [".", ".", "."],
            [".", "K", "."],  # Castle entrance at (1, 1)
            [".", ".", "."],
        ]
        world_map.get_entity_spawns.return_value = [
            {"id": "castle_dungeon", "name": "Ancient Castle", "x": 1, "y": 1}
        ]

        dungeon_manager = Mock()
        dungeon_manager.dungeon_entrances = {"castle_dungeon": (1, 1)}
        dungeon_manager.world_map = world_map

        warrior = Mock()
        warrior.grid_x = 10  # Far away
        warrior.grid_y = 10

        # Act
        with patch.object(renderer, "_draw_castle_entrance") as mock_draw_castle:
            renderer._draw_dungeons_with_camera(camera, dungeon_manager, warrior)

            # Assert
            mock_draw_castle.assert_called_once()

    def test_draw_dungeons_with_camera_generic_entrance(self):
        """Test drawing generic dungeon entrance icons."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (5, 10)

        world_map = Mock()
        world_map.tiles = [
            [".", ".", "."],
            [".", "D", "."],  # Generic dungeon at (1, 1)
            [".", ".", "."],
        ]
        world_map.get_entity_spawns.return_value = [
            {"id": "mystery_dungeon", "name": "Mystery Dungeon", "x": 1, "y": 1}
        ]

        dungeon_manager = Mock()
        dungeon_manager.dungeon_entrances = {"mystery_dungeon": (1, 1)}
        dungeon_manager.world_map = world_map

        warrior = Mock()
        warrior.grid_x = 10  # Far away
        warrior.grid_y = 10

        # Act
        with patch.object(renderer, "_draw_dungeon_entrance") as mock_draw_dungeon:
            renderer._draw_dungeons_with_camera(camera, dungeon_manager, warrior)

            # Assert
            mock_draw_dungeon.assert_called_once()

    def test_draw_dungeons_with_camera_not_visible(self):
        """Test dungeons not drawn when not visible to camera."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = False  # Not visible

        world_map = Mock()
        world_map.tiles = [
            [".", ".", "."],
            [".", "C", "."],
            [".", ".", "."],
        ]

        dungeon_manager = Mock()
        dungeon_manager.dungeon_entrances = {"cave_dungeon": (1, 1)}
        dungeon_manager.world_map = world_map

        warrior = Mock()
        warrior.grid_x = 10
        warrior.grid_y = 10

        # Act
        with patch.object(renderer, "_draw_cave_entrance") as mock_draw_cave:
            renderer._draw_dungeons_with_camera(camera, dungeon_manager, warrior)

            # Assert
            mock_draw_cave.assert_not_called()

    @patch("pygame.draw.rect")
    def test_draw_dungeons_with_camera_shows_name_when_near(self, mock_draw_rect):
        """Test dungeon name is displayed when warrior is near."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (5, 10)

        world_map = Mock()
        world_map.tiles = [
            [".", ".", "."],
            [".", "C", "."],  # Cave entrance at (1, 1)
            [".", ".", "."],
        ]
        world_map.get_entity_spawns.return_value = [
            {"id": "cave_dungeon", "name": "Dark Cave", "x": 1, "y": 1}
        ]

        dungeon_manager = Mock()
        dungeon_manager.dungeon_entrances = {"cave_dungeon": (1, 1)}
        dungeon_manager.world_map = world_map

        warrior = Mock()
        warrior.grid_x = 1  # Next to dungeon
        warrior.grid_y = 2  # Distance = 1

        # Act
        with patch.object(renderer, "_draw_cave_entrance") as mock_draw_cave:
            renderer._draw_dungeons_with_camera(camera, dungeon_manager, warrior)

            # Assert
            mock_draw_cave.assert_called_once()
            # Verify text background was drawn
            assert mock_draw_rect.call_count >= 1
            # Verify text was drawn (blit called)
            assert screen.blit.call_count >= 1

    @patch("pygame.draw.ellipse")
    @patch("pygame.draw.circle")
    def test_draw_cave_entrance(self, mock_circle, mock_ellipse):
        """Test drawing cave entrance with arch and rocky edges."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        # Act
        renderer._draw_cave_entrance(100, 200, 50)

        # Assert
        assert mock_ellipse.call_count >= 2  # Main arch + inner cave
        assert mock_circle.call_count >= 4  # Rocky edges

    @patch("pygame.draw.rect")
    @patch("pygame.draw.line")
    def test_draw_castle_entrance(self, mock_line, mock_rect):
        """Test drawing castle entrance with battlements."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        # Act
        renderer._draw_castle_entrance(100, 200, 50)

        # Assert
        assert mock_rect.call_count >= 4  # Gate structure + battlements
        assert mock_line.call_count >= 3  # Stone block pattern

    @patch("pygame.draw.circle")
    def test_draw_dungeon_entrance(self, mock_circle):
        """Test drawing generic dungeon entrance portal."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        # Act
        renderer._draw_dungeon_entrance(100, 200, 50)

        # Assert
        assert mock_circle.call_count == 3  # Outer glow, inner portal, dark center

    def test_draw_dungeons_with_camera_multiple_dungeons(self):
        """Test drawing multiple dungeon entrances."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (5, 10)

        world_map = Mock()
        world_map.tiles = [
            [".", "C", "K", "D", "."],
            [".", ".", ".", ".", "."],
        ]
        world_map.get_entity_spawns.return_value = [
            {"id": "cave_dungeon", "name": "Dark Cave", "x": 1, "y": 0},
            {"id": "castle_dungeon", "name": "Castle", "x": 2, "y": 0},
            {"id": "mystery_dungeon", "name": "Mystery", "x": 3, "y": 0},
        ]

        dungeon_manager = Mock()
        dungeon_manager.dungeon_entrances = {
            "cave_dungeon": (1, 0),
            "castle_dungeon": (2, 0),
            "mystery_dungeon": (3, 0),
        }
        dungeon_manager.world_map = world_map

        warrior = Mock()
        warrior.grid_x = 10  # Far away from all dungeons
        warrior.grid_y = 10

        # Act
        with (
            patch.object(renderer, "_draw_cave_entrance") as mock_cave,
            patch.object(renderer, "_draw_castle_entrance") as mock_castle,
            patch.object(renderer, "_draw_dungeon_entrance") as mock_dungeon,
        ):
            renderer._draw_dungeons_with_camera(camera, dungeon_manager, warrior)

            # Assert - all three types should be drawn
            mock_cave.assert_called_once()
            mock_castle.assert_called_once()
            mock_dungeon.assert_called_once()

    def test_draw_dungeons_with_camera_warrior_far_from_dungeon(self):
        """Test dungeon name is not displayed when warrior is far."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (5, 10)

        world_map = Mock()
        world_map.tiles = [
            [".", ".", "."],
            [".", "C", "."],  # Cave entrance at (1, 1)
            [".", ".", "."],
        ]
        world_map.get_entity_spawns.return_value = [
            {"id": "cave_dungeon", "name": "Dark Cave", "x": 1, "y": 1}
        ]

        dungeon_manager = Mock()
        dungeon_manager.dungeon_entrances = {"cave_dungeon": (1, 1)}
        dungeon_manager.world_map = world_map

        warrior = Mock()
        warrior.grid_x = 10  # Far away
        warrior.grid_y = 10  # Distance = 18, which is > 1

        # Act
        with patch.object(renderer, "_draw_cave_entrance") as mock_draw_cave:
            renderer._draw_dungeons_with_camera(camera, dungeon_manager, warrior)

            # Assert
            mock_draw_cave.assert_called_once()
            # Verify text was NOT drawn (warrior too far)
            screen.blit.assert_not_called()

    def test_draw_dungeons_with_camera_no_matching_spawn_data(self):
        """Test dungeon drawing when spawn data doesn't match dungeon ID."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (5, 10)

        world_map = Mock()
        world_map.tiles = [
            [".", ".", "."],
            [".", "C", "."],  # Cave entrance at (1, 1)
            [".", ".", "."],
        ]
        # Spawn data with different ID (not matching dungeon_entrances)
        world_map.get_entity_spawns.return_value = [
            {"id": "different_dungeon", "name": "Other Cave", "x": 5, "y": 5}
        ]

        dungeon_manager = Mock()
        dungeon_manager.dungeon_entrances = {"cave_dungeon": (1, 1)}
        dungeon_manager.world_map = world_map

        warrior = Mock()
        warrior.grid_x = 1  # Next to dungeon
        warrior.grid_y = 2  # Distance = 1

        # Act
        with patch.object(renderer, "_draw_cave_entrance") as mock_draw_cave:
            renderer._draw_dungeons_with_camera(camera, dungeon_manager, warrior)

            # Assert
            mock_draw_cave.assert_called_once()
            # Name should not be drawn since no matching spawn data
            screen.blit.assert_not_called()

    @patch("pygame.draw.rect")
    def test_draw_dungeons_mixed_distances(self, mock_draw_rect):
        """Test drawing dungeons with warrior near one and far from another."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (5, 10)

        world_map = Mock()
        world_map.tiles = [
            ["C", ".", ".", ".", "K"],
            [".", ".", ".", ".", "."],
        ]
        world_map.get_entity_spawns.return_value = [
            {"id": "cave_dungeon", "name": "Near Cave", "x": 0, "y": 0},
            {"id": "castle_dungeon", "name": "Far Castle", "x": 4, "y": 0},
        ]

        dungeon_manager = Mock()
        dungeon_manager.dungeon_entrances = {
            "cave_dungeon": (0, 0),
            "castle_dungeon": (4, 0),
        }
        dungeon_manager.world_map = world_map

        warrior = Mock()
        warrior.grid_x = 0  # Next to cave (distance = 1)
        warrior.grid_y = 1

        # Act
        with (
            patch.object(renderer, "_draw_cave_entrance") as mock_cave,
            patch.object(renderer, "_draw_castle_entrance") as mock_castle,
        ):
            renderer._draw_dungeons_with_camera(camera, dungeon_manager, warrior)

            # Assert - both dungeons drawn
            mock_cave.assert_called_once()
            mock_castle.assert_called_once()
            # Name shown only for near cave (text background drawn)
            assert mock_draw_rect.call_count >= 1
            # Text drawn for near cave
            assert screen.blit.call_count >= 1

    def test_draw_dungeons_with_camera_unknown_terrain_type(self):
        """Test dungeon with unknown terrain character doesn't crash."""
        # Arrange
        screen = Mock()
        renderer = WorldRenderer(screen)

        camera = Mock()
        camera.is_visible.return_value = True
        camera.world_to_screen.return_value = (5, 10)

        world_map = Mock()
        world_map.tiles = [
            [".", ".", "."],
            [".", "X", "."],  # Unknown terrain type at (1, 1)
            [".", ".", "."],
        ]
        world_map.get_entity_spawns.return_value = [
            {"id": "unknown_dungeon", "name": "Unknown", "x": 1, "y": 1}
        ]

        dungeon_manager = Mock()
        dungeon_manager.dungeon_entrances = {"unknown_dungeon": (1, 1)}
        dungeon_manager.world_map = world_map

        warrior = Mock()
        warrior.grid_x = 10  # Far away
        warrior.grid_y = 10

        # Act
        with (
            patch.object(renderer, "_draw_cave_entrance") as mock_cave,
            patch.object(renderer, "_draw_castle_entrance") as mock_castle,
            patch.object(renderer, "_draw_dungeon_entrance") as mock_dungeon,
        ):
            renderer._draw_dungeons_with_camera(camera, dungeon_manager, warrior)

            # Assert - no drawing methods should be called for unknown type
            mock_cave.assert_not_called()
            mock_castle.assert_not_called()
            mock_dungeon.assert_not_called()
