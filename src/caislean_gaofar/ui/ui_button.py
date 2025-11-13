"""UI button component for on-screen clickable buttons"""

import pygame
from typing import Tuple


class Button:
    """A clickable button for the UI"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font_size: int = 24,
        bg_color: Tuple[int, int, int] = (60, 60, 70),
        hover_color: Tuple[int, int, int] = (80, 80, 90),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        border_color: Tuple[int, int, int] = (100, 100, 120),
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.is_hovered = False

    def draw(self, screen: pygame.Surface):
        """Draw the button"""
        # Update hover state
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Draw button background
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(screen, color, self.rect)

        # Draw border
        border_width = 3 if self.is_hovered else 2
        pygame.draw.rect(screen, self.border_color, self.rect, border_width)

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_x = self.rect.centerx - text_surface.get_width() // 2
        text_y = self.rect.centery - text_surface.get_height() // 2
        screen.blit(text_surface, (text_x, text_y))

    def is_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """Check if the button was clicked at the given mouse position"""
        return self.rect.collidepoint(mouse_pos)
