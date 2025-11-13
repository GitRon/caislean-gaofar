"""Leprechaun monster - fast and tricky fairy."""

import pygame
import math
from caislean_gaofar.entities.monsters.base_monster import BaseMonster
from caislean_gaofar.ui import visual_components


class Leprechaun(BaseMonster):
    """
    Leprechaun - A small, mischievous fairy known for tricks.

    Special traits:
    - Very fast (speed 2)
    - Low health and damage
    - Short chase range (guards his gold)
    - Green appearance with bouncing animation
    """

    # Monster stats
    HEALTH = 40
    ATTACK_DAMAGE = 8
    SPEED = 2  # Very fast and tricky
    CHASE_RANGE = 4
    ATTACK_RANGE = 1
    DESCRIPTION = "Mischievous fairy - weak but very fast"
    MONSTER_TYPE = "leprechaun"

    # Future: Can override execute_turn() for unique behavior
    # For example: teleport away when hit, leave gold traps, confusion effects, etc.

    def draw_body(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Leprechaun's small green form."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Small bounce animation (mischievous hopping)
        bounce = abs(math.sin(self.frame_count * 0.08)) * 4
        center_y -= bounce

        # Body (green coat)
        coat_color = (34, 139, 34)  # Forest green
        coat_rect = pygame.Rect(
            center_x - width * 0.3, center_y - height * 0.1, width * 0.6, height * 0.5
        )
        pygame.draw.rect(screen, coat_color, coat_rect)

        # Head (peachy skin tone)
        head_color = (255, 218, 185)
        head_radius = int(width * 0.2)
        head_pos = (int(center_x), int(center_y - height * 0.25))
        pygame.draw.circle(screen, head_color, head_pos, head_radius)

        # Famous green hat
        hat_color = (0, 100, 0)  # Dark green
        hat_brim = pygame.Rect(
            center_x - width * 0.25, center_y - height * 0.4, width * 0.5, height * 0.08
        )
        pygame.draw.rect(screen, hat_color, hat_brim)
        # Hat top (tall)
        hat_top = pygame.Rect(
            center_x - width * 0.18,
            center_y - height * 0.65,
            width * 0.36,
            height * 0.25,
        )
        pygame.draw.rect(screen, hat_color, hat_top)
        # Gold buckle on hat
        buckle_color = (255, 215, 0)  # Gold
        buckle = pygame.Rect(
            center_x - width * 0.08,
            center_y - height * 0.48,
            width * 0.16,
            height * 0.08,
        )
        pygame.draw.rect(screen, buckle_color, buckle)

        # Red beard (distinctive feature)
        beard_color = (180, 60, 0)  # Reddish-orange
        beard_points = [
            (center_x - head_radius * 0.6, center_y - height * 0.22),
            (center_x + head_radius * 0.6, center_y - height * 0.22),
            (center_x + head_radius * 0.4, center_y - height * 0.1),
            (center_x, center_y - height * 0.05),
            (center_x - head_radius * 0.4, center_y - height * 0.1),
        ]
        pygame.draw.polygon(screen, beard_color, beard_points)

        # Eyes (mischievous expression)
        eye_color = (50, 50, 50)
        left_eye = (int(center_x - head_radius * 0.4), int(center_y - height * 0.28))
        right_eye = (int(center_x + head_radius * 0.4), int(center_y - height * 0.28))
        pygame.draw.circle(screen, eye_color, left_eye, int(head_radius * 0.2))
        pygame.draw.circle(screen, eye_color, right_eye, int(head_radius * 0.2))

        # Gleam in eyes (mischief!)
        gleam_color = (255, 255, 255)
        pygame.draw.circle(screen, gleam_color, left_eye, int(head_radius * 0.1))
        pygame.draw.circle(screen, gleam_color, right_eye, int(head_radius * 0.1))

        # Legs (black pants/boots)
        leg_color = (40, 40, 40)
        left_leg = pygame.Rect(
            center_x - width * 0.2,
            center_y + height * 0.35,
            width * 0.15,
            height * 0.25,
        )
        right_leg = pygame.Rect(
            center_x + width * 0.05,
            center_y + height * 0.35,
            width * 0.15,
            height * 0.25,
        )
        pygame.draw.rect(screen, leg_color, left_leg)
        pygame.draw.rect(screen, leg_color, right_leg)

        # Gold coin (treasure!) - floats beside him
        coin_x = int(center_x + width * 0.5 + 5 * math.sin(self.frame_count * 0.1))
        coin_y = int(center_y - height * 0.3 + 3 * math.cos(self.frame_count * 0.1))
        pygame.draw.circle(screen, buckle_color, (coin_x, coin_y), int(width * 0.1))
        coin_inner = (218, 165, 32)  # Darker gold for detail
        pygame.draw.circle(screen, coin_inner, (coin_x, coin_y), int(width * 0.06))
