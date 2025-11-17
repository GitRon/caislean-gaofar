"""Rendering logic for HUD (Heads-Up Display)."""

import pygame
from caislean_gaofar.core import config
from caislean_gaofar.ui.hud_state import HUDState
from caislean_gaofar.ui.hud_panels import (
    HealthPanelRenderer,
    PotionPanelRenderer,
    PortalPanelRenderer,
    CurrencyPanelRenderer,
    StatPanelRenderer,
    XPPanelRenderer,
    InventoryPanelRenderer,
    SkillsPanelRenderer,
    WarningRenderer,
)
from caislean_gaofar.ui.ui_constants import UIConstants


class HUDRenderer:
    """Handles rendering of the HUD using specialized panel renderers."""

    def __init__(self):
        """Initialize the HUD renderer with specialized panel renderers."""
        # HUD positioning (right side of screen)
        self.x = config.GAME_AREA_WIDTH
        self.y = 0
        self.width = config.HUD_WIDTH
        self.height = config.HUD_HEIGHT

        # Initialize specialized panel renderers
        self.health_renderer = HealthPanelRenderer(self.x, self.y, self.width)
        self.potion_renderer = PotionPanelRenderer(self.x, self.y, self.width)
        self.portal_renderer = PortalPanelRenderer(self.x, self.y, self.width)
        self.currency_renderer = CurrencyPanelRenderer(self.x, self.y, self.width)
        self.stat_renderer = StatPanelRenderer(self.x, self.y, self.width)
        self.xp_renderer = XPPanelRenderer(self.x, self.y, self.width)
        self.inventory_renderer = InventoryPanelRenderer(self.x, self.y, self.width)
        self.skills_renderer = SkillsPanelRenderer(self.x, self.y, self.width)
        self.warning_renderer = WarningRenderer()

    def draw(self, screen: pygame.Surface, warrior, state: HUDState):
        """
        Draw the HUD on screen.

        Args:
            screen: Pygame surface to draw on
            warrior: The warrior entity to display stats for
            state: The current HUD state
        """
        # Draw HUD background
        hud_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, UIConstants.WOOD_BORDER, hud_rect)

        # Draw all HUD panels using specialized renderers
        self.health_renderer.draw(screen, warrior, state)
        self.potion_renderer.draw(screen, warrior, state)
        self.portal_renderer.draw(screen, warrior)
        self.currency_renderer.draw(screen, warrior)
        self.stat_renderer.draw_attack(screen, warrior)
        self.stat_renderer.draw_defense(screen, warrior)
        self.xp_renderer.draw(screen, warrior)
        self.inventory_renderer.draw(screen)
        self.skills_renderer.draw(screen, warrior)

        # Draw critical health warning if needed
        if state.is_critical_health(warrior):
            self.warning_renderer.draw_critical_health_warning(screen, state)
