"""Merrow monster - Irish sea being similar to mermaid."""

import pygame
import math
from monsters.base_monster import BaseMonster
import visual_components


class Merrow(BaseMonster):
    """
    Merrow (Muir Óg / Muirgen) - Irish sea being similar to mermaids.

    Special traits:
    - Moderate health and damage
    - Beautiful appearance with flowing movements
    - Water-themed creature
    """

    # Monster stats
    HEALTH = 75
    ATTACK_DAMAGE = 11
    SPEED = 1
    CHASE_RANGE = 5
    ATTACK_RANGE = 1
    DESCRIPTION = "Sea being - moderate threat"
    MONSTER_TYPE = "merrow"

    # Future: Can override execute_turn() for unique behavior
    # For example: charm/enchant player, create water hazards, sing to confuse,
    # call sea creatures for help, etc.

    def draw_body(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Merrow's graceful sea form."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Graceful swimming motion
        swim_wave = math.sin(self.frame_count * 0.05) * 5
        adjusted_y = center_y + swim_wave
        tail_sway = int(10 * math.sin(self.frame_count * 0.06))

        # Upper body (human, pale from ocean depths)
        skin_color = (220, 240, 235)  # Pale with slight green tint

        # Torso
        torso_rect = pygame.Rect(
            center_x - width * 0.2,
            adjusted_y - height * 0.1,
            width * 0.4,
            height * 0.35,
        )
        pygame.draw.ellipse(screen, skin_color, torso_rect)

        # Head
        head_radius = int(width * 0.18)
        head_pos = (int(center_x), int(adjusted_y - height * 0.3))
        pygame.draw.circle(screen, skin_color, head_pos, head_radius)

        # Long flowing seaweed-like hair (green)
        hair_color = (60, 120, 80)
        hair_flow = int(15 * math.sin(self.frame_count * 0.07))
        # Multiple hair strands
        for i in range(5):
            hair_x = center_x - width * 0.2 + i * width * 0.1 + hair_flow
            hair_y_start = adjusted_y - height * 0.35
            hair_y_end = adjusted_y + height * 0.2 + i * 5
            pygame.draw.line(
                screen,
                hair_color,
                (int(hair_x), int(hair_y_start)),
                (int(hair_x + hair_flow * 0.5), int(hair_y_end)),
                3,
            )

        # Beautiful eyes (large, ocean-colored)
        eye_color = (100, 180, 200)  # Sea blue
        left_eye = (int(center_x - head_radius * 0.4), int(adjusted_y - height * 0.32))
        right_eye = (int(center_x + head_radius * 0.4), int(adjusted_y - height * 0.32))
        pygame.draw.circle(screen, eye_color, left_eye, int(head_radius * 0.25))
        pygame.draw.circle(screen, eye_color, right_eye, int(head_radius * 0.25))
        # Pupils
        pupil_color = (20, 20, 60)
        pygame.draw.circle(screen, pupil_color, left_eye, int(head_radius * 0.12))
        pygame.draw.circle(screen, pupil_color, right_eye, int(head_radius * 0.12))

        # Arms
        arm_color = skin_color
        # Left arm
        pygame.draw.line(
            screen,
            arm_color,
            (int(center_x - width * 0.2), int(adjusted_y)),
            (int(center_x - width * 0.35), int(adjusted_y + height * 0.15)),
            8,
        )
        # Right arm
        pygame.draw.line(
            screen,
            arm_color,
            (int(center_x + width * 0.2), int(adjusted_y)),
            (int(center_x + width * 0.35), int(adjusted_y + height * 0.15)),
            8,
        )

        # Fish tail (green/blue scales)
        tail_color = (80, 160, 140)
        scale_color = (60, 140, 120)

        # Main tail body
        tail_points = [
            (center_x - width * 0.2, adjusted_y + height * 0.25),
            (center_x + width * 0.2, adjusted_y + height * 0.25),
            (center_x + width * 0.15 + tail_sway, adjusted_y + height * 0.5),
            (center_x - width * 0.15 + tail_sway, adjusted_y + height * 0.5),
        ]
        pygame.draw.polygon(screen, tail_color, tail_points)

        # Tail fin (split)
        fin_left = [
            (center_x - width * 0.15 + tail_sway, adjusted_y + height * 0.5),
            (center_x - width * 0.25 + tail_sway, adjusted_y + height * 0.65),
            (center_x + tail_sway, adjusted_y + height * 0.55),
        ]
        fin_right = [
            (center_x + width * 0.15 + tail_sway, adjusted_y + height * 0.5),
            (center_x + width * 0.25 + tail_sway, adjusted_y + height * 0.65),
            (center_x + tail_sway, adjusted_y + height * 0.55),
        ]
        pygame.draw.polygon(screen, tail_color, fin_left)
        pygame.draw.polygon(screen, tail_color, fin_right)

        # Scale details
        for i in range(3):
            scale_y = adjusted_y + height * 0.3 + i * height * 0.08
            pygame.draw.circle(
                screen,
                scale_color,
                (int(center_x - width * 0.1), int(scale_y)),
                int(width * 0.08),
            )
            pygame.draw.circle(
                screen,
                scale_color,
                (int(center_x + width * 0.1), int(scale_y)),
                int(width * 0.08),
            )

    def draw_details(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Merrow's underwater bubbles."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Adjust y position for swimming motion
        swim_wave = math.sin(self.frame_count * 0.05) * 5
        adjusted_y = center_y + swim_wave

        # Bubbles (underwater)
        bubble_color = (200, 230, 255, 150)
        for i in range(3):
            bubble_x = int(
                center_x + width * 0.2 + 10 * math.sin(self.frame_count * 0.05 + i)
            )
            bubble_y = int(
                adjusted_y - height * 0.2 - i * 15 - (self.frame_count * 0.5) % 30
            )
            pygame.draw.circle(screen, bubble_color, (bubble_x, bubble_y), 4)
