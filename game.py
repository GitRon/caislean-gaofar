"""Main game class and game loop."""

import pygame
import random
import os
from warrior import Warrior
from monsters import ALL_MONSTER_CLASSES
from combat import CombatSystem
from inventory_ui import InventoryUI
from shop import Shop
from shop_ui import ShopUI
from item import Item, ItemType
from camera import Camera
from chest import Chest
from ground_item import GroundItem
from loot_table import get_loot_for_monster
from hud import HUD
from dungeon_manager import DungeonManager
from portal import Portal
import config


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
        self.running = True
        self.state = config.STATE_PLAYING

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

        # Spawn monsters from map data
        self._spawn_monsters()

        self.combat_system = CombatSystem()
        self.inventory_ui = InventoryUI()
        self.hud = HUD()

        # Initialize shop (located at specific position on town map)
        # Position matches 'S' in town.json
        self.shop = Shop(grid_x=4, grid_y=3)  # Position in town
        self.shop_ui = ShopUI()

        # Turn-based state
        self.waiting_for_player_input = True
        self.last_key_time = 0
        self.key_delay = 200  # milliseconds between key presses

        # World objects
        self.chests = []
        self.ground_items = []

        # Portal system
        self.active_portal = None  # Portal in dungeon/world
        self.return_portal = None  # Portal in shop
        self.portal_return_location = None  # (map_id, grid_x, grid_y)
        self.shop_warrior_position = (6, 5)  # Fixed position in shop
        self.portal_cooldown = 0  # Prevent instant re-teleportation

        # Messages
        self.message = ""
        self.message_timer = 0
        self.message_duration = 3000  # milliseconds to show message

        # Spawn chests in the dungeon
        self._spawn_chests()

    def _spawn_monsters(self):
        """Spawn monsters from current map data."""
        self.monsters = []
        monster_spawns = self.world_map.get_entity_spawns("monsters")
        for spawn in monster_spawns:
            monster_type = spawn.get("type", "banshee")
            # Find matching monster class
            monster_class = None
            for cls in ALL_MONSTER_CLASSES:
                if cls.MONSTER_TYPE == monster_type:
                    monster_class = cls
                    break
            if monster_class is None:
                monster_class = random.choice(ALL_MONSTER_CLASSES)
            monster = monster_class(spawn["x"], spawn["y"])
            self.monsters.append(monster)

        # If no monsters in map, spawn one randomly
        if not self.monsters:
            spawn_x, spawn_y = self.world_map.spawn_point
            monster_class = random.choice(ALL_MONSTER_CLASSES)
            monster = monster_class(spawn_x + 5, spawn_y)
            self.monsters.append(monster)

    def drop_item(self, item: Item, grid_x: int, grid_y: int):
        """
        Drop an item on the ground at specified grid coordinates.

        Args:
            item: The item to drop
            grid_x: Grid x position
            grid_y: Grid y position
        """
        ground_item = GroundItem(item, grid_x, grid_y)
        self.ground_items.append(ground_item)

    def get_item_at_position(self, grid_x: int, grid_y: int):
        """
        Get the item at a specific position.

        Args:
            grid_x: Grid x position
            grid_y: Grid y position

        Returns:
            GroundItem if found, None otherwise
        """
        for ground_item in self.ground_items:
            if ground_item.grid_x == grid_x and ground_item.grid_y == grid_y:
                return ground_item
        return None

    def pickup_item_at_position(self, grid_x: int, grid_y: int) -> bool:
        """
        Try to pick up an item at the specified grid position.

        Args:
            grid_x: Grid x position
            grid_y: Grid y position

        Returns:
            True if an item was picked up, False otherwise
        """
        # Find item at this position
        for ground_item in self.ground_items:
            if ground_item.grid_x == grid_x and ground_item.grid_y == grid_y:
                # Check if it's a gold item (has gold_value > 0)
                if ground_item.item.gold_value > 0:
                    # Add gold to currency instead of inventory
                    self.warrior.add_gold(ground_item.item.gold_value)
                    self.ground_items.remove(ground_item)
                    self._show_message(f"Picked up {ground_item.item.gold_value} gold!")
                    return True
                # Try to add regular item to inventory
                elif self.warrior.inventory.add_item(ground_item.item):
                    self.ground_items.remove(ground_item)
                    self._show_message(f"Picked up {ground_item.item.name}!")
                    return True
                else:
                    # Inventory full
                    self._show_message("Inventory is full!")
                    return False
        return False

    def _spawn_chests(self):
        """Spawn chests from map data or at random locations."""
        # Clear existing chests
        self.chests = []

        # Don't spawn chests in town
        if self.dungeon_manager.current_map_id == "town":
            return

        # Try to spawn chests from map data
        chest_spawns = self.world_map.get_entity_spawns("chests")
        if chest_spawns:
            for spawn in chest_spawns:
                chest = Chest(spawn["x"], spawn["y"])
                self.chests.append(chest)
        else:
            # Fallback: Define positions where chests can spawn
            chest_positions = [
                (5, 3),  # Top middle area
                (10, 2),  # Top right area
                (7, 5),  # Center
                (3, 8),  # Bottom left
                (12, 9),  # Bottom right
                (8, 10),  # Bottom center
            ]

            # Randomly select 3-5 positions for chests
            num_chests = random.randint(3, 5)
            selected_positions = random.sample(chest_positions, num_chests)

            for grid_x, grid_y in selected_positions:
                chest = Chest(grid_x, grid_y)
                self.chests.append(chest)

    def handle_events(self):
        """Handle pygame events."""
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.state == config.STATE_GAME_OVER:
                    # Restart game
                    self.restart()
                elif event.key == pygame.K_i and self.state in [
                    config.STATE_PLAYING,
                    config.STATE_INVENTORY,
                    config.STATE_SHOP,
                ]:
                    # Toggle inventory
                    if self.state == config.STATE_PLAYING:
                        self.state = config.STATE_INVENTORY
                    elif self.state == config.STATE_SHOP:
                        self.state = config.STATE_INVENTORY
                    else:
                        # Return to previous state (playing or shop)
                        # Check if we came from shop by checking portal location
                        if self.return_portal:
                            self.state = config.STATE_SHOP
                        else:
                            self.state = config.STATE_PLAYING
                # Handle shop toggle (when on town map near shop)
                elif event.key == pygame.K_s and self.state in [
                    config.STATE_PLAYING,
                    config.STATE_SHOP,
                ]:
                    # Toggle shop (only if on town map near shop location)
                    if self.state == config.STATE_PLAYING:
                        # Check if player is on town map and near shop
                        if (
                            self.dungeon_manager.current_map_id == "town"
                            and self._is_near_shop()
                        ):
                            self.state = config.STATE_SHOP
                        else:
                            self._show_message("No shop nearby!")
                    else:
                        # Exit shop without penalty
                        self.state = config.STATE_PLAYING
                # Handle pickup (instant, doesn't consume a turn)
                elif event.key == pygame.K_g and self.state == config.STATE_PLAYING:
                    self.pickup_item_at_position(
                        self.warrior.grid_x, self.warrior.grid_y
                    )
                # Handle health potion usage (instant, doesn't consume a turn)
                elif event.key == pygame.K_p and self.state == config.STATE_PLAYING:
                    if self.warrior.use_health_potion():
                        self.hud.trigger_potion_glow()
                        self._show_message("Used health potion! +30 HP")
                    else:
                        if self.warrior.count_health_potions() <= 0:
                            self._show_message("No health potions remaining!")
                        else:
                            self._show_message("Health is already full!")
                # Handle town portal usage (instant, doesn't consume a turn)
                elif event.key == pygame.K_t and self.state == config.STATE_PLAYING:
                    self._use_town_portal()
                # Handle shop exit
                elif event.key == pygame.K_ESCAPE and self.state == config.STATE_SHOP:
                    if self.return_portal:
                        self._use_return_portal()
                # Handle return portal usage in shop
                elif event.key == pygame.K_t and self.state == config.STATE_SHOP:
                    if self.return_portal:
                        self._use_return_portal()
                # Handle turn-based movement input
                elif (
                    self.state == config.STATE_PLAYING and self.waiting_for_player_input
                ):
                    if current_time - self.last_key_time >= self.key_delay:
                        action_queued = False
                        if event.key in [pygame.K_w, pygame.K_UP]:
                            self.warrior.queue_movement(0, -1)
                            action_queued = True
                        elif event.key in [pygame.K_s, pygame.K_DOWN]:
                            self.warrior.queue_movement(0, 1)
                            action_queued = True
                        elif event.key in [pygame.K_a, pygame.K_LEFT]:
                            self.warrior.queue_movement(-1, 0)
                            action_queued = True
                        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                            self.warrior.queue_movement(1, 0)
                            action_queued = True
                        elif event.key == pygame.K_SPACE:
                            self.warrior.queue_attack()
                            action_queued = True

                        if action_queued:
                            self.waiting_for_player_input = False
                            self.last_key_time = current_time

            # Handle inventory input when inventory is open
            if self.state == config.STATE_INVENTORY:
                self.inventory_ui.handle_input(event, self.warrior.inventory, self)

            # Handle shop input when shop is open
            if self.state == config.STATE_SHOP:
                self.shop_ui.handle_input(event, self.shop, self.warrior)

    def restart(self):
        """Restart the game."""
        # Close any active portals
        self._close_portals()

        # Reset to world map
        self.dungeon_manager.current_map_id = "world"
        self.dungeon_manager.return_location = None
        self.world_map = self.dungeon_manager.get_current_map()

        # Update camera for new map
        self.camera = Camera(self.world_map.width, self.world_map.height)

        spawn_x, spawn_y = self.world_map.spawn_point
        self.warrior = Warrior(spawn_x, spawn_y)

        # Respawn monsters from map data
        self._spawn_monsters()

        # Add starting items to new warrior
        self._add_starting_items()

        self.state = config.STATE_PLAYING
        self.waiting_for_player_input = True
        self.ground_items = []  # Clear ground items
        self.message = ""
        self.message_timer = 0
        self._spawn_chests()

    def update(self, dt: float):
        """
        Update game state.

        Args:
            dt: Delta time since last update
        """
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= self.clock.get_time()
            if self.message_timer <= 0:
                self.message = ""

        # Update portal cooldown timer
        if self.portal_cooldown > 0:
            self.portal_cooldown -= self.clock.get_time()

        # Update HUD (always update for animations)
        self.hud.update(self.warrior, dt)

        # Update portal animations
        if self.active_portal:
            self.active_portal.update(dt)
        if self.return_portal:
            self.return_portal.update(dt)

        # Only update game logic when actively playing
        if self.state != config.STATE_PLAYING:
            return

        # Process turn if player has queued an action
        if not self.waiting_for_player_input:
            self.process_turn()

        # Update camera to follow player
        self.camera.update(self.warrior.grid_x, self.warrior.grid_y)

        # Check if player stepped on return portal (auto-teleport back)
        if self.return_portal and self.portal_cooldown <= 0:
            if (
                self.warrior.grid_x == self.return_portal.grid_x
                and self.warrior.grid_y == self.return_portal.grid_y
            ):
                self._use_return_portal()
                return

        # Check game over conditions
        if not self.warrior.is_alive:
            self.state = config.STATE_GAME_OVER
            # Close portals on death
            self._close_portals()

    def process_turn(self):
        """Process one complete turn (hero then monsters)."""
        # Hero turn
        self.warrior.on_turn_start()
        # Find nearest monster for targeting
        nearest_monster = None
        min_distance = float("inf")
        for monster in self.monsters:
            if monster.is_alive:
                distance = self.warrior.grid_distance_to(monster)
                if distance < min_distance:
                    min_distance = distance
                    nearest_monster = monster

        self.warrior.execute_turn(nearest_monster, self.world_map)

        # Check for dungeon entrance/exit after warrior moves
        self._check_dungeon_transition()

        # Check for chest collision after warrior moves
        self._check_chest_collision()

        # Check for ground item pickup after warrior moves
        self._check_ground_item_pickup()

        # Check for monster deaths and drop loot (after warrior attacks)
        self._check_monster_deaths()

        # Monster turns
        for monster in self.monsters:
            if monster.is_alive:
                monster.on_turn_start()
                monster.execute_turn(self.warrior, self.world_map)

        # Wait for next player input
        self.waiting_for_player_input = True

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
                self._spawn_monsters()
                self._spawn_chests()
                self.ground_items = []

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
            self._spawn_monsters()
            self._spawn_chests()
            self.ground_items = []

            # Get dungeon name for message
            for spawn in self.dungeon_manager.world_map.get_entity_spawns("dungeons"):
                if spawn.get("id") == dungeon_id:
                    dungeon_name = spawn.get("name", "dungeon")
                    self._show_message(f"You enter the {dungeon_name}!")
                    break

    def _check_chest_collision(self):
        """Check if warrior stepped on a chest and open it."""
        for chest in self.chests[:]:  # Iterate over copy to allow removal
            if (
                not chest.is_opened
                and chest.grid_x == self.warrior.grid_x
                and chest.grid_y == self.warrior.grid_y
            ):
                # Open the chest
                item = chest.open()

                # Create ground item at chest location
                ground_item = GroundItem(item, chest.grid_x, chest.grid_y)
                self.ground_items.append(ground_item)

                # Remove chest from list
                self.chests.remove(chest)

                # Show message
                self._show_message(
                    f"You open the chest. Inside you find a {item.name}!"
                )

    def _check_ground_item_pickup(self):
        """Check if warrior is standing on a ground item and pick it up."""
        for ground_item in self.ground_items[:]:  # Iterate over copy to allow removal
            if (
                ground_item.grid_x == self.warrior.grid_x
                and ground_item.grid_y == self.warrior.grid_y
            ):
                # Check if it's a gold item (has gold_value > 0)
                if ground_item.item.gold_value > 0:
                    # Add gold to currency instead of inventory
                    self.warrior.add_gold(ground_item.item.gold_value)
                    self.ground_items.remove(ground_item)
                    self._show_message(f"Picked up {ground_item.item.gold_value} gold!")
                # Try to add regular item to inventory
                elif self.warrior.inventory.add_item(ground_item.item):
                    # Successfully added
                    self.ground_items.remove(ground_item)
                    self._show_message(f"Picked up {ground_item.item.name}!")
                else:
                    # Inventory full
                    self._show_message("Inventory is full!")

    def _check_monster_deaths(self):
        """Check for dead monsters and drop their loot."""
        for monster in self.monsters[:]:  # Iterate over copy to allow removal
            if not monster.is_alive:
                # Use loot_table system to generate loot
                loot_item = get_loot_for_monster(monster.monster_type)

                if loot_item:
                    # Create ground item at monster location
                    self.drop_item(loot_item, monster.grid_x, monster.grid_y)

                    # Show message
                    self._show_message(
                        f"The {monster.monster_type.replace('_', ' ')} drops a {loot_item.name}!"
                    )

                # Remove dead monster from list so loot only drops once
                self.monsters.remove(monster)

    def _show_message(self, message: str):
        """Show a message to the player."""
        self.message = message
        self.message_timer = self.message_duration

    def _use_town_portal(self):
        """Use a town portal to teleport to town."""
        portal_count = self.warrior.count_town_portals()

        if self.warrior.use_town_portal():
            # Close any existing portals
            self._close_portals()

            # Save current location
            current_map_id = self.dungeon_manager.current_map_id
            self.portal_return_location = (
                current_map_id,
                self.warrior.grid_x,
                self.warrior.grid_y,
            )

            # Create portal at current location
            self.active_portal = Portal(self.warrior.grid_x, self.warrior.grid_y, False)

            # Switch to town map
            self.dungeon_manager.current_map_id = "town"
            self.world_map = self.dungeon_manager.get_current_map()
            self.camera = Camera(self.world_map.width, self.world_map.height)

            # Clear chests when entering town
            self.chests = []

            # Teleport to town spawn point
            spawn_x, spawn_y = self.world_map.spawn_point
            # Place player one tile to the right of portal to avoid standing on it
            self.warrior.grid_x, self.warrior.grid_y = spawn_x + 1, spawn_y

            # Create return portal at spawn location
            self.return_portal = Portal(spawn_x, spawn_y, True)

            # Stay in playing state (on town map)
            self.state = config.STATE_PLAYING

            # Set cooldown to prevent instant re-teleportation (500ms)
            self.portal_cooldown = 500

            self._show_message("You enter the portal and arrive in town!")
        else:
            if portal_count <= 0:
                self._show_message("No town portals in inventory!")
            else:
                self._show_message(
                    f"You have {portal_count} portal(s) but cannot use them here!"
                )

    def _use_return_portal(self):
        """Use the return portal to go back to saved location."""
        if not self.return_portal or not self.portal_return_location:
            self._show_message("No return portal available!")
            return

        map_id, grid_x, grid_y = self.portal_return_location

        # Switch to the saved map
        if map_id != self.dungeon_manager.current_map_id:
            self.dungeon_manager.current_map_id = map_id
            self.world_map = self.dungeon_manager.get_current_map()
            self.camera = Camera(self.world_map.width, self.world_map.height)

            # Respawn chests when returning from town
            if map_id != "town":
                self._spawn_chests()

        # Return to saved position
        self.warrior.grid_x = grid_x
        self.warrior.grid_y = grid_y

        # Return to playing state
        self.state = config.STATE_PLAYING

        # Set cooldown to prevent instant re-teleportation (500ms)
        self.portal_cooldown = 500

        # Close both portals
        self._close_portals()

        self._show_message("You return through the portal!")

    def _close_portals(self):
        """Close all active portals."""
        self.active_portal = None
        self.return_portal = None
        self.portal_return_location = None

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

    def _draw_shop_building(self):
        """Draw the shop building on the town map."""
        if not self.camera.is_visible(self.shop.grid_x, self.shop.grid_y):
            return

        # Convert shop grid position to screen position
        screen_x, screen_y = self.camera.world_to_screen(
            self.shop.grid_x, self.shop.grid_y
        )

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
        if self._is_near_shop():
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

    def draw(self):
        """Draw all game objects."""
        self.screen.fill(config.BLACK)

        if self.state == config.STATE_PLAYING:
            # Draw world map
            self.world_map.draw(
                self.screen,
                self.camera.x,
                self.camera.y,
                self.camera.viewport_width,
                self.camera.viewport_height,
            )

            # Draw world objects (chests and ground items) with camera offset
            self._draw_world_objects_with_camera()

            # Draw active portal if present (only when NOT in town)
            if self.active_portal and self.dungeon_manager.current_map_id != "town":
                if self.camera.is_visible(
                    self.active_portal.grid_x, self.active_portal.grid_y
                ):
                    original_x = self.active_portal.grid_x
                    original_y = self.active_portal.grid_y
                    screen_x, screen_y = self.camera.world_to_screen(
                        original_x, original_y
                    )
                    self.active_portal.grid_x = screen_x
                    self.active_portal.grid_y = screen_y
                    self.active_portal.draw(self.screen)
                    self.active_portal.grid_x = original_x
                    self.active_portal.grid_y = original_y

            # Draw return portal if present (only when IN town)
            if self.return_portal and self.dungeon_manager.current_map_id == "town":
                if self.camera.is_visible(
                    self.return_portal.grid_x, self.return_portal.grid_y
                ):
                    original_x = self.return_portal.grid_x
                    original_y = self.return_portal.grid_y
                    screen_x, screen_y = self.camera.world_to_screen(
                        original_x, original_y
                    )
                    self.return_portal.grid_x = screen_x
                    self.return_portal.grid_y = screen_y
                    self.return_portal.draw(self.screen)
                    self.return_portal.grid_x = original_x
                    self.return_portal.grid_y = original_y

            # Draw shop building if in town
            if self.dungeon_manager.current_map_id == "town":
                self._draw_shop_building()

            # Draw entities with camera offset
            self._draw_entities_with_camera()

            # Draw combat UI (find nearest monster)
            nearest_monster = self._get_nearest_alive_monster()
            if nearest_monster:
                self.combat_system.draw_combat_ui(
                    self.screen, self.warrior, nearest_monster
                )

            # Draw HUD (player stats, potions, gold)
            self.hud.draw(self.screen, self.warrior)

            # Draw message if active
            if self.message:
                self._draw_message()

        elif self.state == config.STATE_INVENTORY:
            # Draw the game in the background
            self.world_map.draw(
                self.screen,
                self.camera.x,
                self.camera.y,
                self.camera.viewport_width,
                self.camera.viewport_height,
            )
            self._draw_world_objects_with_camera()
            self._draw_entities_with_camera()
            nearest_monster = self._get_nearest_alive_monster()
            if nearest_monster:
                self.combat_system.draw_combat_ui(
                    self.screen, self.warrior, nearest_monster
                )

            # Draw HUD (player stats, potions, gold)
            self.hud.draw(self.screen, self.warrior)

            # Draw inventory overlay on top if open
            if self.state == config.STATE_INVENTORY:
                self.inventory_ui.draw(self.screen, self.warrior.inventory)

        elif self.state == config.STATE_SHOP:
            # Draw shop UI
            self.shop_ui.draw(self.screen, self.shop, self.warrior)

        elif self.state == config.STATE_GAME_OVER:
            self.draw_game_over_screen("GAME OVER!", config.RED)

        pygame.display.flip()

    def _get_nearest_alive_monster(self):
        """Get the nearest alive monster to the warrior."""
        nearest_monster = None
        min_distance = float("inf")
        for monster in self.monsters:
            if monster.is_alive:
                distance = self.warrior.grid_distance_to(monster)
                if distance < min_distance:
                    min_distance = distance
                    nearest_monster = monster
        return nearest_monster

    def _draw_world_objects_with_camera(self):
        """Draw chests and ground items with camera offset applied."""
        # Draw chests
        for chest in self.chests:
            if self.camera.is_visible(chest.grid_x, chest.grid_y):
                original_x = chest.grid_x
                original_y = chest.grid_y
                screen_x, screen_y = self.camera.world_to_screen(original_x, original_y)
                chest.grid_x = screen_x
                chest.grid_y = screen_y
                chest.draw(self.screen)
                chest.grid_x = original_x
                chest.grid_y = original_y

        # Draw ground items
        for ground_item in self.ground_items:
            if self.camera.is_visible(ground_item.grid_x, ground_item.grid_y):
                original_x = ground_item.grid_x
                original_y = ground_item.grid_y
                screen_x, screen_y = self.camera.world_to_screen(original_x, original_y)
                ground_item.grid_x = screen_x
                ground_item.grid_y = screen_y
                ground_item.draw(self.screen)
                ground_item.grid_x = original_x
                ground_item.grid_y = original_y

    def _draw_entities_with_camera(self):
        """Draw all entities with camera offset applied."""
        # Temporarily adjust entity positions for drawing
        # Draw warrior
        if self.camera.is_visible(self.warrior.grid_x, self.warrior.grid_y):
            original_x = self.warrior.grid_x
            original_y = self.warrior.grid_y
            screen_x, screen_y = self.camera.world_to_screen(original_x, original_y)
            self.warrior.grid_x = screen_x
            self.warrior.grid_y = screen_y
            self.warrior.draw(self.screen)
            self.warrior.grid_x = original_x
            self.warrior.grid_y = original_y

        # Draw monsters
        for monster in self.monsters:
            if monster.is_alive and self.camera.is_visible(
                monster.grid_x, monster.grid_y
            ):
                original_x = monster.grid_x
                original_y = monster.grid_y
                screen_x, screen_y = self.camera.world_to_screen(original_x, original_y)
                monster.grid_x = screen_x
                monster.grid_y = screen_y
                monster.draw(self.screen)
                monster.grid_x = original_x
                monster.grid_y = original_y

    def draw_game_over_screen(self, message: str, color: tuple):
        """
        Draw game over or victory screen.

        Args:
            message: Message to display
            color: Color of the message
        """
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

    def _draw_message(self):
        """Draw the current message at the bottom of the screen."""
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.message, True, config.WHITE)

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

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0  # Delta time in seconds

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
