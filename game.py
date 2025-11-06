"""Main game class and game loop."""

import pygame
import random
import os
from warrior import Warrior
from monsters import ALL_MONSTER_CLASSES
from combat import CombatSystem
from inventory_ui import InventoryUI
from ui_button import Button
from item import Item, ItemType
from world_map import WorldMap
from camera import Camera
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

        # Load world map
        self.world_map = WorldMap()
        if map_file is None:
            map_file = os.path.join("maps", "sample_map.json")
        self.world_map.load_from_file(map_file)

        # Initialize camera
        self.camera = Camera(self.world_map.width, self.world_map.height)

        # Initialize game objects at spawn point
        spawn_x, spawn_y = self.world_map.spawn_point
        self.warrior = Warrior(spawn_x, spawn_y)

        # Spawn monsters from map data
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
            monster_class = random.choice(ALL_MONSTER_CLASSES)
            monster = monster_class(spawn_x + 5, spawn_y)
            self.monsters.append(monster)

        self.combat_system = CombatSystem()
        self.inventory_ui = InventoryUI()

        # Create UI button for inventory
        button_width = 100
        button_height = 40
        button_x = config.SCREEN_WIDTH - button_width - 10
        button_y = 10
        self.inventory_button = Button(
            button_x, button_y, button_width, button_height, "Inventory (I)"
        )

        # Turn-based state
        self.waiting_for_player_input = True
        self.last_key_time = 0
        self.key_delay = 200  # milliseconds between key presses

        # Add sample items to warrior's inventory
        self._add_sample_items()

    def _add_sample_items(self):
        """Add sample items to the warrior's inventory for testing."""
        # Create sample items
        iron_sword = Item(
            "Iron Sword", ItemType.WEAPON, "A basic sword", attack_bonus=10
        )
        steel_sword = Item(
            "Steel Sword", ItemType.WEAPON, "A stronger sword", attack_bonus=20
        )
        leather_armor = Item(
            "Leather Armor",
            ItemType.ARMOR,
            "Basic protection",
            defense_bonus=5,
            health_bonus=20,
        )
        health_potion = Item(
            "Health Potion", ItemType.CONSUMABLE, "Restores health", health_bonus=30
        )
        gold_coin = Item("Gold Coin", ItemType.MISC, "Shiny currency")

        # Add items to inventory
        self.warrior.inventory.add_item(iron_sword)  # Goes to weapon slot
        self.warrior.inventory.add_item(leather_armor)  # Goes to armor slot
        self.warrior.inventory.add_item(steel_sword)  # Goes to backpack
        self.warrior.inventory.add_item(health_potion)  # Goes to backpack
        self.warrior.inventory.add_item(gold_coin)  # Goes to backpack

    def handle_events(self):
        """Handle pygame events."""
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle inventory button click (only when playing)
                if event.button == 1 and self.state == config.STATE_PLAYING:
                    if self.inventory_button.is_clicked(event.pos):
                        self.state = config.STATE_INVENTORY
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.state != config.STATE_PLAYING:
                    # Restart game
                    self.restart()
                elif event.key == pygame.K_i and self.state in [
                    config.STATE_PLAYING,
                    config.STATE_INVENTORY,
                ]:
                    # Toggle inventory
                    if self.state == config.STATE_PLAYING:
                        self.state = config.STATE_INVENTORY
                    else:
                        self.state = config.STATE_PLAYING
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
                self.inventory_ui.handle_input(event, self.warrior.inventory)

    def restart(self):
        """Restart the game."""
        spawn_x, spawn_y = self.world_map.spawn_point
        self.warrior = Warrior(spawn_x, spawn_y)

        # Respawn monsters from map data
        self.monsters = []
        monster_spawns = self.world_map.get_entity_spawns("monsters")
        for spawn in monster_spawns:
            monster_type = spawn.get("type", "banshee")
            monster_class = None
            for cls in ALL_MONSTER_CLASSES:
                if cls.MONSTER_TYPE == monster_type:
                    monster_class = cls
                    break
            if monster_class is None:
                monster_class = random.choice(ALL_MONSTER_CLASSES)
            monster = monster_class(spawn["x"], spawn["y"])
            self.monsters.append(monster)

        if not self.monsters:
            monster_class = random.choice(ALL_MONSTER_CLASSES)
            monster = monster_class(spawn_x + 5, spawn_y)
            self.monsters.append(monster)

        self.state = config.STATE_PLAYING
        self.waiting_for_player_input = True
        self._add_sample_items()

    def update(self, dt: float):
        """
        Update game state.

        Args:
            dt: Delta time since last update
        """
        # Only update game logic when actively playing
        if self.state != config.STATE_PLAYING:
            return

        # Process turn if player has queued an action
        if not self.waiting_for_player_input:
            self.process_turn()

        # Update camera to follow player
        self.camera.update(self.warrior.grid_x, self.warrior.grid_y)

        # Check game over conditions
        if not self.warrior.is_alive:
            self.state = config.STATE_GAME_OVER
        elif all(not monster.is_alive for monster in self.monsters):
            self.state = config.STATE_VICTORY

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

        # Monster turns
        for monster in self.monsters:
            if monster.is_alive:
                monster.on_turn_start()
                monster.execute_turn(self.warrior, self.world_map)

        # Wait for next player input
        self.waiting_for_player_input = True

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

            # Draw entities with camera offset
            self._draw_entities_with_camera()

            # Draw combat UI (find nearest monster)
            nearest_monster = self._get_nearest_alive_monster()
            if nearest_monster:
                self.combat_system.draw_combat_ui(
                    self.screen, self.warrior, nearest_monster
                )

            # Draw inventory button
            self.inventory_button.draw(self.screen)

        elif self.state == config.STATE_INVENTORY:
            # Draw the game in the background
            self.world_map.draw(
                self.screen,
                self.camera.x,
                self.camera.y,
                self.camera.viewport_width,
                self.camera.viewport_height,
            )
            self._draw_entities_with_camera()
            nearest_monster = self._get_nearest_alive_monster()
            if nearest_monster:
                self.combat_system.draw_combat_ui(
                    self.screen, self.warrior, nearest_monster
                )

            # Draw inventory overlay on top
            self.inventory_ui.draw(self.screen, self.warrior.inventory)

        elif self.state == config.STATE_VICTORY:
            self.draw_game_over_screen("VICTORY!", config.GREEN)

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

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0  # Delta time in seconds

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
