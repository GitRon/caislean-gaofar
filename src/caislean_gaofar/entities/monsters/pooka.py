"""Pooka monster - shape-shifting creature."""

import pygame
import math
from caislean_gaofar.entities.monsters.base_monster import BaseMonster
from caislean_gaofar.ui import visual_components


class Pooka(BaseMonster):
    """
    Pooka (Púca) - A shape-shifting creature of fortune and mischief.

    Special traits:
    - High health (100 HP)
    - Relentless pursuit (chase range 7)
    - Moderate damage
    - Dark horse form with pulsing shadow aura
    """

    # Monster stats
    HEALTH = 100
    ATTACK_DAMAGE = 15
    SPEED = 1
    CHASE_RANGE = 7  # Pursues relentlessly
    ATTACK_RANGE = 1
    DESCRIPTION = "Shape-shifter - high health, relentless pursuit"
    MONSTER_TYPE = "pooka"

    # Future: Can override execute_turn() for unique behavior
    # For example: shape-shift to different forms with different abilities,
    # random teleportation, curse effects, etc.

    def draw_body(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Pooka's dark horse form."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Apply supernatural breathing/pulsing effect
        effective_width = visual_components.apply_pulse_effect(
            width, self.frame_count, intensity=0.1, speed=0.06
        )
        effective_height = visual_components.apply_pulse_effect(
            height, self.frame_count, intensity=0.1, speed=0.06
        )

        # Main body (black, horse-like)
        body_color = (15, 15, 15)  # Nearly black
        body_rect = pygame.Rect(
            center_x - effective_width * 0.35,
            center_y - effective_height * 0.1,
            effective_width * 0.7,
            effective_height * 0.4,
        )
        pygame.draw.ellipse(screen, body_color, body_rect)

        # Head/neck (horse-like profile)
        head_points = [
            (center_x - effective_width * 0.3, center_y - effective_height * 0.05),
            (center_x - effective_width * 0.45, center_y - effective_height * 0.25),
            (center_x - effective_width * 0.5, center_y - effective_height * 0.3),
            (center_x - effective_width * 0.55, center_y - effective_height * 0.25),
            (center_x - effective_width * 0.5, center_y - effective_height * 0.15),
        ]
        pygame.draw.polygon(screen, body_color, head_points)

        # Mane (wild, shadowy)
        mane_color = (25, 25, 30)
        mane_offset = int(3 * math.sin(self.frame_count * 0.1))
        for i in range(3):
            mane_x = center_x - effective_width * 0.4 + i * effective_width * 0.05
            mane_y = (
                center_y
                - effective_height * 0.3
                - i * effective_height * 0.05
                + mane_offset
            )
            mane_width = int(effective_width * 0.08)
            mane_height = int(effective_height * 0.25)
            pygame.draw.ellipse(
                screen, mane_color, (mane_x, mane_y, mane_width, mane_height)
            )

        # Glowing supernatural eyes (eerie!)
        eye_glow_color = (150, 0, 0)  # Red glow
        eye_intensity = int(150 + 105 * abs(math.sin(self.frame_count * 0.15)))
        eye_color = (eye_intensity, 0, 0)

        eye_pos = (
            int(center_x - effective_width * 0.48),
            int(center_y - effective_height * 0.25),
        )
        # Outer glow
        pygame.draw.circle(screen, eye_glow_color, eye_pos, int(effective_width * 0.08))
        # Bright center
        pygame.draw.circle(screen, eye_color, eye_pos, int(effective_width * 0.05))

        # Legs (four horse legs)
        leg_color = (10, 10, 10)
        leg_width = int(effective_width * 0.1)
        leg_height = int(effective_height * 0.35)

        # Front legs
        front_left = pygame.Rect(
            center_x - effective_width * 0.25,
            center_y + effective_height * 0.25,
            leg_width,
            leg_height,
        )
        front_right = pygame.Rect(
            center_x - effective_width * 0.1,
            center_y + effective_height * 0.25,
            leg_width,
            leg_height,
        )
        # Back legs
        back_left = pygame.Rect(
            center_x + effective_width * 0.05,
            center_y + effective_height * 0.25,
            leg_width,
            leg_height,
        )
        back_right = pygame.Rect(
            center_x + effective_width * 0.2,
            center_y + effective_height * 0.25,
            leg_width,
            leg_height,
        )

        pygame.draw.rect(screen, leg_color, front_left)
        pygame.draw.rect(screen, leg_color, front_right)
        pygame.draw.rect(screen, leg_color, back_left)
        pygame.draw.rect(screen, leg_color, back_right)

        # Tail (wispy, shadowy)
        tail_color = (20, 20, 25)
        tail_sway = int(10 * math.sin(self.frame_count * 0.07))
        tail_points = [
            (center_x + effective_width * 0.35, center_y),
            (
                center_x + effective_width * 0.5 + tail_sway,
                center_y - effective_height * 0.2,
            ),
            (
                center_x + effective_width * 0.55 + tail_sway,
                center_y + effective_height * 0.1,
            ),
            (center_x + effective_width * 0.4, center_y + effective_height * 0.15),
        ]
        pygame.draw.polygon(screen, tail_color, tail_points)

        # Hooves (darker accents)
        hoof_color = (5, 5, 5)
        hoof_height = int(effective_height * 0.08)
        pygame.draw.rect(
            screen,
            hoof_color,
            (front_left.x, front_left.bottom - hoof_height, leg_width, hoof_height),
        )
        pygame.draw.rect(
            screen,
            hoof_color,
            (front_right.x, front_right.bottom - hoof_height, leg_width, hoof_height),
        )
        pygame.draw.rect(
            screen,
            hoof_color,
            (back_left.x, back_left.bottom - hoof_height, leg_width, hoof_height),
        )
        pygame.draw.rect(
            screen,
            hoof_color,
            (back_right.x, back_right.bottom - hoof_height, leg_width, hoof_height),
        )

    def draw_details(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Pooka's shadow aura."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Apply same pulse for alignment
        effective_width = visual_components.apply_pulse_effect(
            width, self.frame_count, intensity=0.1, speed=0.06
        )
        effective_height = visual_components.apply_pulse_effect(
            height, self.frame_count, intensity=0.1, speed=0.06
        )

        # Shadow aura (dark supernatural energy)
        aura_surface = visual_components.create_transparent_surface(
            int(effective_width * 1.3), int(effective_height * 1.3)
        )
        aura_color = (20, 0, 40, 60)  # Very dark purple, semi-transparent
        aura_radius = int(effective_width * 0.6)
        pygame.draw.circle(
            aura_surface,
            aura_color,
            (int(effective_width * 0.65), int(effective_height * 0.65)),
            aura_radius,
        )
        screen.blit(
            aura_surface,
            (center_x - effective_width * 0.65, center_y - effective_height * 0.65),
        )
