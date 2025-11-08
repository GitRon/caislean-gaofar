"""Main menu screen for the game."""

import pygame
from typing import Optional
import config
from save_game import SaveGame


class MainMenu:
    """Main menu for selecting New Game or Load Game."""

    def __init__(self, screen: pygame.Surface):
        """
        Initialize the main menu.

        Args:
            screen: Pygame surface to draw on
        """
        self.screen = screen
        self.selected_option = 0  # 0 = New Game, 1+ = Load slots
        self.save_files = []
        self.running = True
        self.result = None  # Will be ("new", None) or ("load", save_data)

    def load_save_files(self):
        """Load available save files."""
        self.save_files = SaveGame.list_save_files()

    def run(self) -> Optional[tuple]:
        """
        Run the main menu loop.

        Returns:
            Tuple of ("new", None) for new game, or ("load", save_data) for load game
            Returns None if the user quits
        """
        self.load_save_files()
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            clock.tick(config.FPS)

        return self.result

    def handle_events(self):
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.result = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.result = None
                elif event.key == pygame.K_UP:
                    self.selected_option = max(0, self.selected_option - 1)
                elif event.key == pygame.K_DOWN:
                    max_option = len(self.save_files)  # 0 = New Game, 1+ = saves
                    self.selected_option = min(max_option, self.selected_option + 1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.select_option()
                elif event.key == pygame.K_DELETE and self.selected_option > 0:
                    # Delete selected save file
                    self.delete_selected_save()

    def select_option(self):
        """Select the currently highlighted option."""
        if self.selected_option == 0:
            # New Game
            self.result = ("new", None)
            self.running = False
        else:
            # Load Game
            save_index = self.selected_option - 1
            if save_index < len(self.save_files):
                save_file = self.save_files[save_index]
                save_data = SaveGame.load_game(save_file["filename"])
                if save_data:
                    self.result = ("load", save_data)
                    self.running = False

    def delete_selected_save(self):
        """Delete the currently selected save file."""
        if self.selected_option > 0:
            save_index = self.selected_option - 1
            if save_index < len(self.save_files):
                save_file = self.save_files[save_index]
                SaveGame.delete_save(save_file["filename"])
                # Reload save files
                self.load_save_files()
                # Adjust selection if needed
                if self.selected_option > len(self.save_files):
                    self.selected_option = len(self.save_files)

    def draw(self):
        """Draw the main menu."""
        self.screen.fill(config.BLACK)

        # Draw title
        font_title = pygame.font.Font(None, 72)
        title_text = font_title.render(config.TITLE, True, config.WHITE)
        title_rect = title_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4)
        )
        self.screen.blit(title_text, title_rect)

        # Draw subtitle
        font_small = pygame.font.Font(None, 24)
        subtitle_text = font_small.render(
            "An Irish Folklore RPG", True, config.GRAY
        )
        subtitle_rect = subtitle_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4 + 50)
        )
        self.screen.blit(subtitle_text, subtitle_rect)

        # Draw options
        font_option = pygame.font.Font(None, 36)
        y_start = config.SCREEN_HEIGHT // 2

        # New Game option
        new_game_color = config.YELLOW if self.selected_option == 0 else config.WHITE
        new_game_text = font_option.render("New Game", True, new_game_color)
        new_game_rect = new_game_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, y_start)
        )
        self.screen.blit(new_game_text, new_game_rect)

        # Load Game section
        if self.save_files:
            # Draw "Load Game:" header
            load_header = font_small.render("Load Game:", True, config.GRAY)
            load_header_rect = load_header.get_rect(
                center=(config.SCREEN_WIDTH // 2, y_start + 50)
            )
            self.screen.blit(load_header, load_header_rect)

            # Draw save files
            for i, save_file in enumerate(self.save_files):
                y_pos = y_start + 90 + (i * 40)
                is_selected = (self.selected_option - 1) == i

                # Format save file info
                timestamp = save_file["timestamp"].split("T")
                date_str = timestamp[0] if len(timestamp) > 0 else "Unknown"
                time_str = (
                    timestamp[1].split(".")[0] if len(timestamp) > 1 else ""
                )

                save_text = f"{save_file['filename']} - {date_str} {time_str}"
                save_color = config.YELLOW if is_selected else config.WHITE

                save_render = font_small.render(save_text, True, save_color)
                save_rect = save_render.get_rect(
                    center=(config.SCREEN_WIDTH // 2, y_pos)
                )
                self.screen.blit(save_render, save_rect)

                # Show delete hint if selected
                if is_selected:
                    delete_hint = font_small.render(
                        "(Press DELETE to remove)", True, config.RED
                    )
                    delete_rect = delete_hint.get_rect(
                        center=(config.SCREEN_WIDTH // 2, y_pos + 20)
                    )
                    self.screen.blit(delete_hint, delete_rect)
        else:
            # No save files
            no_saves = font_small.render("No saved games", True, config.GRAY)
            no_saves_rect = no_saves.get_rect(
                center=(config.SCREEN_WIDTH // 2, y_start + 70)
            )
            self.screen.blit(no_saves, no_saves_rect)

        # Draw controls
        controls_y = config.SCREEN_HEIGHT - 60
        controls = [
            "UP/DOWN: Select",
            "ENTER/SPACE: Confirm",
            "ESC: Quit",
        ]
        for i, control in enumerate(controls):
            control_text = font_small.render(control, True, config.GRAY)
            control_rect = control_text.get_rect(
                center=(config.SCREEN_WIDTH // 2, controls_y + (i * 20))
            )
            self.screen.blit(control_text, control_rect)
