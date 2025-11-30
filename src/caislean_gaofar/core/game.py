"""Main game class - thin facade coordinating game components."""

from typing import TYPE_CHECKING

from caislean_gaofar.objects.item import Item
from caislean_gaofar.objects.ground_item import GroundItem
from caislean_gaofar.world.camera import Camera

# Import coordinator and initializer classes
from caislean_gaofar.core.game_initializer import GameInitializer
from caislean_gaofar.core.game_state_coordinator import GameStateCoordinator
from caislean_gaofar.core.game_render_coordinator import GameRenderCoordinator
from caislean_gaofar.utils.event_context import EventContext

if TYPE_CHECKING:
    from caislean_gaofar.world.world_map import WorldMap


class Game:
    """Thin facade that coordinates game components."""

    def __init__(self, map_file: str | None = None):
        """
        Initialize the game by delegating to GameInitializer.

        Args:
            map_file: Optional path to map JSON file. If None, uses default map.
        """
        # Initialize all subsystems using GameInitializer
        initializer = GameInitializer(map_file)
        components = initializer.initialize()

        # Store component references (assert non-None for type checker)
        assert components.screen is not None
        assert components.clock is not None
        assert components.entity_manager is not None
        assert components.turn_processor is not None
        assert components.renderer is not None
        assert components.state_manager is not None
        assert components.event_dispatcher is not None
        assert components.game_loop is not None
        assert components.dungeon_transition_manager is not None
        assert components.dungeon_manager is not None
        assert components.world_map is not None
        assert components.camera is not None
        assert components.fog_of_war is not None
        assert components.warrior is not None
        assert components.shop is not None
        assert components.temple is not None
        assert components.skill_ui is not None

        self.screen = components.screen
        self.clock = components.clock
        self.entity_manager = components.entity_manager
        self.turn_processor = components.turn_processor
        self.renderer = components.renderer
        self.state_manager = components.state_manager
        self.event_dispatcher = components.event_dispatcher
        self.game_loop = components.game_loop
        self.dungeon_transition_manager = components.dungeon_transition_manager
        self.dungeon_manager = components.dungeon_manager
        self.world_map = components.world_map
        self.camera = components.camera
        self.fog_of_war = components.fog_of_war
        self.warrior = components.warrior
        self.shop = components.shop
        self.temple = components.temple
        self.skill_ui = components.skill_ui

        # Initialize coordinators
        self.state_coordinator = GameStateCoordinator(
            state_manager=self.state_manager,
            turn_processor=self.turn_processor,
            entity_manager=self.entity_manager,
            dungeon_transition_manager=self.dungeon_transition_manager,
            renderer=self.renderer,
        )

        self.render_coordinator = GameRenderCoordinator(
            screen=self.screen,
            renderer=self.renderer,
            skill_ui=self.skill_ui,
            state_manager=self.state_manager,
        )

    def drop_item(self, item: Item, grid_x: int, grid_y: int):
        """
        Drop an item on the ground at specified grid coordinates.

        Args:
            item: The item to drop
            grid_x: Grid x position
            grid_y: Grid y position
        """
        self.entity_manager.drop_item(item, grid_x, grid_y)

    def get_item_at_position(self, grid_x: int, grid_y: int) -> GroundItem | None:
        """
        Get the item at a specific position.

        Args:
            grid_x: Grid x position
            grid_y: Grid y position

        Returns:
            GroundItem if found, None otherwise
        """
        return self.entity_manager.get_item_at_position(grid_x, grid_y)

    def pickup_item_at_position(self, grid_x: int, grid_y: int) -> bool:
        """
        Try to pick up an item at the specified grid position.

        Args:
            grid_x: Grid x position
            grid_y: Grid y position

        Returns:
            True if an item was picked up, False otherwise
        """
        success, message = self.entity_manager.pickup_item_at_position(
            grid_x, grid_y, self.warrior
        )
        if message:
            self._show_message(message)
        return success

    def handle_events(self):
        """Handle pygame events."""
        # Create event context
        ctx = EventContext(
            warrior=self.warrior,
            game_state_manager=self.state_manager,
            turn_processor=self.turn_processor,
            entity_manager=self.entity_manager,
            inventory_ui=self.renderer.inventory_ui,
            shop=self.shop,
            shop_ui=self.renderer.shop_ui,
            skill_ui=self.skill_ui,
            dungeon_manager=self.dungeon_manager,
            on_restart=self.restart,
            on_save=self.save_game,
            on_pickup_item=self._handle_pickup_item,
            on_use_potion=self._handle_use_potion,
            on_use_town_portal=self._handle_use_town_portal,
            on_use_return_portal=self._handle_use_return_portal,
            on_shop_check=self._handle_shop_check,
            inventory_game_ref=self,
        )

        # Use event dispatcher for all event handling
        self.event_dispatcher.handle_events(ctx)

    def restart(self):
        """Restart the game by delegating to GameStateCoordinator."""
        # Delegate restart to state coordinator
        self.warrior, self.camera, self.world_map = self.state_coordinator.restart(
            warrior=self.warrior,
            dungeon_manager=self.dungeon_manager,
            camera=self.camera,
            world_map=self.world_map,
        )

        # Add starting items to new warrior using initializer
        initializer = GameInitializer()
        initializer._add_starting_items(self.warrior)

    def update(self, dt: float):
        """
        Update game state by delegating to GameStateCoordinator.

        Args:
            dt: Delta time since last update
        """
        # Delegate to state coordinator and get potentially updated state
        self.camera, self.world_map = self.state_coordinator.update(
            clock=self.clock,
            warrior=self.warrior,
            camera=self.camera,
            dungeon_manager=self.dungeon_manager,
            fog_of_war=self.fog_of_war,
            temple=self.temple,
            world_map=self.world_map,
            dt=dt,
        )

        # Check for dungeon transitions after turn processing
        self._check_dungeon_transition()

    def _check_dungeon_transition(self):
        """Check if player is entering or exiting a dungeon."""
        new_camera, transition_occurred = (
            self.dungeon_transition_manager.check_and_handle_transition(
                warrior=self.warrior,
                dungeon_manager=self.dungeon_manager,
                entity_manager=self.entity_manager,
                on_camera_update=self._create_camera,
                on_message=self._show_message,
            )
        )

        if transition_occurred and new_camera:
            self.camera = new_camera
            self.world_map = self.dungeon_manager.get_current_map()

    def _create_camera(self, width: int, height: int) -> Camera:
        """
        Create a new camera with the given dimensions.

        Args:
            width: Camera width
            height: Camera height

        Returns:
            New Camera instance
        """
        return Camera(width, height)

    def _handle_pickup_item(self, grid_x: int, grid_y: int):
        """
        Handle pickup item event.

        Args:
            grid_x: Grid x position
            grid_y: Grid y position
        """
        self.pickup_item_at_position(grid_x, grid_y)

    def _handle_use_potion(self):
        """Handle use potion event."""
        if self.warrior.use_health_potion():
            self.renderer.hud.trigger_potion_glow()
            self._show_message("Used health potion! +30 HP")
        else:
            if self.warrior.count_health_potions() <= 0:
                self._show_message("No health potions remaining!")
            else:
                self._show_message("Health is already full!")

    def _handle_use_town_portal(self):
        """Handle use town portal event."""
        success, message = self.state_manager.use_town_portal(
            self.warrior,
            self.dungeon_manager,
        )

        if success:
            # Update references after portal use
            self.world_map = self.dungeon_manager.get_current_map()
            self.camera = Camera(self.world_map.width, self.world_map.height)
            # Clear chests when entering town
            self.entity_manager.chests = []

        self._show_message(message)

    def _handle_use_return_portal(self):
        """Handle use return portal event."""
        success, message = self.state_manager.use_return_portal(
            self.warrior,
            self.dungeon_manager,
        )

        if success:
            # Update references after portal use
            self.world_map = self.dungeon_manager.get_current_map()
            self.camera = Camera(self.world_map.width, self.world_map.height)
            # Respawn chests when returning from town
            if self.dungeon_manager.current_map_id != "town":
                self.entity_manager.spawn_chests(self.world_map, self.dungeon_manager)

        self._show_message(message)

    def _handle_shop_check(self) -> tuple[bool, str]:
        """
        Handle shop proximity check.

        Returns:
            Tuple of (is_near: bool, message: str)
        """
        if self.dungeon_manager.current_map_id == "town" and self._is_near_shop():
            return True, ""
        else:
            return False, "No shop nearby!"

    def _show_message(self, message: str):
        """Show a message to the player."""
        self.state_manager.show_message(message)

    def _is_near_shop(self) -> bool:
        """
        Check if player is near the shop.

        Returns:
            True if player is within 1 tile of shop
        """
        distance = abs(self.warrior.grid_x - self.shop.grid_x) + abs(
            self.warrior.grid_y - self.shop.grid_y
        )
        return distance <= 1

    def _heal_at_temple(self):
        """Heal the warrior at the temple (delegates to GameStateCoordinator)."""
        self.state_coordinator._heal_at_temple(self.warrior, self.temple)

    def process_turn(self):
        """Process one complete turn (delegates to GameStateCoordinator)."""
        self.state_coordinator._process_turn(
            warrior=self.warrior,
            dungeon_manager=self.dungeon_manager,
            world_map=self.world_map,
            camera=self.camera,
            fog_of_war=self.fog_of_war,
            temple=self.temple,
        )

    def _handle_chest_opened(self, item: Item):
        """Handle chest opened event (delegates to GameStateCoordinator)."""
        self.state_coordinator._handle_chest_opened(item)

    def _handle_monster_death(self, loot_item: Item, monster_type: str, xp_value: int):
        """Handle monster death event (delegates to GameStateCoordinator)."""
        self.state_coordinator._handle_monster_death(
            self.warrior, loot_item, monster_type, xp_value
        )

    def draw(self):
        """Draw all game objects by delegating to GameRenderCoordinator."""
        # Type assertion: world_map is guaranteed to be WorldMap after initialization
        world_map: "WorldMap" = self.world_map  # type: ignore[assignment]
        self.render_coordinator.render(
            world_map=world_map,
            camera=self.camera,
            entity_manager=self.entity_manager,
            warrior=self.warrior,
            dungeon_manager=self.dungeon_manager,
            shop=self.shop,
            temple=self.temple,
            fog_of_war=self.fog_of_war,
        )

    def draw_game_over_screen(self, message: str, color: tuple):
        """
        Draw game over or victory screen by delegating to GameRenderCoordinator.

        Args:
            message: Message to display
            color: Color of the message
        """
        self.render_coordinator.draw_game_over_screen(message, color)

    def save_game(self, filename: str = "quicksave") -> bool:
        """
        Save the current game state.

        Args:
            filename: Name of the save file

        Returns:
            True if save was successful
        """
        from caislean_gaofar.systems.save_game import SaveGame

        success = SaveGame.save_game(self, filename)
        if success:
            self._show_message(f"Game saved: {filename}")
        else:
            self._show_message("Failed to save game")
        return success

    def load_game_state(self, save_data: dict):
        """
        Load game state from save data.

        Args:
            save_data: Dictionary containing saved game state
        """
        from caislean_gaofar.systems.save_game import SaveGame

        # Load player state
        player_data = save_data["player"]
        self.warrior.grid_x = player_data["grid_x"]
        self.warrior.grid_y = player_data["grid_y"]
        self.warrior.health = player_data["health"]
        self.warrior.max_health = player_data["max_health"]
        self.warrior.gold = player_data["gold"]
        self.warrior.inventory = SaveGame.deserialize_inventory(
            player_data["inventory"]
        )

        # Load map state
        self.dungeon_manager.current_map_id = save_data["current_map_id"]
        self.dungeon_manager.return_location = save_data.get("return_location")
        self.world_map = self.dungeon_manager.get_current_map()

        # Update camera for loaded map
        self.camera = Camera(self.world_map.width, self.world_map.height)

        # Load tracking lists
        self.entity_manager.killed_monsters = save_data.get("killed_monsters", [])
        self.entity_manager.opened_chests = save_data.get("opened_chests", [])

        # Spawn monsters and chests (will filter out killed/opened ones)
        self.entity_manager.spawn_monsters(self.world_map, self.dungeon_manager)
        self.entity_manager.spawn_chests(self.world_map, self.dungeon_manager)

        # Load ground items for current map
        current_map_id = self.dungeon_manager.current_map_id
        self.entity_manager.ground_items = []
        for gi_data in save_data.get("ground_items", []):
            if gi_data["map_id"] == current_map_id:
                item = SaveGame.deserialize_item(gi_data["item"])
                ground_item = GroundItem(item, gi_data["grid_x"], gi_data["grid_y"])
                self.entity_manager.ground_items.append(ground_item)

        # Reset game state
        self.state_manager.reset()
        self.turn_processor.reset()

    def run(self):
        """Main game loop."""

        # Synchronize running state between event_dispatcher and game_loop
        def handle_events_wrapper():
            self.handle_events()
            # If event_dispatcher stops, stop game_loop too
            if not self.event_dispatcher.running:
                self.game_loop.stop()

        self.game_loop.run(
            handle_events=handle_events_wrapper,
            update=self.update,
            draw=self.draw,
        )
