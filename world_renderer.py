"""Rendering system for all game visuals."""

import pygame
from warrior import Warrior
from entity_manager import EntityManager
from combat import CombatSystem
from inventory_ui import InventoryUI
from shop import Shop
from shop_ui import ShopUI
from hud import HUD
from camera import Camera
from attack_effect import AttackEffectManager
import config


class WorldRenderer:
    """Handles all rendering concerns."""

    def __init__(self, screen: pygame.Surface):
        """
        Initialize the world renderer.

        Args:
            screen: The pygame screen surface
        """
        self.screen = screen
        self.combat_system = CombatSystem()
        self.inventory_ui = InventoryUI()
        self.shop_ui = ShopUI()
        self.hud = HUD()
        self.attack_effect_manager = AttackEffectManager()

    def draw_playing_state(
        self,
        world_map,
        camera: Camera,
        entity_manager: EntityManager,
        warrior: Warrior,
        dungeon_manager,
        shop: Shop,
        active_portal,
        return_portal,
        message: str,
        fog_of_war=None,
        temple=None,
    ):
        """
        Draw the playing state.

        Args:
            world_map: The current world map
            camera: The camera instance
            entity_manager: The entity manager
            warrior: The warrior entity
            dungeon_manager: The dungeon manager
            shop: The shop instance
            active_portal: Active portal if present
            return_portal: Return portal if present
            message: Current message to display
            fog_of_war: Fog of war system (optional)
            temple: Temple instance (optional)
        """
        self.screen.fill(config.BLACK)

        # Draw world map
        if fog_of_war:
            world_map.draw(
                self.screen,
                camera.x,
                camera.y,
                camera.viewport_width,
                camera.viewport_height,
                fog_of_war,
                dungeon_manager.current_map_id,
            )
        else:
            world_map.draw(
                self.screen,
                camera.x,
                camera.y,
                camera.viewport_width,
                camera.viewport_height,
            )

        # Draw world objects (chests and ground items) with camera offset
        self._draw_world_objects_with_camera(camera, entity_manager, fog_of_war, dungeon_manager)

        # Draw active portal if present (only when NOT in town)
        if active_portal and dungeon_manager.current_map_id != "town":
            self._draw_portal_with_camera(camera, active_portal)

        # Draw return portal if present (only when IN town)
        if return_portal and dungeon_manager.current_map_id == "town":
            self._draw_portal_with_camera(camera, return_portal)

        # Draw shop building if in town
        if dungeon_manager.current_map_id == "town":
            self._draw_shop_building(camera, shop, warrior)

            # Draw temple if present and in town
            if temple:
                self._draw_temple_with_camera(camera, temple)

        # Draw entities with camera offset
        self._draw_entities_with_camera(camera, warrior, entity_manager, fog_of_war, dungeon_manager)

        # Draw attack effects with camera offset
        self._draw_attack_effects_with_camera(camera)

        # Draw combat UI (find nearest monster)
        nearest_monster = entity_manager.get_nearest_alive_monster(warrior)
        if nearest_monster:
            self.combat_system.draw_combat_ui(self.screen, warrior, nearest_monster)

        # Draw HUD (player stats, potions, gold)
        self.hud.draw(self.screen, warrior)

        # Draw message if active
        if message:
            self._draw_message(message)

        pygame.display.flip()

    def draw_inventory_state(
        self,
        world_map,
        camera: Camera,
        entity_manager: EntityManager,
        warrior: Warrior,
        fog_of_war=None,
        dungeon_manager=None,
    ):
        """
        Draw the inventory state.

        Args:
            world_map: The current world map
            camera: The camera instance
            entity_manager: The entity manager
            warrior: The warrior entity
            fog_of_war: Fog of war system (optional)
            dungeon_manager: The dungeon manager (optional)
        """
        self.screen.fill(config.BLACK)

        # Draw the game in the background
        if fog_of_war and dungeon_manager:
            world_map.draw(
                self.screen,
                camera.x,
                camera.y,
                camera.viewport_width,
                camera.viewport_height,
                fog_of_war,
                dungeon_manager.current_map_id,
            )
        else:
            world_map.draw(
                self.screen,
                camera.x,
                camera.y,
                camera.viewport_width,
                camera.viewport_height,
            )
        self._draw_world_objects_with_camera(camera, entity_manager, fog_of_war, dungeon_manager)
        self._draw_entities_with_camera(camera, warrior, entity_manager, fog_of_war, dungeon_manager)
        nearest_monster = entity_manager.get_nearest_alive_monster(warrior)
        if nearest_monster:
            self.combat_system.draw_combat_ui(self.screen, warrior, nearest_monster)

        # Draw HUD (player stats, potions, gold)
        self.hud.draw(self.screen, warrior)

        # Draw inventory overlay on top
        self.inventory_ui.draw(self.screen, warrior.inventory)

        pygame.display.flip()

    def draw_shop_state(self, shop: Shop, warrior: Warrior):
        """
        Draw the shop state.

        Args:
            shop: The shop instance
            warrior: The warrior entity
        """
        self.screen.fill(config.BLACK)
        self.shop_ui.draw(self.screen, shop, warrior)
        pygame.display.flip()

    def draw_game_over_state(self, message: str, color: tuple):
        """
        Draw game over or victory screen.

        Args:
            message: Message to display
            color: Color of the message
        """
        self.screen.fill(config.BLACK)

        font_large = pygame.font.Font(None, 74)
        font_small = pygame.font.Font(None, 36)

        # Main message
        text = font_large.render(message, True, color)
        text_rect = text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50)
        )
        self.screen.blit(text, text_rect)

        # Restart instruction
        restart_text = font_small.render("Press R to Restart", True, config.WHITE)
        restart_rect = restart_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 50)
        )
        self.screen.blit(restart_text, restart_rect)

        # Exit instruction
        exit_text = font_small.render("Press ESC to Exit", True, config.WHITE)
        exit_rect = exit_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 100)
        )
        self.screen.blit(exit_text, exit_rect)

        pygame.display.flip()

    def _draw_world_objects_with_camera(
        self, camera: Camera, entity_manager: EntityManager, fog_of_war=None, dungeon_manager=None
    ):
        """
        Draw chests and ground items with camera offset applied.

        Args:
            camera: The camera instance
            entity_manager: The entity manager
            fog_of_war: Fog of war system (optional)
            dungeon_manager: The dungeon manager (optional)
        """
        # Check if fog of war is enabled for current map
        fog_enabled = (
            fog_of_war
            and dungeon_manager
            and fog_of_war.is_fog_enabled_for_map(dungeon_manager.current_map_id)
        )

        # Draw chests
        for chest in entity_manager.chests:
            if camera.is_visible(chest.grid_x, chest.grid_y):
                # Check fog of war visibility
                if fog_enabled and not fog_of_war.is_visible(chest.grid_x, chest.grid_y):
                    continue

                original_x = chest.grid_x
                original_y = chest.grid_y
                screen_x, screen_y = camera.world_to_screen(original_x, original_y)
                chest.grid_x = screen_x
                chest.grid_y = screen_y
                chest.draw(self.screen)
                chest.grid_x = original_x
                chest.grid_y = original_y

        # Draw ground items
        for ground_item in entity_manager.ground_items:
            if camera.is_visible(ground_item.grid_x, ground_item.grid_y):
                # Check fog of war visibility
                if fog_enabled and not fog_of_war.is_visible(ground_item.grid_x, ground_item.grid_y):
                    continue

                original_x = ground_item.grid_x
                original_y = ground_item.grid_y
                screen_x, screen_y = camera.world_to_screen(original_x, original_y)
                ground_item.grid_x = screen_x
                ground_item.grid_y = screen_y
                ground_item.draw(self.screen)
                ground_item.grid_x = original_x
                ground_item.grid_y = original_y

    def _draw_entities_with_camera(
        self, camera: Camera, warrior: Warrior, entity_manager: EntityManager, fog_of_war=None, dungeon_manager=None
    ):
        """
        Draw all entities with camera offset applied.

        Args:
            camera: The camera instance
            warrior: The warrior entity
            entity_manager: The entity manager
            fog_of_war: Fog of war system (optional)
            dungeon_manager: The dungeon manager (optional)
        """
        # Check if fog of war is enabled for current map
        fog_enabled = (
            fog_of_war
            and dungeon_manager
            and fog_of_war.is_fog_enabled_for_map(dungeon_manager.current_map_id)
        )

        # Draw warrior (always visible)
        if camera.is_visible(warrior.grid_x, warrior.grid_y):
            original_x = warrior.grid_x
            original_y = warrior.grid_y
            screen_x, screen_y = camera.world_to_screen(original_x, original_y)
            warrior.grid_x = screen_x
            warrior.grid_y = screen_y
            warrior.draw(self.screen)
            warrior.grid_x = original_x
            warrior.grid_y = original_y

        # Draw monsters
        for monster in entity_manager.monsters:
            if monster.is_alive and camera.is_visible(monster.grid_x, monster.grid_y):
                # Check fog of war visibility
                if fog_enabled and not fog_of_war.is_visible(monster.grid_x, monster.grid_y):
                    continue

                original_x = monster.grid_x
                original_y = monster.grid_y
                screen_x, screen_y = camera.world_to_screen(original_x, original_y)
                monster.grid_x = screen_x
                monster.grid_y = screen_y
                monster.draw(self.screen)
                monster.grid_x = original_x
                monster.grid_y = original_y

    def _draw_portal_with_camera(self, camera: Camera, portal):
        """
        Draw a portal with camera offset applied.

        Args:
            camera: The camera instance
            portal: The portal to draw
        """
        if camera.is_visible(portal.grid_x, portal.grid_y):
            original_x = portal.grid_x
            original_y = portal.grid_y
            screen_x, screen_y = camera.world_to_screen(original_x, original_y)
            portal.grid_x = screen_x
            portal.grid_y = screen_y
            portal.draw(self.screen)
            portal.grid_x = original_x
            portal.grid_y = original_y

    def _draw_temple_with_camera(self, camera: Camera, temple):
        """
        Draw a temple with camera offset applied.

        Args:
            camera: The camera instance
            temple: The temple to draw
        """
        if camera.is_visible(temple.grid_x, temple.grid_y):
            original_x = temple.grid_x
            original_y = temple.grid_y
            screen_x, screen_y = camera.world_to_screen(original_x, original_y)
            temple.grid_x = screen_x
            temple.grid_y = screen_y
            temple.draw(self.screen)
            temple.grid_x = original_x
            temple.grid_y = original_y

    def _draw_shop_building(self, camera: Camera, shop: Shop, warrior: Warrior):
        """
        Draw the shop building on the town map.

        Args:
            camera: The camera instance
            shop: The shop instance
            warrior: The warrior entity
        """
        if not camera.is_visible(shop.grid_x, shop.grid_y):
            return

        # Convert shop grid position to screen position
        screen_x, screen_y = camera.world_to_screen(shop.grid_x, shop.grid_y)

        # Convert grid coordinates to pixel coordinates
        x = screen_x * config.TILE_SIZE
        y = screen_y * config.TILE_SIZE
        size = config.TILE_SIZE

        # Draw building (brown/tan house)
        building_color = (139, 90, 43)  # Brown
        roof_color = (160, 82, 45)  # Saddle brown
        door_color = (101, 67, 33)  # Dark brown
        window_color = (135, 206, 235)  # Sky blue

        # Main building
        pygame.draw.rect(
            self.screen, building_color, (x, y + size // 3, size, size * 2 // 3)
        )

        # Roof (triangle)
        roof_points = [
            (x, y + size // 3),  # Left corner
            (x + size // 2, y),  # Top
            (x + size, y + size // 3),  # Right corner
        ]
        pygame.draw.polygon(self.screen, roof_color, roof_points)

        # Door
        door_width = size // 4
        door_height = size // 3
        door_x = x + size // 2 - door_width // 2
        door_y = y + size - door_height
        pygame.draw.rect(
            self.screen, door_color, (door_x, door_y, door_width, door_height)
        )

        # Windows
        window_size = size // 6
        # Left window
        pygame.draw.rect(
            self.screen,
            window_color,
            (x + size // 6, y + size // 2, window_size, window_size),
        )
        # Right window
        pygame.draw.rect(
            self.screen,
            window_color,
            (x + size * 2 // 3, y + size // 2, window_size, window_size),
        )

        # Sign above door (gold coin symbol)
        sign_size = size // 5
        sign_x = x + size // 2
        sign_y = y + size // 2
        pygame.draw.circle(self.screen, config.GOLD, (sign_x, sign_y), sign_size)
        pygame.draw.circle(
            self.screen, building_color, (sign_x, sign_y), sign_size - 2, 2
        )

        # "Press S" text indicator when player is near
        distance = abs(warrior.grid_x - shop.grid_x) + abs(warrior.grid_y - shop.grid_y)
        if distance <= 1:
            font = pygame.font.Font(None, 20)
            text = font.render("Press S", True, config.WHITE)
            text_x = x + size // 2 - text.get_width() // 2
            text_y = y - 20
            # Draw background for text
            bg_rect = pygame.Rect(
                text_x - 3, text_y - 3, text.get_width() + 6, text.get_height() + 6
            )
            pygame.draw.rect(self.screen, config.BLACK, bg_rect)
            self.screen.blit(text, (text_x, text_y))

    def _draw_message(self, message: str):
        """
        Draw the current message at the bottom of the screen.

        Args:
            message: The message to display
        """
        font = pygame.font.Font(None, 32)
        text_surface = font.render(message, True, config.WHITE)

        # Draw semi-transparent background
        padding = 10
        text_rect = text_surface.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 40)
        )
        bg_rect = text_rect.inflate(padding * 2, padding * 2)

        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surface.set_alpha(200)
        bg_surface.fill(config.BLACK)
        self.screen.blit(bg_surface, bg_rect)

        # Draw text
        self.screen.blit(text_surface, text_rect)

    def _draw_attack_effects_with_camera(self, camera: Camera):
        """
        Draw attack effects with camera offset applied.

        Args:
            camera: The camera instance
        """
        # Temporarily adjust camera offset for attack effects
        # Since attack effects use pixel coordinates, we need to adjust them
        for effect in self.attack_effect_manager.effects:
            # Store original position
            original_x = effect.x
            original_y = effect.y

            # Convert to screen coordinates (effects are in world pixel space)
            # Calculate grid position first
            grid_x = original_x // config.TILE_SIZE
            grid_y = original_y // config.TILE_SIZE

            # Only draw if in camera view
            if camera.is_visible(grid_x, grid_y):
                # Convert to screen space
                screen_grid_x, screen_grid_y = camera.world_to_screen(grid_x, grid_y)
                offset_x = original_x % config.TILE_SIZE
                offset_y = original_y % config.TILE_SIZE
                effect.x = screen_grid_x * config.TILE_SIZE + offset_x
                effect.y = screen_grid_y * config.TILE_SIZE + offset_y

                # Draw the effect
                effect.draw(self.screen)

                # Restore original position
                effect.x = original_x
                effect.y = original_y
