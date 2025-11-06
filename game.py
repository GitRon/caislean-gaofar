"""Main game class and game loop."""

import pygame
import random
from warrior import Warrior
from monsters import ALL_MONSTER_CLASSES
from combat import CombatSystem
from inventory_ui import InventoryUI
from ui_button import Button
from item import Item, ItemType
from chest import Chest
from ground_item import GroundItem
import config


class Game:
    """Main game class that manages the game loop and state."""

    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = config.STATE_PLAYING

        # Initialize game objects with grid coordinates
        self.warrior = Warrior(2, config.GRID_HEIGHT // 2)
        # Randomly select a monster class for variety
        monster_class = random.choice(ALL_MONSTER_CLASSES)
        self.monster = monster_class(config.GRID_WIDTH - 3, config.GRID_HEIGHT // 2)
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

        # World objects
        self.chests = []
        self.ground_items = []

        # Messages
        self.message = ""
        self.message_timer = 0
        self.message_duration = 3000  # milliseconds to show message

        # Add sample items to warrior's inventory
        self._add_sample_items()

        # Spawn chests in the dungeon
        self._spawn_chests()

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

    def _spawn_chests(self):
        """Spawn chests at random locations in the dungeon."""
        # Clear existing chests
        self.chests = []

        # Define positions where chests can spawn (avoid spawning on player or monster)
        # For now, manually place some chests at good locations
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
        self.warrior = Warrior(2, config.GRID_HEIGHT // 2)
        # Randomly select a new monster class on restart
        monster_class = random.choice(ALL_MONSTER_CLASSES)
        self.monster = monster_class(config.GRID_WIDTH - 3, config.GRID_HEIGHT // 2)
        self.state = config.STATE_PLAYING
        self.waiting_for_player_input = True
        self._add_sample_items()
        self._spawn_chests()
        self.ground_items = []
        self.message = ""
        self.message_timer = 0

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

        # Only update game logic when actively playing
        if self.state != config.STATE_PLAYING:
            return

        # Process turn if player has queued an action
        if not self.waiting_for_player_input:
            self.process_turn()

        # Check game over conditions
        if not self.warrior.is_alive:
            self.state = config.STATE_GAME_OVER
        elif not self.monster.is_alive:
            self.state = config.STATE_VICTORY

    def process_turn(self):
        """Process one complete turn (hero then monsters)."""
        # Hero turn
        self.warrior.on_turn_start()
        self.warrior.execute_turn(self.monster)

        # Check for chest collision after warrior moves
        self._check_chest_collision()

        # Check for ground item pickup after warrior moves
        self._check_ground_item_pickup()

        # Monster turns
        if self.monster.is_alive:
            self.monster.on_turn_start()
            self.monster.execute_turn(self.warrior)

        # Wait for next player input
        self.waiting_for_player_input = True

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
                # Try to add item to inventory
                if self.warrior.inventory.add_item(ground_item.item):
                    # Successfully added
                    self.ground_items.remove(ground_item)
                    self._show_message(f"Picked up {ground_item.item.name}!")
                else:
                    # Inventory full
                    self._show_message("Inventory is full!")

    def _show_message(self, message: str):
        """Show a message to the player."""
        self.message = message
        self.message_timer = self.message_duration

    def draw(self):
        """Draw all game objects."""
        self.screen.fill(config.BLACK)

        if self.state == config.STATE_PLAYING:
            # Draw world objects (chests and ground items) first (behind entities)
            for chest in self.chests:
                chest.draw(self.screen)

            for ground_item in self.ground_items:
                ground_item.draw(self.screen)

            # Draw attack range indicator
            self.combat_system.draw_attack_range_indicator(
                self.screen, self.warrior, self.monster
            )

            # Draw entities
            self.warrior.draw(self.screen)
            self.monster.draw(self.screen)

            # Draw combat UI
            self.combat_system.draw_combat_ui(self.screen, self.warrior, self.monster)

            # Draw message if active
            if self.message:
                self._draw_message()

            # Draw inventory button
            self.inventory_button.draw(self.screen)

        elif self.state == config.STATE_INVENTORY:
            # Draw the game in the background
            for chest in self.chests:
                chest.draw(self.screen)

            for ground_item in self.ground_items:
                ground_item.draw(self.screen)

            self.combat_system.draw_attack_range_indicator(
                self.screen, self.warrior, self.monster
            )
            self.warrior.draw(self.screen)
            self.monster.draw(self.screen)
            self.combat_system.draw_combat_ui(self.screen, self.warrior, self.monster)

            # Draw inventory overlay on top
            self.inventory_ui.draw(self.screen, self.warrior.inventory)

        elif self.state == config.STATE_VICTORY:
            self.draw_game_over_screen("VICTORY!", config.GREEN)

        elif self.state == config.STATE_GAME_OVER:
            self.draw_game_over_screen("GAME OVER!", config.RED)

        pygame.display.flip()

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

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0  # Delta time in seconds

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
