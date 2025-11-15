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

    # Property delegation for backward compatibility with tests
    @property
    def displayed_health(self):
        return self.state.displayed_health

    @displayed_health.setter
    def displayed_health(self, value):
        self.state.displayed_health = value

    @property
    def animation_speed(self):
        return self.state.animation_speed

    @property
    def potion_glow_timer(self):
        return self.state.potion_glow_timer

    @property
    def potion_glow_duration(self):
        return self.state.potion_glow_duration

    @property
    def critical_health_timer(self):
        return self.state.critical_health_timer

    @property
    def critical_health_threshold(self):
        return self.state.critical_health_threshold

    @property
    def wood_color(self):
        return self.renderer.wood_color

    @property
    def wood_border(self):
        return self.renderer.wood_border

    @property
    def ornate_gold(self):
        return self.renderer.ornate_gold

    @property
    def health_green(self):
        return self.renderer.health_green

    @property
    def health_red(self):
        return self.renderer.health_red

    @property
    def health_critical(self):
        return self.renderer.health_critical

    @property
    def text_color(self):
        return self.renderer.text_color

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
