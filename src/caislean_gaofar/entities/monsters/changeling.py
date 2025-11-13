"""Changeling monster - fairy child left in place of human baby."""

import pygame
import math
from caislean_gaofar.entities.monsters.base_monster import BaseMonster
from caislean_gaofar.ui import visual_components


class Changeling(BaseMonster):
    """
    Changeling - A fairy child secretly left in place of a human baby.

    Special traits:
    - Deceptively dangerous
    - Twitchy, unsettling movements
    - Moderate health and damage
    - Child-like appearance with disturbing features
    """

    # Monster stats
    HEALTH = 50
    ATTACK_DAMAGE = 14
    SPEED = 1
    CHASE_RANGE = 4
    ATTACK_RANGE = 1
    DESCRIPTION = "Fairy child - deceptively dangerous"
    MONSTER_TYPE = "changeling"

    # Future: Can override execute_turn() for unique behavior
    # For example: confuse player controls, summon fairy allies, steal items,
    # mimic player appearance, etc.

    def draw_body(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Changeling's unsettling child-like form."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Twitchy, unnatural movements
        twitch_x = int(2 * math.sin(self.frame_count * 0.2))
        twitch_y = int(2 * math.cos(self.frame_count * 0.25))
        adjusted_x = center_x + twitch_x
        adjusted_y = center_y + twitch_y

        # Small body (child-like, but wrong proportions)
        body_color = (200, 190, 180)
        # Oversized head for creepy effect
        head_radius = int(width * 0.22)
        head_pos = (int(adjusted_x), int(adjusted_y - height * 0.2))
        pygame.draw.circle(screen, body_color, head_pos, head_radius)

        # Small body/dress
        dress_color = (220, 200, 180)
        dress_points = [
            (adjusted_x - width * 0.15, adjusted_y),
            (adjusted_x + width * 0.15, adjusted_y),
            (adjusted_x + width * 0.25, adjusted_y + height * 0.4),
            (adjusted_x - width * 0.25, adjusted_y + height * 0.4),
        ]
        pygame.draw.polygon(screen, dress_color, dress_points)

        # Unsettling large eyes (too big, too knowing)
        eye_white = (240, 240, 255)
        eye_color = (20, 20, 60)  # Deep, unnatural blue
        # Left eye
        left_eye_pos = (
            int(adjusted_x - head_radius * 0.4),
            int(adjusted_y - height * 0.22),
        )
        pygame.draw.circle(screen, eye_white, left_eye_pos, int(head_radius * 0.35))
        pygame.draw.circle(screen, eye_color, left_eye_pos, int(head_radius * 0.25))
        # Right eye
        right_eye_pos = (
            int(adjusted_x + head_radius * 0.4),
            int(adjusted_y - height * 0.22),
        )
        pygame.draw.circle(screen, eye_white, right_eye_pos, int(head_radius * 0.35))
        pygame.draw.circle(screen, eye_color, right_eye_pos, int(head_radius * 0.25))

        # Unnatural gleam in eyes
        gleam = (200, 200, 255)
        pygame.draw.circle(screen, gleam, left_eye_pos, int(head_radius * 0.1))
        pygame.draw.circle(screen, gleam, right_eye_pos, int(head_radius * 0.1))

        # Too-wide smile (unsettling)
        smile_color = (100, 80, 80)
        smile_rect = pygame.Rect(
            adjusted_x - head_radius * 0.5,
            adjusted_y - height * 0.1,
            head_radius,
            head_radius * 0.3,
        )
        pygame.draw.arc(screen, smile_color, smile_rect, 0, math.pi, 2)

        # Thin, spindly limbs (unnatural)
        limb_color = (190, 180, 170)
        # Arms
        pygame.draw.line(
            screen,
            limb_color,
            (int(adjusted_x - width * 0.15), int(adjusted_y + height * 0.05)),
            (int(adjusted_x - width * 0.25), int(adjusted_y + height * 0.25)),
            4,
        )
        pygame.draw.line(
            screen,
            limb_color,
            (int(adjusted_x + width * 0.15), int(adjusted_y + height * 0.05)),
            (int(adjusted_x + width * 0.25), int(adjusted_y + height * 0.25)),
            4,
        )

        # Legs
        pygame.draw.line(
            screen,
            limb_color,
            (int(adjusted_x - width * 0.1), int(adjusted_y + height * 0.4)),
            (int(adjusted_x - width * 0.15), int(adjusted_y + height * 0.6)),
            4,
        )
        pygame.draw.line(
            screen,
            limb_color,
            (int(adjusted_x + width * 0.1), int(adjusted_y + height * 0.4)),
            (int(adjusted_x + width * 0.15), int(adjusted_y + height * 0.6)),
            4,
        )

    def draw_details(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Changeling's faint fairy aura."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Adjust for twitch effect
        twitch_x = int(2 * math.sin(self.frame_count * 0.2))
        twitch_y = int(2 * math.cos(self.frame_count * 0.25))
        adjusted_x = center_x + twitch_x
        adjusted_y = center_y + twitch_y

        # Faint fairy aura (revealing true nature)
        visual_components.draw_aura_effect(
            screen,
            adjusted_x,
            adjusted_y,
            width,
            height,
            self.frame_count,
            color=(180, 150, 255),
            min_alpha=50,
            max_alpha=80,
            size_multiplier=1.2,
        )
