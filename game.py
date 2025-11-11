"""Main game class and game loop."""

import pygame
import os
from warrior import Warrior
from shop import Shop
from skill_ui import SkillUI
from item import Item, ItemType
from camera import Camera
from ground_item import GroundItem
from dungeon_manager import DungeonManager
from fog_of_war import FogOfWar
import config

# Import new component classes
from entity_manager import EntityManager
from turn_processor import TurnProcessor
from world_renderer import WorldRenderer
from game_state_manager import GameStateManager
from event_dispatcher import EventDispatcher


class Game:
    """Main game class that manages the game loop and state."""

    def __init__(self, map_file: str = None):
        """
        Initialize the game.

        Args:
            map_file: Optional path to map JSON file. If None, uses default map.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()

        # Initialize new component systems
        self.entity_manager = EntityManager()
        self.turn_processor = TurnProcessor()
        self.renderer = WorldRenderer(self.screen)
        self.state_manager = GameStateManager()
        self.event_dispatcher = EventDispatcher()

        # Initialize dungeon manager
        if map_file is None:
            map_file = os.path.join("maps", "overworld.json")
        self.dungeon_manager = DungeonManager(map_file)
        self.dungeon_manager.load_world_map()

        # Load dungeons
        self.dungeon_manager.load_dungeon(
            "dark_cave", os.path.join("maps", "dark_cave.json")
        )
        self.dungeon_manager.load_dungeon(
            "ancient_castle", os.path.join("maps", "ancient_castle.json")
        )
        self.dungeon_manager.load_dungeon("town", os.path.join("maps", "town.json"))

        # Get current map (initially world map)
        self.world_map = self.dungeon_manager.get_current_map()

        # Initialize camera
        self.camera = Camera(self.world_map.width, self.world_map.height)

        # Initialize game objects at spawn point
        spawn_x, spawn_y = self.world_map.spawn_point
        self.warrior = Warrior(spawn_x, spawn_y)

        # Add starting items to warrior inventory
        self._add_starting_items()

        # Initialize fog of war (2 tile visibility radius)
        self.fog_of_war = FogOfWar(visibility_radius=2)

        # Initialize skill UI (separate from renderer since it's a full-screen UI)
        self.skill_ui = SkillUI()

        # Initialize shop (located at specific position on town map)
        self.shop = Shop(grid_x=4, grid_y=3)  # Position in town

        # Spawn monsters and chests
        self.entity_manager.spawn_monsters(self.world_map, self.dungeon_manager)
        self.entity_manager.spawn_chests(self.world_map, self.dungeon_manager)

    @property
    def running(self):
        """Get running state from event dispatcher."""
        return self.event_dispatcher.running

    @running.setter
    def running(self, value):
        """Set running state on event dispatcher."""
        self.event_dispatcher.running = value

    @property
    def state(self):
        """Get current game state from state manager."""
        return self.state_manager.state

    @state.setter
    def state(self, value):
        """Set game state on state manager."""
        self.state_manager.state = value

    @property
    def waiting_for_player_input(self):
        """Get waiting for input state from turn processor."""
        return self.turn_processor.waiting_for_player_input

    @waiting_for_player_input.setter
    def waiting_for_player_input(self, value):
        """Set waiting for input state on turn processor."""
        self.turn_processor.waiting_for_player_input = value

    @property
    def monsters(self):
        """Get monsters list from entity manager."""
        return self.entity_manager.monsters

    @monsters.setter
    def monsters(self, value):
        """Set monsters list on entity manager."""
        self.entity_manager.monsters = value

    @property
    def chests(self):
        """Get chests list from entity manager."""
        return self.entity_manager.chests

    @chests.setter
    def chests(self, value):
        """Set chests list on entity manager."""
        self.entity_manager.chests = value

    @property
    def ground_items(self):
        """Get ground items list from entity manager."""
        return self.entity_manager.ground_items

    @ground_items.setter
    def ground_items(self, value):
        """Set ground items list on entity manager."""
        self.entity_manager.ground_items = value

    @property
    def killed_monsters(self):
        """Get killed monsters list from entity manager."""
        return self.entity_manager.killed_monsters

    @killed_monsters.setter
    def killed_monsters(self, value):
        """Set killed monsters list on entity manager."""
        self.entity_manager.killed_monsters = value

    @property
    def opened_chests(self):
        """Get opened chests list from entity manager."""
        return self.entity_manager.opened_chests

    @opened_chests.setter
    def opened_chests(self, value):
        """Set opened chests list on entity manager."""
        self.entity_manager.opened_chests = value

    @property
    def message(self):
        """Get message from state manager."""
        return self.state_manager.message

    @message.setter
    def message(self, value):
        """Set message on state manager."""
        self.state_manager.message = value

    @property
    def message_timer(self):
        """Get message timer from state manager."""
        return self.state_manager.message_timer

    @message_timer.setter
    def message_timer(self, value):
        """Set message timer on state manager."""
        self.state_manager.message_timer = value

    @property
    def active_portal(self):
        """Get active portal from state manager."""
        return self.state_manager.active_portal

    @active_portal.setter
    def active_portal(self, value):
        """Set active portal on state manager."""
        self.state_manager.active_portal = value

    @property
    def return_portal(self):
        """Get return portal from state manager."""
        return self.state_manager.return_portal

    @return_portal.setter
    def return_portal(self, value):
        """Set return portal on state manager."""
        self.state_manager.return_portal = value

    @property
    def portal_return_location(self):
        """Get portal return location from state manager."""
        return self.state_manager.portal_return_location

    @portal_return_location.setter
    def portal_return_location(self, value):
        """Set portal return location on state manager."""
        self.state_manager.portal_return_location = value

    @property
    def portal_cooldown(self):
        """Get portal cooldown from state manager."""
        return self.state_manager.portal_cooldown

    @portal_cooldown.setter
    def portal_cooldown(self, value):
        """Set portal cooldown on state manager."""
        self.state_manager.portal_cooldown = value

    @property
    def combat_system(self):
        """Get combat system from renderer."""
        return self.renderer.combat_system

    @property
    def inventory_ui(self):
        """Get inventory UI from renderer."""
        return self.renderer.inventory_ui

    @property
    def shop_ui(self):
        """Get shop UI from renderer."""
        return self.renderer.shop_ui

    @property
    def hud(self):
        """Get HUD from renderer."""
        return self.renderer.hud

    def drop_item(self, item: Item, grid_x: int, grid_y: int):
        """
        Drop an item on the ground at specified grid coordinates.

        Args:
            item: The item to drop
            grid_x: Grid x position
            grid_y: Grid y position
        """
        self.entity_manager.drop_item(item, grid_x, grid_y)

    def get_item_at_position(self, grid_x: int, grid_y: int):
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
        # Use event dispatcher for most event handling
        self.event_dispatcher.handle_events(
            warrior=self.warrior,
            game_state_manager=self.state_manager,
            turn_processor=self.turn_processor,
            entity_manager=self.entity_manager,
            inventory_ui=self.renderer.inventory_ui,
            shop=self.shop,
            shop_ui=self.renderer.shop_ui,
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

        # Handle skill UI input separately (skills screen)
        for event in pygame.event.get():
            if self.state_manager.state == config.STATE_SKILLS:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click - learn skill
                        self.skill_ui.handle_click(event.pos, self.warrior, False)
                    elif event.button == 3:  # Right click - set active
                        self.skill_ui.handle_click(event.pos, self.warrior, True)

    def restart(self):
        """Restart the game."""
        # Close any active portals
        self.state_manager.close_portals()

        # Reset to world map
        self.dungeon_manager.current_map_id = "world"
        self.dungeon_manager.return_location = None
        self.world_map = self.dungeon_manager.get_current_map()

        # Update camera for new map
        self.camera = Camera(self.world_map.width, self.world_map.height)

        spawn_x, spawn_y = self.world_map.spawn_point
        self.warrior = Warrior(spawn_x, spawn_y)

        # Add starting items to new warrior
        self._add_starting_items()

        # Reset managers
        self.state_manager.reset()
        self.turn_processor.reset()
        self.entity_manager.reset_tracking()

        # Respawn entities
        self.entity_manager.spawn_monsters(self.world_map, self.dungeon_manager)
        self.entity_manager.spawn_chests(self.world_map, self.dungeon_manager)
        self.entity_manager.clear_ground_items()

    def update(self, dt: float):
        """
        Update game state.

        Args:
            dt: Delta time since last update
        """
        # Update state manager (messages, portals, etc.)
        self.state_manager.update(self.clock, self.warrior, dt)

        # Update HUD (always update for animations)
        self.renderer.hud.update(self.warrior, dt)

        # Only update game logic when actively playing
        if self.state_manager.state != config.STATE_PLAYING:
            return

        # Process turn if player has queued an action
        if not self.turn_processor.waiting_for_player_input:
            self.process_turn()

        # Update camera to follow player
        self.camera.update(self.warrior.grid_x, self.warrior.grid_y)

        # Update fog of war based on player position
        self.fog_of_war.update_visibility(
            self.warrior.grid_x,
            self.warrior.grid_y,
            self.dungeon_manager.current_map_id,
        )

        # Check if player stepped on return portal (auto-teleport back)
        if self.state_manager.check_return_portal_collision(self.warrior):
            self._handle_use_return_portal()
            return

        # Check game over conditions
        if not self.warrior.is_alive:
            self.state_manager.transition_to_game_over()

    def process_turn(self):
        """Process one complete turn (hero then monsters)."""
        self.turn_processor.process_turn(
            warrior=self.warrior,
            entity_manager=self.entity_manager,
            world_map=self.world_map,
            dungeon_manager=self.dungeon_manager,
            on_dungeon_transition=self._check_dungeon_transition,
            on_chest_opened=self._handle_chest_opened,
            on_item_picked=self._show_message,
            on_monster_death=self._handle_monster_death,
        )

    def _check_dungeon_transition(self):
        """Check if player is entering or exiting a dungeon."""
        player_x = self.warrior.grid_x
        player_y = self.warrior.grid_y

        # Check if exiting dungeon
        if self.dungeon_manager.check_for_exit(player_x, player_y):
            return_pos = self.dungeon_manager.exit_dungeon()
            if return_pos:
                # Update map reference
                self.world_map = self.dungeon_manager.get_current_map()

                # Update camera for new map
                self.camera = Camera(self.world_map.width, self.world_map.height)

                # Move player to return location
                self.warrior.grid_x, self.warrior.grid_y = return_pos

                # Respawn monsters and chests for world map
                self.entity_manager.spawn_monsters(self.world_map, self.dungeon_manager)
                self.entity_manager.spawn_chests(self.world_map, self.dungeon_manager)
                self.entity_manager.clear_ground_items()

                self._show_message("You return to the world map.")
                return

        # Check if entering dungeon
        dungeon_id = self.dungeon_manager.get_dungeon_at_position(player_x, player_y)
        if dungeon_id:
            # Enter the dungeon
            spawn_x, spawn_y = self.dungeon_manager.enter_dungeon(
                dungeon_id, player_x, player_y
            )

            # Update map reference
            self.world_map = self.dungeon_manager.get_current_map()

            # Update camera for new map
            self.camera = Camera(self.world_map.width, self.world_map.height)

            # Move player to dungeon spawn
            self.warrior.grid_x = spawn_x
            self.warrior.grid_y = spawn_y

            # Spawn monsters and chests for dungeon
            self.entity_manager.spawn_monsters(self.world_map, self.dungeon_manager)
            self.entity_manager.spawn_chests(self.world_map, self.dungeon_manager)
            self.entity_manager.clear_ground_items()

            # Get dungeon name for message
            for spawn in self.dungeon_manager.world_map.get_entity_spawns("dungeons"):
                if spawn.get("id") == dungeon_id:
                    dungeon_name = spawn.get("name", "dungeon")
                    self._show_message(f"You enter the {dungeon_name}!")
                    break

    def _handle_chest_opened(self, item: Item):
        """
        Handle chest opened event.

        Args:
            item: The item found in the chest
        """
        self._show_message(f"You open the chest. Inside you find a {item.name}!")

    def _handle_monster_death(self, loot_item: Item, monster_type: str, xp_value: int):
        """
        Handle monster death event.

        Args:
            loot_item: The loot item dropped
            monster_type: The type of monster that died
            xp_value: Experience points awarded
        """
        # Award experience points
        leveled_up = self.warrior.gain_experience(xp_value)

        # Show appropriate message
        if leveled_up:
            self._show_message(
                f"Level Up! Now level {self.warrior.experience.current_level}! The {monster_type.replace('_', ' ')} drops a {loot_item.name}! (+{xp_value} XP)"
            )
        else:
            self._show_message(
                f"The {monster_type.replace('_', ' ')} drops a {loot_item.name}! (+{xp_value} XP)"
            )

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


    def draw(self):
        """Draw all game objects."""
        if self.state_manager.state == config.STATE_PLAYING:
            self.renderer.draw_playing_state(
                world_map=self.world_map,
                camera=self.camera,
                entity_manager=self.entity_manager,
                warrior=self.warrior,
                dungeon_manager=self.dungeon_manager,
                shop=self.shop,
                active_portal=self.state_manager.active_portal,
                return_portal=self.state_manager.return_portal,
                message=self.state_manager.message,
                fog_of_war=self.fog_of_war,
            )
        elif self.state_manager.state == config.STATE_INVENTORY:
            self.renderer.draw_inventory_state(
                world_map=self.world_map,
                camera=self.camera,
                entity_manager=self.entity_manager,
                warrior=self.warrior,
                fog_of_war=self.fog_of_war,
            )
        elif self.state_manager.state == config.STATE_SHOP:
            self.renderer.draw_shop_state(shop=self.shop, warrior=self.warrior)
        elif self.state_manager.state == config.STATE_SKILLS:
            # Draw skill UI (full-screen)
            self.skill_ui.draw(self.screen, self.warrior)
            pygame.display.flip()
        elif self.state_manager.state == config.STATE_GAME_OVER:
            self.renderer.draw_game_over_state("GAME OVER!", config.RED)

    def draw_game_over_screen(self, message: str, color: tuple):
        """
        Draw game over or victory screen.

        Args:
            message: Message to display
            color: Color of the message
        """
        self.renderer.draw_game_over_state(message, color)

    def _add_starting_items(self):
        """Add starting equipment to warrior inventory."""
        # Import loot table function for town portal
        from loot_table import create_town_portal

        # Create starting equipment
        short_sword = Item(
            name="Short Sword",
            item_type=ItemType.WEAPON,
            description="A basic short sword",
            attack_bonus=3,
        )
        woolen_tunic = Item(
            name="Woolen Tunic",
            item_type=ItemType.ARMOR,
            description="A simple woolen tunic",
            defense_bonus=1,
        )
        health_potion = Item(
            name="Health Potion",
            item_type=ItemType.CONSUMABLE,
            description="Restores 30 HP",
            health_bonus=30,
        )

        # Equip starting items (they'll auto-equip to appropriate slots)
        self.warrior.inventory.add_item(short_sword)
        self.warrior.inventory.add_item(woolen_tunic)
        self.warrior.inventory.add_item(health_potion)

        # Add a starting town portal for testing
        self.warrior.inventory.add_item(create_town_portal())

        # Player starts with some gold to buy items
        self.warrior.add_gold(100)

    def save_game(self, filename: str = "quicksave") -> bool:
        """
        Save the current game state.

        Args:
            filename: Name of the save file

        Returns:
            True if save was successful
        """
        from save_game import SaveGame

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
        from save_game import SaveGame

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
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0  # Delta time in seconds

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
