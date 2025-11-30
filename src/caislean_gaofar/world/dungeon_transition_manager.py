"""Manages dungeon transitions and portal mechanics."""

from typing import Callable, Optional, Tuple
from caislean_gaofar.world.camera import Camera
from caislean_gaofar.world.dungeon_manager import DungeonManager
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.entities.entity_manager import EntityManager


class DungeonTransitionManager:
    """Handles dungeon entry/exit and portal transitions."""

    def check_and_handle_transition(
        self,
        warrior: Warrior,
        dungeon_manager: DungeonManager,
        entity_manager: EntityManager,
        on_camera_update: Callable[[int, int], Camera],
        on_message: Callable[[str], None],
    ) -> Tuple[Optional[Camera], bool]:
        """
        Check if player is entering or exiting a dungeon/town and handle the transition.

        Args:
            warrior: The player character
            dungeon_manager: The dungeon manager
            entity_manager: The entity manager for spawning
            on_camera_update: Callback to create new camera (width, height) -> Camera
            on_message: Callback to show messages to player

        Returns:
            Tuple of (new_camera or None, transition_occurred)
        """
        player_x = warrior.grid_x
        player_y = warrior.grid_y

        # Check if exiting town
        if dungeon_manager.check_for_town_exit(player_x, player_y):
            return self._handle_town_exit(
                warrior, dungeon_manager, entity_manager, on_camera_update, on_message
            )

        # Check if exiting dungeon
        if dungeon_manager.check_for_exit(player_x, player_y):
            return self._handle_dungeon_exit(
                warrior, dungeon_manager, entity_manager, on_camera_update, on_message
            )

        # Check if entering town
        if dungeon_manager.check_for_town_entrance(player_x, player_y):
            return self._handle_town_entry(
                warrior,
                dungeon_manager,
                entity_manager,
                on_camera_update,
                on_message,
                player_x,
                player_y,
            )

        # Check if entering dungeon
        dungeon_id = dungeon_manager.get_dungeon_at_position(player_x, player_y)
        if dungeon_id:
            return self._handle_dungeon_entry(
                warrior,
                dungeon_manager,
                entity_manager,
                on_camera_update,
                on_message,
                dungeon_id,
                player_x,
                player_y,
            )

        return None, False

    def _handle_dungeon_exit(
        self,
        warrior: Warrior,
        dungeon_manager: DungeonManager,
        entity_manager: EntityManager,
        on_camera_update: Callable[[int, int], Camera],
        on_message: Callable[[str], None],
    ) -> Tuple[Optional[Camera], bool]:
        """
        Handle exiting a dungeon.

        Args:
            warrior: The player character
            dungeon_manager: The dungeon manager
            entity_manager: The entity manager for spawning
            on_camera_update: Callback to create new camera
            on_message: Callback to show messages

        Returns:
            Tuple of (new_camera or None, transition_occurred)
        """
        return_pos = dungeon_manager.exit_dungeon()
        if return_pos:
            # Update map reference
            world_map = dungeon_manager.get_current_map()

            # Update camera for new map
            new_camera = on_camera_update(world_map.width, world_map.height)

            # Move player to return location
            warrior.grid_x, warrior.grid_y = return_pos

            # Respawn monsters and chests for world map
            entity_manager.spawn_monsters(world_map, dungeon_manager)
            entity_manager.spawn_chests(world_map, dungeon_manager)
            entity_manager.clear_ground_items()

            on_message("You return to the world map.")
            return new_camera, True

        return None, False

    def _handle_dungeon_entry(
        self,
        warrior: Warrior,
        dungeon_manager: DungeonManager,
        entity_manager: EntityManager,
        on_camera_update: Callable[[int, int], Camera],
        on_message: Callable[[str], None],
        dungeon_id: str,
        player_x: int,
        player_y: int,
    ) -> Tuple[Camera, bool]:
        """
        Handle entering a dungeon.

        Args:
            warrior: The player character
            dungeon_manager: The dungeon manager
            entity_manager: The entity manager for spawning
            on_camera_update: Callback to create new camera
            on_message: Callback to show messages
            dungeon_id: ID of the dungeon to enter
            player_x: Player's current x position
            player_y: Player's current y position

        Returns:
            Tuple of (new_camera, transition_occurred)
        """
        # Enter the dungeon
        spawn_x, spawn_y = dungeon_manager.enter_dungeon(dungeon_id, player_x, player_y)

        # Update map reference
        world_map = dungeon_manager.get_current_map()

        # Update camera for new map
        new_camera = on_camera_update(world_map.width, world_map.height)

        # Move player to dungeon spawn
        warrior.grid_x = spawn_x
        warrior.grid_y = spawn_y

        # Spawn monsters and chests for dungeon
        entity_manager.spawn_monsters(world_map, dungeon_manager)
        entity_manager.spawn_chests(world_map, dungeon_manager)
        entity_manager.clear_ground_items()

        # Get dungeon name for message
        for spawn in dungeon_manager.world_map.get_entity_spawns("dungeons"):
            if spawn.get("id") == dungeon_id:
                dungeon_name = spawn.get("name", "dungeon")
                on_message(f"You enter the {dungeon_name}!")
                break

        return new_camera, True

    def _handle_town_entry(
        self,
        warrior: Warrior,
        dungeon_manager: DungeonManager,
        entity_manager: EntityManager,
        on_camera_update: Callable[[int, int], Camera],
        on_message: Callable[[str], None],
        player_x: int,
        player_y: int,
    ) -> Tuple[Camera, bool]:
        """
        Handle entering town from world map.

        Args:
            warrior: The player character
            dungeon_manager: The dungeon manager
            entity_manager: The entity manager for spawning
            on_camera_update: Callback to create new camera
            on_message: Callback to show messages
            player_x: Player's current x position
            player_y: Player's current y position

        Returns:
            Tuple of (new_camera, transition_occurred)
        """
        # Enter the town
        spawn_x, spawn_y = dungeon_manager.enter_town(player_x, player_y)

        # Update map reference
        world_map = dungeon_manager.get_current_map()

        # Update camera for new map
        new_camera = on_camera_update(world_map.width, world_map.height)

        # Move player to town spawn
        warrior.grid_x = spawn_x
        warrior.grid_y = spawn_y

        # Clear monsters and ground items (town is safe)
        entity_manager.monsters.clear()
        entity_manager.chests.clear()
        entity_manager.clear_ground_items()

        on_message("You enter the town!")

        return new_camera, True

    def _handle_town_exit(
        self,
        warrior: Warrior,
        dungeon_manager: DungeonManager,
        entity_manager: EntityManager,
        on_camera_update: Callable[[int, int], Camera],
        on_message: Callable[[str], None],
    ) -> Tuple[Optional[Camera], bool]:
        """
        Handle exiting town to world map.

        Args:
            warrior: The player character
            dungeon_manager: The dungeon manager
            entity_manager: The entity manager for spawning
            on_camera_update: Callback to create new camera
            on_message: Callback to show messages

        Returns:
            Tuple of (new_camera or None, transition_occurred)
        """
        return_pos = dungeon_manager.exit_town()
        if return_pos:
            # Update map reference
            world_map = dungeon_manager.get_current_map()

            # Update camera for new map
            new_camera = on_camera_update(world_map.width, world_map.height)

            # Move player to return location
            warrior.grid_x, warrior.grid_y = return_pos

            # Respawn monsters and chests for world map
            entity_manager.spawn_monsters(world_map, dungeon_manager)
            entity_manager.spawn_chests(world_map, dungeon_manager)
            entity_manager.clear_ground_items()

            on_message("You return to the world map.")
            return new_camera, True

        return None, False
