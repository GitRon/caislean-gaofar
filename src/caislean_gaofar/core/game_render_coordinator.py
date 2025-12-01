"""Game render coordinator - orchestrates rendering across different game states."""

import pygame
from caislean_gaofar.core import config
from caislean_gaofar.world.world_renderer import WorldRenderer
from caislean_gaofar.entities.entity_manager import EntityManager
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.world.world_map import WorldMap
from caislean_gaofar.world.camera import Camera
from caislean_gaofar.world.dungeon_manager import DungeonManager
from caislean_gaofar.objects.shop import Shop
from caislean_gaofar.objects.temple import Temple
from caislean_gaofar.objects.library import Library
from caislean_gaofar.world.fog_of_war import FogOfWar
from caislean_gaofar.ui.skill_ui import SkillUI
from caislean_gaofar.core.game_state_manager import GameStateManager


class GameRenderCoordinator:
    """Coordinates rendering across different game states."""

    def __init__(
        self,
        screen: pygame.Surface,
        renderer: WorldRenderer,
        skill_ui: SkillUI,
        state_manager: GameStateManager,
    ):
        """
        Initialize the render coordinator.

        Args:
            screen: Pygame screen surface
            renderer: WorldRenderer instance
            skill_ui: SkillUI instance
            state_manager: GameStateManager instance
        """
        self.screen = screen
        self.renderer = renderer
        self.skill_ui = skill_ui
        self.state_manager = state_manager

    def render(
        self,
        world_map: WorldMap,
        camera: Camera,
        entity_manager: EntityManager,
        warrior: Warrior,
        dungeon_manager: DungeonManager,
        shop: Shop,
        temple: Temple,
        library: Library,
        fog_of_war: FogOfWar,
    ):
        """
        Render the current game state.

        Args:
            world_map: Current world map
            camera: Camera instance
            entity_manager: EntityManager instance
            warrior: Warrior instance
            dungeon_manager: DungeonManager instance
            shop: Shop instance
            temple: Temple instance
            library: Library instance
            fog_of_war: FogOfWar instance
        """
        state = self.state_manager.state

        if state == config.STATE_PLAYING:
            self._render_playing_state(
                world_map,
                camera,
                entity_manager,
                warrior,
                dungeon_manager,
                shop,
                temple,
                library,
                fog_of_war,
            )
        elif state == config.STATE_INVENTORY:
            self._render_inventory_state(
                world_map, camera, entity_manager, warrior, fog_of_war, dungeon_manager
            )
        elif state == config.STATE_SHOP:
            self._render_shop_state(shop, warrior)
        elif state == config.STATE_SKILLS:
            self._render_skills_state(warrior)
        elif state == config.STATE_GAME_OVER:
            self._render_game_over_state()

    def _render_playing_state(
        self,
        world_map: WorldMap,
        camera: Camera,
        entity_manager: EntityManager,
        warrior: Warrior,
        dungeon_manager: DungeonManager,
        shop: Shop,
        temple: Temple,
        library: Library,
        fog_of_war: FogOfWar,
    ):
        """
        Render the playing state.

        Args:
            world_map: Current world map
            camera: Camera instance
            entity_manager: EntityManager instance
            warrior: Warrior instance
            dungeon_manager: DungeonManager instance
            shop: Shop instance
            temple: Temple instance
            library: Library instance
            fog_of_war: FogOfWar instance
        """
        self.renderer.draw_playing_state(
            world_map=world_map,
            camera=camera,
            entity_manager=entity_manager,
            warrior=warrior,
            dungeon_manager=dungeon_manager,
            shop=shop,
            active_portal=self.state_manager.active_portal,
            return_portal=self.state_manager.return_portal,
            message=self.state_manager.message,
            fog_of_war=fog_of_war,
            temple=temple,
            library=library,
        )

    def _render_inventory_state(
        self,
        world_map: WorldMap,
        camera: Camera,
        entity_manager: EntityManager,
        warrior: Warrior,
        fog_of_war: FogOfWar,
        dungeon_manager: DungeonManager,
    ):
        """
        Render the inventory state.

        Args:
            world_map: Current world map
            camera: Camera instance
            entity_manager: EntityManager instance
            warrior: Warrior instance
            fog_of_war: FogOfWar instance
            dungeon_manager: DungeonManager instance
        """
        self.renderer.draw_inventory_state(
            world_map=world_map,
            camera=camera,
            entity_manager=entity_manager,
            warrior=warrior,
            fog_of_war=fog_of_war,
            dungeon_manager=dungeon_manager,
        )

    def _render_shop_state(self, shop: Shop, warrior: Warrior):
        """
        Render the shop state.

        Args:
            shop: Shop instance
            warrior: Warrior instance
        """
        self.renderer.draw_shop_state(shop=shop, warrior=warrior)

    def _render_skills_state(self, warrior: Warrior):
        """
        Render the skills state.

        Args:
            warrior: Warrior instance
        """
        self.skill_ui.draw(self.screen, warrior)
        pygame.display.flip()

    def _render_game_over_state(self):
        """Render the game over state."""
        self.renderer.draw_game_over_state("GAME OVER!", config.RED)

    def draw_game_over_screen(self, message: str, color: tuple):
        """
        Draw game over or victory screen with custom message.

        Args:
            message: Message to display
            color: Color of the message
        """
        self.renderer.draw_game_over_state(message, color)
