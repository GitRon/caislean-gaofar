"""Entry point for the Caislean Gaofar game."""

import pygame
from caislean_gaofar.core.game import Game
from caislean_gaofar.ui.main_menu import MainMenu
from caislean_gaofar.core import config


def main() -> None:
    """Start the game."""
    # Initialize pygame for the menu
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.TITLE)

    # Show main menu
    menu = MainMenu(screen)
    menu_result = menu.run()

    if menu_result is None:
        # User quit from menu
        pygame.quit()
        return

    action, data = menu_result

    # Create game instance
    game = Game()

    if action == "load" and data is not None:
        # Load saved game
        game.load_game_state(data)

    # Run the game (new game or loaded game)
    game.run()


if __name__ == "__main__":
    main()
