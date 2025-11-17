"""Renderer for dungeon entrance icons on the world map.

This module handles rendering of different types of dungeon entrances
with specialized icons for caves, castles, and generic dungeons.
"""

import pygame
from caislean_gaofar.core import config
from caislean_gaofar.ui.ui_constants import UIConstants as UI
from caislean_gaofar.ui.ui_drawing_utils import UIDrawingUtils as Draw


class DungeonEntranceRenderer:
    """Handles rendering of dungeon entrance icons."""

    def draw_entrance(
        self,
        screen: pygame.Surface,
        terrain_char: str,
        x: int,
        y: int,
        size: int,
    ):
        """
        Draw a dungeon entrance icon based on terrain type.

        Args:
            screen: Pygame surface to draw on
            terrain_char: Terrain character determining entrance type
            x: Screen x position
            y: Screen y position
            size: Tile size
        """
        if terrain_char == "C":  # Cave entrance
            self._draw_cave_entrance(screen, x, y, size)
        elif terrain_char == "K":  # Castle entrance
            self._draw_castle_entrance(screen, x, y, size)
        elif terrain_char == "D":  # Generic dungeon entrance
            self._draw_dungeon_entrance(screen, x, y, size)

    def draw_entrance_name(
        self,
        screen: pygame.Surface,
        dungeon_name: str,
        x: int,
        y: int,
        size: int,
    ):
        """
        Draw dungeon name above entrance.

        Args:
            screen: Pygame surface to draw on
            dungeon_name: Name of the dungeon
            x: Screen x position
            y: Screen y position
            size: Tile size
        """
        font = pygame.font.Font(None, 20)
        text_x = x + size // 2
        text_y = y - UI.ENTRANCE_ICON_NAME_OFFSET

        Draw.draw_message_box(
            screen,
            dungeon_name,
            (text_x, text_y),
            font,
            text_color=config.WHITE,
            bg_color=config.BLACK,
            border_color=config.WHITE,
            padding=UI.ENTRANCE_ICON_TEXT_BG_PADDING,
            centered=True,
        )

    def _draw_cave_entrance(self, screen: pygame.Surface, x: int, y: int, size: int):
        """
        Draw a cave entrance icon.

        Args:
            screen: Pygame surface to draw on
            x: Screen x position
            y: Screen y position
            size: Tile size
        """
        center = (x + size // 2, y + size // 2)
        radius = size // 2

        # Background circle for visibility
        Draw.draw_entrance_background_circle(screen, center, radius, UI.CAVE_BG_COLOR)

        # Main cave opening (arch shape)
        arch_rect = pygame.Rect(
            x + int(size * UI.CAVE_ARCH_X_FRACTION),
            y + int(size * UI.CAVE_ARCH_Y_FRACTION),
            int(size * UI.CAVE_ARCH_WIDTH_FRACTION),
            int(size * UI.CAVE_ARCH_HEIGHT_FRACTION),
        )
        pygame.draw.ellipse(screen, UI.CAVE_COLOR, arch_rect)

        # Dark inner cave (very dark to show depth)
        inner_rect = pygame.Rect(
            x + int(size * UI.CAVE_INNER_X_FRACTION),
            y + int(size * UI.CAVE_INNER_Y_FRACTION),
            int(size * UI.CAVE_INNER_WIDTH_FRACTION),
            int(size * UI.CAVE_INNER_HEIGHT_FRACTION),
        )
        pygame.draw.ellipse(screen, UI.CAVE_INNER_COLOR, inner_rect)

        # Rocky edges (small circles)
        rock_positions = [
            (
                x + int(size * UI.CAVE_ARCH_X_FRACTION),
                y + int(size * UI.CAVE_INNER_Y_FRACTION),
            ),
            (
                x
                + int(
                    size
                    * (
                        UI.CAVE_ARCH_X_FRACTION
                        + UI.CAVE_ARCH_WIDTH_FRACTION
                        - UI.CAVE_ARCH_X_FRACTION
                    )
                ),
                y + int(size * UI.CAVE_INNER_Y_FRACTION),
            ),
            (
                x + int(size * UI.CAVE_INNER_X_FRACTION),
                y + int(size * UI.CAVE_ARCH_Y_FRACTION),
            ),
            (
                x
                + int(size * (UI.CAVE_INNER_X_FRACTION + UI.CAVE_INNER_WIDTH_FRACTION)),
                y + int(size * UI.CAVE_ARCH_Y_FRACTION),
            ),
        ]
        rock_radius = int(size * UI.CAVE_ROCK_RADIUS_FRACTION)
        for rx, ry in rock_positions:
            pygame.draw.circle(
                screen, UI.CAVE_ROCK_COLOR, (int(rx), int(ry)), rock_radius
            )

    def _draw_castle_entrance(self, screen: pygame.Surface, x: int, y: int, size: int):
        """
        Draw a castle entrance icon.

        Args:
            screen: Pygame surface to draw on
            x: Screen x position
            y: Screen y position
            size: Tile size
        """
        center = (x + size // 2, y + size // 2)
        radius = size // 2

        # Background circle for visibility
        Draw.draw_entrance_background_circle(screen, center, radius, UI.CASTLE_BG_COLOR)

        # Main gate structure
        gate_rect = pygame.Rect(
            x + int(size * UI.CASTLE_GATE_X_FRACTION),
            y + int(size * UI.CASTLE_GATE_Y_FRACTION),
            int(size * UI.CASTLE_GATE_WIDTH_FRACTION),
            int(size * UI.CASTLE_GATE_HEIGHT_FRACTION),
        )
        pygame.draw.rect(screen, UI.CASTLE_STONE_COLOR, gate_rect)

        # Dark gate opening
        opening_rect = pygame.Rect(
            x + int(size * UI.CASTLE_OPENING_X_FRACTION),
            y + int(size * UI.CASTLE_OPENING_Y_FRACTION),
            int(size * UI.CASTLE_OPENING_WIDTH_FRACTION),
            int(size * UI.CASTLE_OPENING_HEIGHT_FRACTION),
        )
        pygame.draw.rect(screen, UI.CASTLE_DARK_STONE, opening_rect)

        # Battlements on top (crenellations)
        battlement_width = int(size * UI.CASTLE_BATTLEMENT_WIDTH_FRACTION)
        for i in range(3):
            if i % 2 == 0:  # Every other one
                bx = x + int(size * UI.CASTLE_GATE_X_FRACTION) + i * battlement_width
                by = y + int(size * UI.CASTLE_BATTLEMENT_Y_FRACTION)
                bh = int(size * UI.CASTLE_BATTLEMENT_HEIGHT_FRACTION)
                pygame.draw.rect(
                    screen,
                    UI.CASTLE_STONE_COLOR,
                    (bx, by, battlement_width, bh),
                )

        # Stone blocks pattern
        for i in range(3):
            by = (
                y
                + int(size * UI.CASTLE_GATE_Y_FRACTION)
                + i * int(size * UI.CASTLE_GATE_WIDTH_FRACTION / 3)
            )
            pygame.draw.line(
                screen,
                UI.CASTLE_DARK_STONE,
                (x + int(size * UI.CASTLE_GATE_X_FRACTION), by),
                (
                    x
                    + int(
                        size
                        * (UI.CASTLE_GATE_X_FRACTION + UI.CASTLE_GATE_WIDTH_FRACTION)
                    ),
                    by,
                ),
                UI.BORDER_WIDTH_THIN,
            )

    def _draw_dungeon_entrance(self, screen: pygame.Surface, x: int, y: int, size: int):
        """
        Draw a generic dungeon entrance icon.

        Args:
            screen: Pygame surface to draw on
            x: Screen x position
            y: Screen y position
            size: Tile size
        """
        center = (x + size // 2, y + size // 2)
        radius = size // 2

        # Background circle for visibility
        Draw.draw_entrance_background_circle(
            screen, center, radius, UI.DUNGEON_BG_COLOR
        )

        # Outer glow
        glow_radius = int(size * UI.DUNGEON_GLOW_RADIUS_FRACTION)
        pygame.draw.circle(
            screen, UI.DUNGEON_GLOW_COLOR, center, glow_radius + UI.DUNGEON_GLOW_WIDTH
        )

        # Inner portal
        portal_radius = int(size * UI.DUNGEON_PORTAL_RADIUS_FRACTION)
        pygame.draw.circle(screen, UI.DUNGEON_COLOR, center, portal_radius + 1)

        # Dark center
        center_radius = int(size * UI.DUNGEON_CENTER_RADIUS_FRACTION)
        pygame.draw.circle(screen, UI.DUNGEON_CENTER_COLOR, center, center_radius)
