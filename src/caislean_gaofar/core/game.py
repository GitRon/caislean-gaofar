"""Main game class and game loop."""

import pygame
import os
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.objects.shop import Shop
from caislean_gaofar.ui.skill_ui import SkillUI
from caislean_gaofar.objects.item import Item, ItemType
from caislean_gaofar.world.camera import Camera
from caislean_gaofar.objects.ground_item import GroundItem
from caislean_gaofar.world.dungeon_manager import DungeonManager
from caislean_gaofar.objects.temple import Temple
from caislean_gaofar.world.fog_of_war import FogOfWar
from caislean_gaofar.core import config

# Import new component classes
from caislean_gaofar.entities.entity_manager import EntityManager
from caislean_gaofar.systems.turn_processor import TurnProcessor
from caislean_gaofar.world.world_renderer import WorldRenderer
from caislean_gaofar.core.game_state_manager import GameStateManager
from caislean_gaofar.utils.event_dispatcher import EventDispatcher
from caislean_gaofar.core.game_loop import GameLoop
from caislean_gaofar.world.dungeon_transition_manager import DungeonTransitionManager


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
        self.game_loop = GameLoop(self.clock)
        self.dungeon_transition_manager = DungeonTransitionManager()

        # Initialize dungeon manager
        if map_file is None:
            map_file = config.resource_path(
                os.path.join("data", "maps", "overworld.json")
            )
        else:
            # Apply resource_path to custom map if it's a relative path
            if not os.path.isabs(map_file):
                map_file = config.resource_path(map_file)
        self.dungeon_manager = DungeonManager(map_file)
        self.dungeon_manager.load_world_map()

        # Load dungeons - map unique IDs to actual dungeon files
        dark_cave_path = config.resource_path(
            os.path.join("data", "maps", "dark_cave.json")
        )
        ancient_castle_path = config.resource_path(
            os.path.join("data", "maps", "ancient_castle.json")
        )

        # Cave-type dungeons
        self.dungeon_manager.load_dungeon("dark_cave_1", dark_cave_path)
        self.dungeon_manager.load_dungeon("mystic_grotto", dark_cave_path)
        self.dungeon_manager.load_dungeon("dark_woods_lair", dark_cave_path)
        self.dungeon_manager.load_dungeon("southern_caverns", dark_cave_path)

        # Castle-type dungeons
        self.dungeon_manager.load_dungeon("haunted_crypt", ancient_castle_path)
        self.dungeon_manager.load_dungeon("shadow_keep", ancient_castle_path)
        self.dungeon_manager.load_dungeon("ruined_fortress", ancient_castle_path)
        self.dungeon_manager.load_dungeon("ancient_keep", ancient_castle_path)

        # Town
        self.dungeon_manager.load_dungeon(
            "town", config.resource_path(os.path.join("data", "maps", "town.json"))
        )

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

        # Initialize temple (located at specific position on town map)
        # Position matches 'T' in town.json
        self.temple = Temple(grid_x=8, grid_y=1)  # Position in town

        # Spawn monsters and chests
        self.entity_manager.spawn_monsters(self.world_map, self.dungeon_manager)
        self.entity_manager.spawn_chests(self.world_map, self.dungeon_manager)

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
        # Use event dispatcher for all event handling
        self.event_dispatcher.handle_events(
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

        # Update temple animation
        if self.temple:
            self.temple.update(dt)

        # Update attack effects
        self.renderer.attack_effect_manager.update(dt)

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

        # Check if player stepped on temple (heal to max HP)
        if (
            self.dungeon_manager.current_map_id == "town"
            and self.warrior.grid_x == self.temple.grid_x
            and self.warrior.grid_y == self.temple.grid_y
        ):
            self._heal_at_temple()

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
            attack_effect_manager=self.renderer.attack_effect_manager,
        )

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

    def _heal_at_temple(self):
        """Heal the warrior to maximum HP when stepping on the temple."""
        if self.warrior.health < self.warrior.max_health:
            # Heal to max HP
            self.warrior.health = self.warrior.max_health
            # Activate healing visual effect
            self.temple.activate_healing()
            self._show_message("The temple's divine power restores your health!")

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
                temple=self.temple,
            )
        elif self.state_manager.state == config.STATE_INVENTORY:
            self.renderer.draw_inventory_state(
                world_map=self.world_map,
                camera=self.camera,
                entity_manager=self.entity_manager,
                warrior=self.warrior,
                fog_of_war=self.fog_of_war,
                dungeon_manager=self.dungeon_manager,
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
        from caislean_gaofar.systems.loot_table import create_town_portal

        # Create starting equipment
        short_sword = Item(
            name="Short Sword",
            item_type=ItemType.WEAPON,
            description="A basic short sword",
            attack_bonus=3,
            gold_value=30,
        )
        woolen_tunic = Item(
            name="Woolen Tunic",
            item_type=ItemType.ARMOR,
            description="A simple woolen tunic",
            defense_bonus=1,
            gold_value=10,
        )
        health_potion = Item(
            name="Health Potion",
            item_type=ItemType.CONSUMABLE,
            description="Restores 30 HP",
            gold_value=30,
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
