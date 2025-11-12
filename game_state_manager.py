"""Game state management system."""

from typing import Optional, Tuple
from portal import Portal
from warrior import Warrior
import config


class GameStateManager:
    """Tracks game state and manages state transitions."""

    def __init__(self):
        """Initialize the game state manager."""
        self.state = config.STATE_PLAYING

        # Message system
        self.message = ""
        self.message_timer = 0
        self.message_duration = 3000  # milliseconds to show message

        # Portal system
        self.active_portal: Optional[Portal] = None  # Portal in dungeon/world
        self.return_portal: Optional[Portal] = None  # Portal in shop
        self.portal_return_location: Optional[Tuple[str, int, int]] = None
        self.portal_cooldown = 0  # Prevent instant re-teleportation

    def update(self, clock, warrior: Warrior, dt: float):
        """
        Update state manager timers and animations.

        Args:
            clock: The pygame clock
            warrior: The warrior entity
            dt: Delta time since last update
        """
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= clock.get_time()
            if self.message_timer <= 0:
                self.message = ""

        # Update portal cooldown timer
        if self.portal_cooldown > 0:
            self.portal_cooldown -= clock.get_time()

        # Update portal animations
        if self.active_portal:
            self.active_portal.update(dt)
        if self.return_portal:
            self.return_portal.update(dt)

    def show_message(self, message: str):
        """
        Show a message to the player.

        Args:
            message: The message to display
        """
        self.message = message
        self.message_timer = self.message_duration

    def use_town_portal(self, warrior: Warrior, dungeon_manager) -> Tuple[bool, str]:
        """
        Use a town portal to teleport to town.

        Args:
            warrior: The warrior using the portal
            dungeon_manager: The dungeon manager

        Returns:
            Tuple of (success: bool, message: str)
        """
        portal_count = warrior.count_town_portals()

        if warrior.use_town_portal():
            # Close any existing portals
            self.close_portals()

            # Save current location
            current_map_id = dungeon_manager.current_map_id
            self.portal_return_location = (
                current_map_id,
                warrior.grid_x,
                warrior.grid_y,
            )

            # Create portal at current location
            self.active_portal = Portal(warrior.grid_x, warrior.grid_y, False)

            # Switch to town map
            dungeon_manager.current_map_id = "town"

            # Teleport to town spawn point (caller will update world_map and camera)
            world_map = dungeon_manager.get_current_map()
            spawn_x, spawn_y = world_map.spawn_point
            # Place player one tile to the right of portal to avoid standing on it
            warrior.grid_x, warrior.grid_y = spawn_x + 1, spawn_y

            # Create return portal at spawn location
            self.return_portal = Portal(spawn_x, spawn_y, True)

            # Stay in playing state (on town map)
            self.state = config.STATE_PLAYING

            # Set cooldown to prevent instant re-teleportation (500ms)
            self.portal_cooldown = 500

            return True, "You enter the portal and arrive in town!"
        else:
            if portal_count <= 0:
                return False, "No town portals in inventory!"
            else:
                return (
                    False,
                    f"You have {portal_count} portal(s) but cannot use them here!",
                )

    def use_return_portal(self, warrior: Warrior, dungeon_manager) -> Tuple[bool, str]:
        """
        Use the return portal to go back to saved location.

        Args:
            warrior: The warrior using the portal
            dungeon_manager: The dungeon manager

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.return_portal or not self.portal_return_location:
            return False, "No return portal available!"

        map_id, grid_x, grid_y = self.portal_return_location

        # Switch to the saved map (caller will update world_map and camera)
        if map_id != dungeon_manager.current_map_id:
            dungeon_manager.current_map_id = map_id

        # Return to saved position
        warrior.grid_x = grid_x
        warrior.grid_y = grid_y

        # Return to playing state
        self.state = config.STATE_PLAYING

        # Set cooldown to prevent instant re-teleportation (500ms)
        self.portal_cooldown = 500

        # Close both portals
        self.close_portals()

        return True, "You return through the portal!"

    def check_return_portal_collision(self, warrior: Warrior) -> bool:
        """
        Check if warrior stepped on return portal.

        Args:
            warrior: The warrior to check

        Returns:
            True if warrior is on return portal
        """
        if self.return_portal and self.portal_cooldown <= 0:
            if (
                warrior.grid_x == self.return_portal.grid_x
                and warrior.grid_y == self.return_portal.grid_y
            ):
                return True
        return False

    def close_portals(self):
        """Close all active portals."""
        self.active_portal = None
        self.return_portal = None
        self.portal_return_location = None

    def transition_to_inventory(self):
        """Transition to inventory state."""
        if self.state in [config.STATE_PLAYING, config.STATE_SHOP]:
            self.state = config.STATE_INVENTORY

    def transition_from_inventory(self):
        """Transition from inventory state back to previous state."""
        if self.state == config.STATE_INVENTORY:
            # Check if we came from shop by checking portal location
            if self.return_portal:
                self.state = config.STATE_SHOP
            else:
                self.state = config.STATE_PLAYING

    def transition_to_shop(self, is_near_shop: bool) -> bool:
        """
        Transition to shop state.

        Args:
            is_near_shop: Whether the player is near the shop

        Returns:
            True if transition was successful
        """
        if self.state == config.STATE_PLAYING and is_near_shop:
            self.state = config.STATE_SHOP
            return True
        return False

    def transition_from_shop(self):
        """Transition from shop state back to playing state."""
        if self.state == config.STATE_SHOP:
            self.state = config.STATE_PLAYING

    def transition_to_game_over(self):
        """Transition to game over state."""
        self.state = config.STATE_GAME_OVER
        self.close_portals()

    def reset(self):
        """Reset state manager to initial state."""
        self.state = config.STATE_PLAYING
        self.message = ""
        self.message_timer = 0
        self.close_portals()
