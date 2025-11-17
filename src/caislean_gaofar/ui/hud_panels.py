"""Specialized panel renderers for HUD components.

This module contains focused renderer classes for each HUD panel,
following the Single Responsibility Principle.
"""

import pygame
import math
from caislean_gaofar.core import config
from caislean_gaofar.ui.ui_constants import UIConstants as UI
from caislean_gaofar.ui.ui_drawing_utils import UIDrawingUtils as Draw


class HealthPanelRenderer:
    """Renders the health panel with bar and numerical display."""

    def __init__(self, hud_x: int, hud_y: int, hud_width: int):
        """
        Initialize the health panel renderer.

        Args:
            hud_x: X position of the HUD
            hud_y: Y position of the HUD
            hud_width: Width of the HUD
        """
        self.hud_x = hud_x
        self.hud_y = hud_y
        self.hud_width = hud_width

    def draw(self, screen: pygame.Surface, warrior, state):
        """
        Draw the health panel.

        Args:
            screen: Pygame surface to draw on
            warrior: The warrior entity
            state: The HUD state
        """
        # Panel dimensions and position
        panel_width = self.hud_width - UI.HUD_PANEL_WIDTH_OFFSET
        panel_x = self.hud_x + UI.HUD_PANEL_PADDING
        panel_y = self.hud_y + UI.HEALTH_PANEL_Y
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, UI.HEALTH_PANEL_HEIGHT)

        # Draw panel
        Draw.draw_panel(screen, panel_rect)

        # Draw title
        font_title = pygame.font.Font(None, UI.FONT_SIZE_SMALL)
        title_text = font_title.render("Health", True, UI.ORNATE_GOLD)
        screen.blit(title_text, (panel_x + UI.HUD_PANEL_PADDING, panel_y + 8))

        # Health bar dimensions
        bar_width = panel_width - UI.HEALTH_BAR_MARGIN
        bar_x = panel_x + UI.HUD_PANEL_PADDING
        bar_y = panel_y + UI.HEALTH_BAR_Y_OFFSET
        bar_rect = pygame.Rect(bar_x, bar_y, bar_width, UI.HEALTH_BAR_HEIGHT)

        # Calculate health percentage
        health_percentage = warrior.health / warrior.max_health
        displayed_percentage = state.displayed_health / warrior.max_health

        # Determine bar color based on health
        if health_percentage > UI.HEALTH_THRESHOLD_HIGH:
            bar_color = UI.HEALTH_GREEN
        elif health_percentage > UI.HEALTH_THRESHOLD_MED:
            bar_color = UI.HEALTH_YELLOW
        else:
            bar_color = UI.HEALTH_RED

        # Draw health bar
        Draw.draw_progress_bar(screen, bar_rect, displayed_percentage, bar_color)

        # Draw numerical health display with shadow
        font_health = pygame.font.Font(None, UI.FONT_SIZE_MEDIUM)
        health_text = f"{int(warrior.health)}/{warrior.max_health} HP"
        Draw.draw_shadowed_text(
            screen,
            font_health,
            health_text,
            (bar_x + bar_width // 2, bar_y + UI.HEALTH_BAR_HEIGHT // 2),
            UI.TEXT_COLOR,
            centered=True,
        )


class PotionPanelRenderer:
    """Renders the potion panel with count and glow effect."""

    def __init__(self, hud_x: int, hud_y: int, hud_width: int):
        """Initialize the potion panel renderer."""
        self.hud_x = hud_x
        self.hud_y = hud_y
        self.hud_width = hud_width

    def draw(self, screen: pygame.Surface, warrior, state):
        """Draw the potion panel."""
        panel_width = self.hud_width - UI.HUD_PANEL_WIDTH_OFFSET
        panel_x = self.hud_x + UI.HUD_PANEL_PADDING
        panel_y = self.hud_y + UI.POTION_PANEL_Y
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, UI.POTION_PANEL_HEIGHT)

        Draw.draw_panel(screen, panel_rect)

        # Draw potion icon
        icon_x = panel_x + UI.POTION_ICON_OFFSET
        icon_y = panel_y + UI.POTION_ICON_OFFSET

        # Apply glow effect if potion was just used
        if state.is_potion_glowing():
            glow_alpha = int(
                UI.POTION_GLOW_ALPHA
                * (state.potion_glow_timer / state.potion_glow_duration)
            )
            glow_surface = pygame.Surface(
                (
                    UI.POTION_ICON_SIZE + UI.POTION_GLOW_RADIUS_OFFSET,
                    UI.POTION_ICON_SIZE + UI.POTION_GLOW_RADIUS_OFFSET,
                )
            )
            glow_surface.set_alpha(glow_alpha)
            pygame.draw.circle(
                glow_surface,
                UI.POTION_GLOW_COLOR,
                (
                    UI.POTION_ICON_SIZE // 2 + UI.POTION_GLOW_OFFSET,
                    UI.POTION_ICON_SIZE // 2 + UI.POTION_GLOW_OFFSET,
                ),
                UI.POTION_ICON_SIZE // 2 + UI.POTION_GLOW_OFFSET,
            )
            screen.blit(
                glow_surface,
                (icon_x - UI.POTION_GLOW_OFFSET, icon_y - UI.POTION_GLOW_OFFSET),
            )

        # Draw potion bottle
        self._draw_potion_icon(screen, icon_x, icon_y)

        # Draw potion count
        font_title = pygame.font.Font(None, UI.FONT_SIZE_INFO)
        title_text = font_title.render("Potions", True, UI.ORNATE_GOLD)
        screen.blit(title_text, (panel_x + 60, panel_y + 10))

        font_count = pygame.font.Font(None, UI.FONT_SIZE_SUBTITLE)
        potion_count = warrior.count_health_potions()
        count_text = font_count.render(f"x {potion_count}", True, UI.TEXT_COLOR)
        screen.blit(count_text, (panel_x + 60, panel_y + 30))

        # Draw usage hint
        font_hint = pygame.font.Font(None, UI.FONT_SIZE_HINT)
        hint_text = font_hint.render("Press P", True, config.GRAY)
        screen.blit(hint_text, (panel_x + 130, panel_y + 40))

    def _draw_potion_icon(self, screen: pygame.Surface, icon_x: int, icon_y: int):
        """Draw a stylized potion bottle icon."""
        # Bottle body
        bottle_rect = pygame.Rect(icon_x + 10, icon_y + 8, 20, 24)
        pygame.draw.rect(screen, UI.POTION_RED, bottle_rect)
        # Bottle neck
        neck_rect = pygame.Rect(icon_x + 14, icon_y + 4, 12, 8)
        pygame.draw.rect(screen, UI.POTION_RED, neck_rect)
        # Cork
        cork_rect = pygame.Rect(icon_x + 16, icon_y, 8, 6)
        pygame.draw.rect(screen, UI.POTION_CORK, cork_rect)
        # Highlight on bottle
        highlight = pygame.Rect(icon_x + 12, icon_y + 10, 4, 10)
        pygame.draw.rect(screen, UI.POTION_HIGHLIGHT, highlight)


class PortalPanelRenderer:
    """Renders the town portal panel with count."""

    def __init__(self, hud_x: int, hud_y: int, hud_width: int):
        """Initialize the portal panel renderer."""
        self.hud_x = hud_x
        self.hud_y = hud_y
        self.hud_width = hud_width

    def draw(self, screen: pygame.Surface, warrior):
        """Draw the portal panel."""
        panel_width = self.hud_width - UI.HUD_PANEL_WIDTH_OFFSET
        panel_x = self.hud_x + UI.HUD_PANEL_PADDING
        panel_y = self.hud_y + UI.PORTAL_PANEL_Y
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, UI.PORTAL_PANEL_HEIGHT)

        Draw.draw_panel(screen, panel_rect)

        # Draw portal icon
        icon_x = panel_x + UI.PORTAL_ICON_OFFSET
        icon_y = panel_y + UI.PORTAL_ICON_OFFSET
        center_x = icon_x + UI.PORTAL_ICON_SIZE // 2
        center_y = icon_y + UI.PORTAL_ICON_SIZE // 2

        # Draw magical portal effect
        pygame.draw.circle(screen, UI.PORTAL_OUTER, (center_x, center_y), 18, 3)
        pygame.draw.circle(screen, UI.PORTAL_MIDDLE, (center_x, center_y), 12, 2)
        pygame.draw.circle(screen, UI.PORTAL_INNER, (center_x, center_y), 6)

        # Draw portal count
        font_title = pygame.font.Font(None, UI.FONT_SIZE_INFO)
        title_text = font_title.render("Portals", True, UI.ORNATE_GOLD)
        screen.blit(title_text, (panel_x + 60, panel_y + 10))

        font_count = pygame.font.Font(None, UI.FONT_SIZE_SUBTITLE)
        portal_count = warrior.count_town_portals()
        count_text = font_count.render(f"x {portal_count}", True, UI.TEXT_COLOR)
        screen.blit(count_text, (panel_x + 60, panel_y + 30))

        # Draw usage hint
        font_hint = pygame.font.Font(None, UI.FONT_SIZE_HINT)
        hint_text = font_hint.render("Press T", True, config.GRAY)
        screen.blit(hint_text, (panel_x + 130, panel_y + 40))


class CurrencyPanelRenderer:
    """Renders the currency/gold panel."""

    def __init__(self, hud_x: int, hud_y: int, hud_width: int):
        """Initialize the currency panel renderer."""
        self.hud_x = hud_x
        self.hud_y = hud_y
        self.hud_width = hud_width

    def draw(self, screen: pygame.Surface, warrior):
        """Draw the currency panel."""
        panel_width = self.hud_width - UI.HUD_PANEL_WIDTH_OFFSET
        panel_x = self.hud_x + UI.HUD_PANEL_PADDING
        panel_y = self.hud_y + UI.CURRENCY_PANEL_Y
        panel_rect = pygame.Rect(
            panel_x, panel_y, panel_width, UI.CURRENCY_PANEL_HEIGHT
        )

        Draw.draw_panel(screen, panel_rect)

        # Draw gold coin icon
        coin_center_x = panel_x + 30
        coin_center_y = panel_y + 30

        # Multi-layer coin for depth
        Draw.draw_icon_circle(
            screen,
            (coin_center_x, coin_center_y),
            UI.CURRENCY_COIN_RADIUS,
            UI.GOLD_COIN_DARK,
            UI.GOLD_COIN_COLOR,
            inner_radius_offset=3,
        )
        pygame.draw.circle(
            screen,
            UI.GOLD_COIN_COLOR,
            (coin_center_x, coin_center_y),
            UI.CURRENCY_COIN_RADIUS - 6,
        )

        # Draw gold amount
        font_title = pygame.font.Font(None, UI.FONT_SIZE_SMALL)
        title_text = font_title.render("Gold", True, UI.ORNATE_GOLD)
        screen.blit(title_text, (panel_x + 60, panel_y + 8))

        font_gold = pygame.font.Font(None, UI.FONT_SIZE_SUBTITLE)
        gold_amount = warrior.count_gold()
        gold_text = font_gold.render(f"{gold_amount}", True, UI.TEXT_COLOR)
        screen.blit(gold_text, (panel_x + 60, panel_y + 26))


class StatPanelRenderer:
    """Renders attack and defense stat panels."""

    def __init__(self, hud_x: int, hud_y: int, hud_width: int):
        """Initialize the stat panel renderer."""
        self.hud_x = hud_x
        self.hud_y = hud_y
        self.hud_width = hud_width

    def draw_attack(self, screen: pygame.Surface, warrior):
        """Draw the attack stat panel."""
        panel_width = self.hud_width - UI.HUD_PANEL_WIDTH_OFFSET
        panel_x = self.hud_x + UI.HUD_PANEL_PADDING
        panel_y = self.hud_y + UI.ATTACK_PANEL_Y
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, UI.ATTACK_PANEL_HEIGHT)

        Draw.draw_panel(screen, panel_rect)

        # Draw sword icon
        self._draw_sword_icon(screen, panel_x + 20, panel_y + 15)

        # Draw attack value
        font_title = pygame.font.Font(None, UI.FONT_SIZE_SMALL)
        title_text = font_title.render("Attack", True, UI.ORNATE_GOLD)
        screen.blit(title_text, (panel_x + 60, panel_y + 8))

        font_stat = pygame.font.Font(None, UI.FONT_SIZE_SUBTITLE)
        attack_value = warrior.get_effective_attack_damage()
        stat_text = font_stat.render(f"{attack_value}", True, UI.TEXT_COLOR)
        screen.blit(stat_text, (panel_x + 60, panel_y + 26))

    def draw_defense(self, screen: pygame.Surface, warrior):
        """Draw the defense stat panel."""
        panel_width = self.hud_width - UI.HUD_PANEL_WIDTH_OFFSET
        panel_x = self.hud_x + UI.HUD_PANEL_PADDING
        panel_y = self.hud_y + UI.DEFENSE_PANEL_Y
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, UI.DEFENSE_PANEL_HEIGHT)

        Draw.draw_panel(screen, panel_rect)

        # Draw shield icon
        self._draw_shield_icon(screen, panel_x + 20, panel_y + 23)

        # Draw defense value
        font_title = pygame.font.Font(None, UI.FONT_SIZE_SMALL)
        title_text = font_title.render("Defense", True, UI.ORNATE_GOLD)
        screen.blit(title_text, (panel_x + 60, panel_y + 8))

        font_stat = pygame.font.Font(None, UI.FONT_SIZE_SUBTITLE)
        defense_value = warrior.inventory.get_total_defense_bonus()
        stat_text = font_stat.render(f"{defense_value}", True, UI.TEXT_COLOR)
        screen.blit(stat_text, (panel_x + 60, panel_y + 26))

    def _draw_sword_icon(self, screen: pygame.Surface, icon_x: int, icon_y: int):
        """Draw a sword icon."""
        # Blade
        pygame.draw.line(
            screen, UI.SWORD_COLOR, (icon_x, icon_y), (icon_x, icon_y + 25), 3
        )
        # Crossguard
        pygame.draw.line(
            screen,
            UI.SWORD_HANDLE_COLOR,
            (icon_x - 8, icon_y + 8),
            (icon_x + 8, icon_y + 8),
            3,
        )
        # Pommel
        pygame.draw.circle(screen, UI.SWORD_HANDLE_COLOR, (icon_x, icon_y + 28), 4)

    def _draw_shield_icon(
        self, screen: pygame.Surface, icon_center_x: int, icon_center_y: int
    ):
        """Draw a shield icon."""
        shield_points = [
            (icon_center_x, icon_center_y - 15),
            (icon_center_x + 12, icon_center_y - 10),
            (icon_center_x + 12, icon_center_y + 10),
            (icon_center_x, icon_center_y + 18),
            (icon_center_x - 12, icon_center_y + 10),
            (icon_center_x - 12, icon_center_y - 10),
        ]
        pygame.draw.polygon(screen, UI.SHIELD_COLOR, shield_points)
        pygame.draw.polygon(
            screen, UI.SHIELD_BORDER_COLOR, shield_points, UI.BORDER_WIDTH_THIN
        )


class XPPanelRenderer:
    """Renders the experience/level panel with progress bar."""

    def __init__(self, hud_x: int, hud_y: int, hud_width: int):
        """Initialize the XP panel renderer."""
        self.hud_x = hud_x
        self.hud_y = hud_y
        self.hud_width = hud_width

    def draw(self, screen: pygame.Surface, warrior):
        """Draw the XP panel."""
        panel_width = self.hud_width - UI.HUD_PANEL_WIDTH_OFFSET
        panel_x = self.hud_x + UI.HUD_PANEL_PADDING
        panel_y = self.hud_y + UI.XP_PANEL_Y
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, UI.XP_PANEL_HEIGHT)

        Draw.draw_panel(screen, panel_rect)

        # Draw title with level
        font_title = pygame.font.Font(None, UI.FONT_SIZE_TINY)
        level_text = font_title.render(
            f"Level {warrior.experience.current_level}", True, UI.ORNATE_GOLD
        )
        screen.blit(level_text, (panel_x + UI.HUD_PANEL_PADDING, panel_y + 6))

        # XP bar dimensions
        bar_width = panel_width - UI.HUD_PANEL_MARGIN
        bar_x = panel_x + UI.HUD_PANEL_PADDING
        bar_y = panel_y + UI.XP_BAR_Y_OFFSET
        bar_rect = pygame.Rect(bar_x, bar_y, bar_width, UI.XP_BAR_HEIGHT)

        # Calculate and draw XP progress
        xp_progress = warrior.experience.get_xp_progress()
        Draw.draw_progress_bar(screen, bar_rect, xp_progress, UI.ORNATE_GOLD)

        # Draw XP text
        font_xp = pygame.font.Font(None, UI.FONT_SIZE_DETAIL)
        if warrior.experience.is_max_level():
            xp_text = "MAX LEVEL"
        else:
            current_xp = warrior.experience.current_xp
            next_level_xp = warrior.experience.get_xp_for_next_level()
            xp_text = f"{current_xp}/{next_level_xp} XP"

        Draw.draw_shadowed_text(
            screen,
            font_xp,
            xp_text,
            (bar_x + bar_width // 2, bar_y + UI.XP_BAR_HEIGHT // 2),
            UI.TEXT_COLOR,
            shadow_offset=UI.TEXT_SHADOW_OFFSET_SMALL,
            centered=True,
        )


class InventoryPanelRenderer:
    """Renders the inventory panel with icon and hotkey hint."""

    def __init__(self, hud_x: int, hud_y: int, hud_width: int):
        """Initialize the inventory panel renderer."""
        self.hud_x = hud_x
        self.hud_y = hud_y
        self.hud_width = hud_width

    def draw(self, screen: pygame.Surface):
        """Draw the inventory panel."""
        panel_width = self.hud_width - UI.HUD_PANEL_WIDTH_OFFSET
        panel_x = self.hud_x + UI.HUD_PANEL_PADDING
        panel_y = self.hud_y + UI.INVENTORY_PANEL_Y
        panel_rect = pygame.Rect(
            panel_x, panel_y, panel_width, UI.INVENTORY_PANEL_HEIGHT
        )

        Draw.draw_panel(screen, panel_rect)

        # Draw backpack icon
        self._draw_backpack_icon(screen, panel_x + 15, panel_y + 15)

        # Draw title
        font_title = pygame.font.Font(None, UI.FONT_SIZE_INFO)
        title_text = font_title.render("Inventory", True, UI.ORNATE_GOLD)
        screen.blit(title_text, (panel_x + 60, panel_y + 15))

        # Draw usage hint
        font_hint = pygame.font.Font(None, UI.FONT_SIZE_HINT)
        hint_text = font_hint.render("Press I", True, config.GRAY)
        screen.blit(hint_text, (panel_x + 60, panel_y + 38))

    def _draw_backpack_icon(self, screen: pygame.Surface, icon_x: int, icon_y: int):
        """Draw a backpack/bag icon."""
        # Backpack body
        bag_rect = pygame.Rect(icon_x + 5, icon_y + 8, 30, 25)
        pygame.draw.rect(screen, UI.BAG_COLOR, bag_rect)
        pygame.draw.rect(screen, UI.BAG_BORDER, bag_rect, UI.BORDER_WIDTH_THIN)

        # Backpack flap
        flap_rect = pygame.Rect(icon_x + 5, icon_y + 3, 30, 10)
        pygame.draw.rect(screen, UI.BAG_FLAP_COLOR, flap_rect)
        pygame.draw.rect(screen, UI.BAG_BORDER, flap_rect, UI.BORDER_WIDTH_THIN)

        # Backpack straps
        pygame.draw.line(
            screen, UI.BAG_BORDER, (icon_x + 12, icon_y), (icon_x + 12, icon_y + 8), 3
        )
        pygame.draw.line(
            screen, UI.BAG_BORDER, (icon_x + 28, icon_y), (icon_x + 28, icon_y + 8), 3
        )

        # Buckle/clasp
        pygame.draw.circle(screen, UI.ORNATE_GOLD, (icon_x + 20, icon_y + 15), 3)


class SkillsPanelRenderer:
    """Renders the skills panel with notification badge."""

    def __init__(self, hud_x: int, hud_y: int, hud_width: int):
        """Initialize the skills panel renderer."""
        self.hud_x = hud_x
        self.hud_y = hud_y
        self.hud_width = hud_width

    def draw(self, screen: pygame.Surface, warrior):
        """Draw the skills panel."""
        panel_width = self.hud_width - UI.HUD_PANEL_WIDTH_OFFSET
        panel_x = self.hud_x + UI.HUD_PANEL_PADDING
        panel_y = self.hud_y + UI.SKILLS_PANEL_Y
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, UI.SKILLS_PANEL_HEIGHT)

        Draw.draw_panel(screen, panel_rect)

        # Draw skill book icon
        icon_x = panel_x + 15
        icon_y = panel_y + 10
        self._draw_book_icon(screen, icon_x, icon_y)

        # Draw skill points indicator if available
        skill_points = warrior.experience.get_available_skill_points()
        if skill_points > 0:
            badge_x = icon_x + UI.SKILL_BADGE_X_OFFSET
            badge_y = icon_y + UI.SKILL_BADGE_Y_OFFSET
            pygame.draw.circle(
                screen, config.RED, (badge_x, badge_y), UI.SKILL_BADGE_RADIUS
            )
            pygame.draw.circle(
                screen, config.WHITE, (badge_x, badge_y), UI.SKILL_BADGE_RADIUS, 1
            )

            font_badge = pygame.font.Font(None, UI.FONT_SIZE_HINT)
            badge_text = font_badge.render(str(skill_points), True, config.WHITE)
            badge_rect = badge_text.get_rect(center=(badge_x, badge_y))
            screen.blit(badge_text, badge_rect)

        # Draw title
        font_title = pygame.font.Font(None, UI.FONT_SIZE_INFO)
        title_text = font_title.render("Skills", True, UI.ORNATE_GOLD)
        screen.blit(title_text, (panel_x + 60, panel_y + 10))

        # Draw level info
        font_level = pygame.font.Font(None, UI.FONT_SIZE_HINT)
        level_text = font_level.render(
            f"Lvl {warrior.experience.current_level}", True, UI.TEXT_COLOR
        )
        screen.blit(level_text, (panel_x + 110, panel_y + 12))

        # Draw usage hint
        font_hint = pygame.font.Font(None, UI.FONT_SIZE_HINT)
        hint_text = font_hint.render("Press C", True, config.GRAY)
        screen.blit(hint_text, (panel_x + 60, panel_y + 33))

    def _draw_book_icon(self, screen: pygame.Surface, icon_x: int, icon_y: int):
        """Draw a skill book icon."""
        # Book cover
        book_rect = pygame.Rect(icon_x + 5, icon_y + 3, 25, 35)
        pygame.draw.rect(screen, UI.BOOK_COLOR, book_rect)
        pygame.draw.rect(screen, UI.BOOK_BORDER, book_rect, UI.BORDER_WIDTH_THIN)

        # Book pages
        pages_rect = pygame.Rect(icon_x + 8, icon_y + 6, 19, 29)
        pygame.draw.rect(screen, UI.BOOK_PAGES_COLOR, pages_rect)

        # Book spine decoration
        spine_x = icon_x + 7
        for i in range(3):
            pygame.draw.line(
                screen,
                UI.ORNATE_GOLD,
                (spine_x, icon_y + 10 + i * 8),
                (spine_x, icon_y + 15 + i * 8),
                2,
            )


class WarningRenderer:
    """Renders visual warnings (e.g., critical health)."""

    def draw_critical_health_warning(self, screen: pygame.Surface, state):
        """
        Draw a visual warning when health is critically low.

        Args:
            screen: Pygame surface to draw on
            state: The current HUD state
        """
        # Pulsing red vignette effect
        alpha = int(
            UI.CRITICAL_HEALTH_ALPHA_BASE
            * (
                0.5
                + 0.5
                * math.sin(
                    state.critical_health_timer / UI.CRITICAL_HEALTH_PULSE_DIVISOR
                )
            )
        )

        # Create semi-transparent red overlay at game area edges
        overlay = pygame.Surface((config.GAME_AREA_WIDTH, config.GAME_AREA_HEIGHT))
        overlay.set_alpha(alpha)
        overlay.fill(UI.HEALTH_CRITICAL)

        # Draw vignette (darker at edges)
        vignette_width = UI.CRITICAL_HEALTH_VIGNETTE_WIDTH
        # Top
        pygame.draw.rect(
            overlay, UI.HEALTH_CRITICAL, (0, 0, config.GAME_AREA_WIDTH, vignette_width)
        )
        # Bottom
        pygame.draw.rect(
            overlay,
            UI.HEALTH_CRITICAL,
            (
                0,
                config.GAME_AREA_HEIGHT - vignette_width,
                config.GAME_AREA_WIDTH,
                vignette_width,
            ),
        )
        # Left
        pygame.draw.rect(
            overlay, UI.HEALTH_CRITICAL, (0, 0, vignette_width, config.GAME_AREA_HEIGHT)
        )
        # Right
        pygame.draw.rect(
            overlay,
            UI.HEALTH_CRITICAL,
            (
                config.GAME_AREA_WIDTH - vignette_width,
                0,
                vignette_width,
                config.GAME_AREA_HEIGHT,
            ),
        )

        screen.blit(overlay, (0, 0))

        # Draw warning text (pulsing)
        if int(state.critical_health_timer / UI.CRITICAL_HEALTH_BLINK_RATE) % 2 == 0:
            font_warning = pygame.font.Font(None, UI.FONT_SIZE_NORMAL)
            Draw.draw_shadowed_text(
                screen,
                font_warning,
                "LOW HEALTH!",
                (
                    config.GAME_AREA_WIDTH // 2,
                    config.GAME_AREA_HEIGHT - UI.CRITICAL_HEALTH_TEXT_Y,
                ),
                UI.HEALTH_CRITICAL,
                centered=True,
            )
