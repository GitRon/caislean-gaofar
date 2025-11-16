"""Game state coordinator - manages game state transitions and updates."""

import pygame
from caislean_gaofar.core import config
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.entities.entity_manager import EntityManager
from caislean_gaofar.systems.turn_processor import TurnProcessor
from caislean_gaofar.world.camera import Camera
from caislean_gaofar.world.dungeon_manager import DungeonManager
from caislean_gaofar.world.fog_of_war import FogOfWar
from caislean_gaofar.objects.temple import Temple
from caislean_gaofar.core.game_state_manager import GameStateManager
from caislean_gaofar.world.world_renderer import WorldRenderer
from caislean_gaofar.world.dungeon_transition_manager import DungeonTransitionManager
from caislean_gaofar.objects.item import Item


class GameStateCoordinator:
    """Coordinates game state transitions and updates."""

    def __init__(
        self,
        state_manager: GameStateManager,
        turn_processor: TurnProcessor,
        entity_manager: EntityManager,
        dungeon_transition_manager: DungeonTransitionManager,
        renderer: WorldRenderer,
    ):
        """
        Initialize the state coordinator.

        Args:
            state_manager: GameStateManager instance
            turn_processor: TurnProcessor instance
            entity_manager: EntityManager instance
            dungeon_transition_manager: DungeonTransitionManager instance
            renderer: WorldRenderer instance
        """
        self.state_manager = state_manager
        self.turn_processor = turn_processor
        self.entity_manager = entity_manager
        self.dungeon_transition_manager = dungeon_transition_manager
        self.renderer = renderer

    def update(
        self,
        clock: pygame.time.Clock,
        warrior: Warrior,
        camera: Camera,
        dungeon_manager: DungeonManager,
        fog_of_war: FogOfWar,
        temple: Temple,
        world_map,
        dt: float,
    ) -> tuple[Camera, object]:
        """
        Update game state.

        Args:
            clock: Pygame clock
            warrior: Warrior instance
            camera: Camera instance
            dungeon_manager: DungeonManager instance
            fog_of_war: FogOfWar instance
            temple: Temple instance
            world_map: Current world map
            dt: Delta time since last update

        Returns:
            Tuple of (updated_camera, updated_world_map)
        """
        # Update state manager (messages, portals, etc.)
        self.state_manager.update(clock, warrior, dt)

        # Update HUD (always update for animations)
        self.renderer.hud.update(warrior, dt)

        # Update temple animation
        if temple:
            temple.update(dt)

        # Update attack effects
        self.renderer.attack_effect_manager.update(dt)

        # Only update game logic when actively playing
        if self.state_manager.state != config.STATE_PLAYING:
            return camera, world_map

        # Process turn if player has queued an action
        if not self.turn_processor.waiting_for_player_input:
            self._process_turn(
                warrior, dungeon_manager, world_map, camera, fog_of_war, temple
            )
            # Get potentially updated camera and world_map after turn processing
            camera, world_map = self._get_updated_world_state(
                camera, world_map, dungeon_manager
            )

        # Update camera to follow player
        camera.update(warrior.grid_x, warrior.grid_y)

        # Update fog of war based on player position
        fog_of_war.update_visibility(
            warrior.grid_x,
            warrior.grid_y,
            dungeon_manager.current_map_id,
        )

        # Check if player stepped on return portal (auto-teleport back)
        if self.state_manager.check_return_portal_collision(warrior):
            camera, world_map = self._handle_return_portal(
                warrior, dungeon_manager, camera
            )
            return camera, world_map

        # Check if player stepped on temple (heal to max HP)
        if (
            dungeon_manager.current_map_id == "town"
            and warrior.grid_x == temple.grid_x
            and warrior.grid_y == temple.grid_y
        ):
            self._heal_at_temple(warrior, temple)

        # Check game over conditions
        if not warrior.is_alive:
            self.state_manager.transition_to_game_over()

        return camera, world_map

    def _process_turn(
        self,
        warrior: Warrior,
        dungeon_manager: DungeonManager,
        world_map,
        camera: Camera,
        fog_of_war: FogOfWar,
        temple: Temple,
    ):
        """
        Process one complete turn (hero then monsters).

        Args:
            warrior: Warrior instance
            dungeon_manager: DungeonManager instance
            world_map: Current world map
            camera: Camera instance
            fog_of_war: FogOfWar instance
            temple: Temple instance
        """
        # Store callbacks for turn processor
        def on_dungeon_transition():
            # This will be handled in _get_updated_world_state
            pass

        def on_chest_opened(item: Item):
            self._handle_chest_opened(item)

        def on_item_picked(message: str):
            self._show_message(message)

        def on_monster_death(loot_item: Item, monster_type: str, xp_value: int):
            self._handle_monster_death(warrior, loot_item, monster_type, xp_value)

        self.turn_processor.process_turn(
            warrior=warrior,
            entity_manager=self.entity_manager,
            world_map=world_map,
            dungeon_manager=dungeon_manager,
            on_dungeon_transition=on_dungeon_transition,
            on_chest_opened=on_chest_opened,
            on_item_picked=on_item_picked,
            on_monster_death=on_monster_death,
            attack_effect_manager=self.renderer.attack_effect_manager,
        )

    def _get_updated_world_state(
        self, camera: Camera, world_map, dungeon_manager: DungeonManager
    ) -> tuple[Camera, object]:
        """
        Check for dungeon transitions and update world state.

        Args:
            camera: Current camera
            world_map: Current world map
            dungeon_manager: DungeonManager instance

        Returns:
            Tuple of (updated_camera, updated_world_map)
        """
        # Get warrior from turn processor context if available
        # For now, we'll handle this in the Game class
        return camera, world_map

    def _handle_chest_opened(self, item: Item):
        """
        Handle chest opened event.

        Args:
            item: The item found in the chest
        """
        self._show_message(f"You open the chest. Inside you find a {item.name}!")

    def _handle_monster_death(
        self, warrior: Warrior, loot_item: Item, monster_type: str, xp_value: int
    ):
        """
        Handle monster death event.

        Args:
            warrior: Warrior instance
            loot_item: The loot item dropped
            monster_type: The type of monster that died
            xp_value: Experience points awarded
        """
        # Award experience points
        leveled_up = warrior.gain_experience(xp_value)

        # Show appropriate message
        if leveled_up:
            self._show_message(
                f"Level Up! Now level {warrior.experience.current_level}! The {monster_type.replace('_', ' ')} drops a {loot_item.name}! (+{xp_value} XP)"
            )
        else:
            self._show_message(
                f"The {monster_type.replace('_', ' ')} drops a {loot_item.name}! (+{xp_value} XP)"
            )

    def _show_message(self, message: str):
        """
        Show a message to the player.

        Args:
            message: Message to display
        """
        self.state_manager.show_message(message)

    def _heal_at_temple(self, warrior: Warrior, temple: Temple):
        """
        Heal the warrior to maximum HP when stepping on the temple.

        Args:
            warrior: Warrior instance
            temple: Temple instance
        """
        if warrior.health < warrior.max_health:
            # Heal to max HP
            warrior.health = warrior.max_health
            # Activate healing visual effect
            temple.activate_healing()
            self._show_message("The temple's divine power restores your health!")

    def _handle_return_portal(
        self, warrior: Warrior, dungeon_manager: DungeonManager, camera: Camera
    ) -> tuple[Camera, object]:
        """
        Handle return portal usage.

        Args:
            warrior: Warrior instance
            dungeon_manager: DungeonManager instance
            camera: Current camera

        Returns:
            Tuple of (updated_camera, updated_world_map)
        """
        success, message = self.state_manager.use_return_portal(
            warrior,
            dungeon_manager,
        )

        if success:
            # Update references after portal use
            world_map = dungeon_manager.get_current_map()
            camera = Camera(world_map.width, world_map.height)
            # Respawn chests when returning from town
            if dungeon_manager.current_map_id != "town":
                self.entity_manager.spawn_chests(world_map, dungeon_manager)
        else:
            world_map = dungeon_manager.get_current_map()

        self._show_message(message)
        return camera, world_map

    def restart(
        self,
        warrior: Warrior,
        dungeon_manager: DungeonManager,
        camera: Camera,
        world_map,
    ) -> tuple[Warrior, Camera, object]:
        """
        Restart the game.

        Args:
            warrior: Current warrior instance
            dungeon_manager: DungeonManager instance
            camera: Current camera
            world_map: Current world map

        Returns:
            Tuple of (new_warrior, new_camera, new_world_map)
        """
        # Import here to avoid circular dependency
        from caislean_gaofar.entities.warrior import Warrior

        # Close any active portals
        self.state_manager.close_portals()

        # Reset to world map
        dungeon_manager.current_map_id = "world"
        dungeon_manager.return_location = None
        world_map = dungeon_manager.get_current_map()

        # Update camera for new map
        camera = Camera(world_map.width, world_map.height)

        spawn_x, spawn_y = world_map.spawn_point
        warrior = Warrior(spawn_x, spawn_y)

        # Reset managers
        self.state_manager.reset()
        self.turn_processor.reset()
        self.entity_manager.reset_tracking()

        # Respawn entities
        self.entity_manager.spawn_monsters(world_map, dungeon_manager)
        self.entity_manager.spawn_chests(world_map, dungeon_manager)
        self.entity_manager.clear_ground_items()

        return warrior, camera, world_map
