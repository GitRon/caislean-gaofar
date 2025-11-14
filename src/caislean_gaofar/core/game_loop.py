"""Core game loop management."""

import pygame
from typing import Callable
from caislean_gaofar.core import config


class GameLoop:
    """Manages the core game loop without business logic."""

    def __init__(self, clock: pygame.time.Clock):
        """
        Initialize the game loop.

        Args:
            clock: Pygame clock for frame rate control
        """
        self.clock = clock
        self.running = True

    def run(
        self,
        handle_events: Callable[[], None],
        update: Callable[[float], None],
        draw: Callable[[], None],
    ):
        """
        Execute the main game loop.

        Args:
            handle_events: Callback to handle pygame events
            update: Callback to update game state (receives delta time)
            draw: Callback to draw game objects
        """
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0  # Delta time in seconds

            handle_events()
            update(dt)
            draw()

        pygame.quit()

    def stop(self):
        """Stop the game loop."""
        self.running = False
