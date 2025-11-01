"""Main game class and game loop."""

import pygame
from warrior import Warrior
from monster import Monster
from combat import CombatSystem
from inventory_ui import InventoryUI
from item import Item, ItemType
import config


class Game:
    """Main game class that manages the game loop and state."""

    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = config.STATE_PLAYING

        # Initialize game objects
        self.warrior = Warrior(100, config.SCREEN_HEIGHT // 2)
        self.monster = Monster(config.SCREEN_WIDTH - 150, config.SCREEN_HEIGHT // 2)
        self.combat_system = CombatSystem()
        self.inventory_ui = InventoryUI()

        # Add sample items to warrior's inventory
        self._add_sample_items()

    def _add_sample_items(self):
        """Add sample items to the warrior's inventory for testing."""
        # Create sample items
        iron_sword = Item("Iron Sword", ItemType.WEAPON, "A basic sword", attack_bonus=10)
        steel_sword = Item("Steel Sword", ItemType.WEAPON, "A stronger sword", attack_bonus=20)
        leather_armor = Item("Leather Armor", ItemType.ARMOR, "Basic protection", defense_bonus=5, health_bonus=20)
        health_potion = Item("Health Potion", ItemType.CONSUMABLE, "Restores health", health_bonus=30)
        gold_coin = Item("Gold Coin", ItemType.MISC, "Shiny currency")

        # Add items to inventory
        self.warrior.inventory.add_item(iron_sword)  # Goes to weapon slot
        self.warrior.inventory.add_item(leather_armor)  # Goes to armor slot
        self.warrior.inventory.add_item(steel_sword)  # Goes to backpack
        self.warrior.inventory.add_item(health_potion)  # Goes to backpack
        self.warrior.inventory.add_item(gold_coin)  # Goes to backpack

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.state != config.STATE_PLAYING:
                    # Restart game
                    self.restart()
                elif event.key == pygame.K_i and self.state in [config.STATE_PLAYING, config.STATE_INVENTORY]:
                    # Toggle inventory
                    if self.state == config.STATE_PLAYING:
                        self.state = config.STATE_INVENTORY
                    else:
                        self.state = config.STATE_PLAYING

            # Handle inventory input when inventory is open
            if self.state == config.STATE_INVENTORY:
                self.inventory_ui.handle_input(event, self.warrior.inventory)

    def restart(self):
        """Restart the game."""
        self.warrior = Warrior(100, config.SCREEN_HEIGHT // 2)
        self.monster = Monster(config.SCREEN_WIDTH - 150, config.SCREEN_HEIGHT // 2)
        self.state = config.STATE_PLAYING

    def update(self, dt: float):
        """
        Update game state.

        Args:
            dt: Delta time since last update
        """
        # Only update game logic when actively playing
        if self.state != config.STATE_PLAYING:
            return

        current_time = pygame.time.get_ticks()

        # Handle warrior input
        keys = pygame.key.get_pressed()
        self.warrior.handle_input(keys)

        # Check for warrior attacks
        self.combat_system.check_attack_input(self.warrior, self.monster, current_time)

        # Update monster AI
        self.monster.update(dt, self.warrior, current_time)

        # Check game over conditions
        if not self.warrior.is_alive:
            self.state = config.STATE_GAME_OVER
        elif not self.monster.is_alive:
            self.state = config.STATE_VICTORY

    def draw(self):
        """Draw all game objects."""
        self.screen.fill(config.BLACK)

        if self.state == config.STATE_PLAYING:
            # Draw attack range indicator
            self.combat_system.draw_attack_range_indicator(self.screen, self.warrior, self.monster)

            # Draw entities
            self.warrior.draw(self.screen)
            self.monster.draw(self.screen)

            # Draw combat UI
            self.combat_system.draw_combat_ui(self.screen, self.warrior, self.monster)

        elif self.state == config.STATE_INVENTORY:
            # Draw the game in the background
            self.combat_system.draw_attack_range_indicator(self.screen, self.warrior, self.monster)
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
        text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)

        # Restart instruction
        restart_text = font_small.render("Press R to Restart", True, config.WHITE)
        restart_rect = restart_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)

        # Exit instruction
        exit_text = font_small.render("Press ESC to Exit", True, config.WHITE)
        exit_rect = exit_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(exit_text, exit_rect)

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0  # Delta time in seconds

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
