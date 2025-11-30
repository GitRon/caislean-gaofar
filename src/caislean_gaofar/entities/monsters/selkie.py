"""Selkie monster - seal that transforms to human."""

import pygame
import math
from caislean_gaofar.entities.monsters.base_monster import BaseMonster
from caislean_gaofar.ui import visual_components


class Selkie(BaseMonster):
    """
    Selkie - A seal that can shed its skin to live as a human.

    Special traits:
    - Balanced stats
    - Water-themed abilities
    - Seal-human hybrid appearance with swimming motion
    """

    # Monster stats
    HEALTH = 70
    ATTACK_DAMAGE = 10
    SPEED = 1
    CHASE_RANGE = 5
    ATTACK_RANGE = 1
    DESCRIPTION = "Seal-human hybrid - balanced stats"
    MONSTER_TYPE = "selkie"

    # Future: Can override execute_turn() for unique behavior
    # For example: transform between seal/human forms, water pools that slow player,
    # healing when near water, etc.

    def draw_body(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Selkie's seal-human hybrid form."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Gentle swimming/bobbing motion
        center_y = int(
            visual_components.apply_floating_effect(
                center_y, self.frame_count, amplitude=4, speed=0.04
            )
        )

        # Sleek seal-like body (gray-blue)
        body_color = (100, 120, 140)
        # Main body (rounded seal shape)
        body_ellipse = pygame.Rect(
            center_x - width * 0.35, center_y - height * 0.15, width * 0.7, height * 0.5
        )
        pygame.draw.ellipse(screen, body_color, body_ellipse)

        # Human-like head (transformation aspect)
        head_color = (210, 180, 160)  # Skin tone
        head_radius = int(width * 0.18)
        head_pos = (int(center_x), int(center_y - height * 0.25))
        pygame.draw.circle(screen, head_color, head_pos, head_radius)

        # Long flowing hair (dark, wet-looking)
        hair_color = (40, 60, 80)
        hair_sway = int(5 * math.sin(self.frame_count * 0.06))
        pygame.draw.ellipse(
            screen,
            hair_color,
            (
                center_x - width * 0.22 + hair_sway,
                center_y - height * 0.35,
                width * 0.44,
                height * 0.3,
            ),
        )

        # Eyes (large, dark, seal-like)
        eye_color = (20, 20, 20)
        left_eye = (int(center_x - head_radius * 0.4), int(center_y - height * 0.27))
        right_eye = (int(center_x + head_radius * 0.4), int(center_y - height * 0.27))
        pygame.draw.ellipse(
            screen, eye_color, (left_eye[0] - 4, left_eye[1] - 6, 8, 12)
        )
        pygame.draw.ellipse(
            screen, eye_color, (right_eye[0] - 4, right_eye[1] - 6, 8, 12)
        )
        # Gleam
        gleam_color = (200, 220, 255)
        pygame.draw.circle(screen, gleam_color, left_eye, 2)
        pygame.draw.circle(screen, gleam_color, right_eye, 2)

        # Seal flippers (transforming to arms)
        flipper_color = (80, 100, 120)
        # Left flipper
        left_flipper = [
            (center_x - width * 0.35, center_y),
            (center_x - width * 0.5, center_y + height * 0.1),
            (center_x - width * 0.45, center_y + height * 0.25),
            (center_x - width * 0.3, center_y + height * 0.15),
        ]
        pygame.draw.polygon(screen, flipper_color, left_flipper)
        # Right flipper
        right_flipper = [
            (center_x + width * 0.35, center_y),
            (center_x + width * 0.5, center_y + height * 0.1),
            (center_x + width * 0.45, center_y + height * 0.25),
            (center_x + width * 0.3, center_y + height * 0.15),
        ]
        pygame.draw.polygon(screen, flipper_color, right_flipper)

        # Seal tail (lower body)
        tail_color = (90, 110, 130)
        tail_points = [
            (center_x - width * 0.15, center_y + height * 0.3),
            (center_x + width * 0.15, center_y + height * 0.3),
            (center_x + width * 0.1, center_y + height * 0.5),
            (center_x, center_y + height * 0.55),
            (center_x - width * 0.1, center_y + height * 0.5),
        ]
        pygame.draw.polygon(screen, tail_color, tail_points)

    def draw_details(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Selkie's magical water droplets."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Gentle swimming/bobbing motion (match body)
        center_y = int(
            visual_components.apply_floating_effect(
                center_y, self.frame_count, amplitude=4, speed=0.04
            )
        )

        # Water droplets around (magical transformation)
        droplet_color = (150, 200, 255, 150)
        for i in range(3):
            drop_x = int(center_x + width * 0.3 * math.sin(self.frame_count * 0.1 + i))
            drop_y = int(
                center_y - height * 0.4 + i * 10 + 5 * math.cos(self.frame_count * 0.1)
            )
            pygame.draw.circle(screen, droplet_color, (drop_x, drop_y), 3)
