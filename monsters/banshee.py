"""Banshee monster - wailing spirit with ranged attacks."""

import pygame
from monsters.base_monster import BaseMonster
import visual_components


class Banshee(BaseMonster):
    """
    Banshee (Bean Sí) - A female spirit who wails to foretell death.

    Special traits:
    - Can attack from 2 tiles away (ranged wail)
    - Medium health, moderate damage
    - Ghostly appearance with floating animation
    """

    # Monster stats
    HEALTH = 60
    ATTACK_DAMAGE = 12
    SPEED = 1
    CHASE_RANGE = 6
    ATTACK_RANGE = 2  # Can wail from a distance
    DESCRIPTION = "Ghostly spirit - fast, ranged attacks"
    MONSTER_TYPE = "banshee"

    # Future: Can override execute_turn() for unique behavior
    # For example: teleport, fear effects, wailing that affects multiple tiles, etc.

    def draw_body(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Banshee's ghostly form."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Apply gentle floating effect
        center_y = visual_components.apply_floating_effect(
            center_y, self.frame_count, amplitude=3, speed=0.05
        )

        # Create semi-transparent surface for ghostly effect
        ghost_surface = visual_components.create_transparent_surface(
            int(width), int(height)
        )

        # Flowing robe/dress (pale white-blue)
        robe_color = (220, 230, 245, 180)  # Semi-transparent pale blue-white
        robe_points = [
            (width * 0.5, height * 0.2),  # Top (head area)
            (width * 0.3, height * 0.4),  # Left shoulder
            (width * 0.2, height * 0.9),  # Left bottom (flowing)
            (width * 0.4, height * 1.0),  # Left inner
            (width * 0.6, height * 1.0),  # Right inner
            (width * 0.8, height * 0.9),  # Right bottom (flowing)
            (width * 0.7, height * 0.4),  # Right shoulder
        ]
        pygame.draw.polygon(ghost_surface, robe_color, robe_points)

        # Head (pale, ghostly)
        head_color = (235, 240, 250, 200)
        head_radius = int(width * 0.15)
        pygame.draw.circle(
            ghost_surface,
            head_color,
            (int(width * 0.5), int(height * 0.15)),
            head_radius,
        )

        # Long flowing hair
        hair_color = (200, 210, 220, 160)
        pygame.draw.ellipse(
            ghost_surface,
            hair_color,
            (width * 0.35, height * 0.1, width * 0.3, height * 0.3),
        )

        # Wailing mouth (dark open mouth)
        mouth_color = (40, 40, 60, 220)
        mouth_center = (int(width * 0.5), int(height * 0.18))
        pygame.draw.circle(
            ghost_surface, mouth_color, mouth_center, int(head_radius * 0.4)
        )

        # Dark hollow eyes
        eye_color = (30, 30, 50, 200)
        left_eye = (int(width * 0.45), int(height * 0.13))
        right_eye = (int(width * 0.55), int(height * 0.13))
        eye_radius = int(head_radius * 0.25)
        pygame.draw.circle(ghost_surface, eye_color, left_eye, eye_radius)
        pygame.draw.circle(ghost_surface, eye_color, right_eye, eye_radius)

        # Blit to main surface
        screen.blit(ghost_surface, (center_x - width // 2, center_y - height // 2))

    def draw_details(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Banshee's wispy trailing effect."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Apply same floating effect for alignment
        center_y = visual_components.apply_floating_effect(
            center_y, self.frame_count, amplitude=3, speed=0.05
        )

        # Wispy trailing effect (animated)
        visual_components.draw_wispy_trail(
            screen,
            center_x,
            center_y,
            width,
            height,
            self.frame_count,
            color=(200, 220, 240),
            min_alpha=50,
            max_alpha=150,
        )
