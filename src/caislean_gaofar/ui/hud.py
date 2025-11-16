"""HUD (Heads-Up Display) for displaying player stats and resources.

This module provides a coordinated interface for the HUD,
following separation of concerns with state management and rendering logic separated.
"""

import pygame
from caislean_gaofar.ui.hud_state import HUDState
from caislean_gaofar.ui.hud_renderer import HUDRenderer


class HUD:
    """Manages the player's heads-up display showing health, potions, and currency."""

    def __init__(self):
        """Initialize the HUD with separated state and renderer."""
        self.state = HUDState()
        self.renderer = HUDRenderer()

    def update(self, warrior, dt: float):
        """
        Update HUD animations and timers.

        Args:
            warrior: The warrior entity to track
            dt: Delta time in seconds
        """
        self.state.update(warrior, dt)

    def trigger_potion_glow(self):
        """Trigger visual feedback when a potion is used."""
        self.state.trigger_potion_glow()

    def draw(self, screen: pygame.Surface, warrior):
        """
        Draw the HUD on screen.

        Args:
            screen: Pygame surface to draw on
            warrior: The warrior entity to display stats for
        """
        self.renderer.draw(screen, warrior, self.state)
