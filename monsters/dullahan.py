"""Dullahan monster - headless rider, omen of death."""

import pygame
import math
from monsters.base_monster import BaseMonster
import visual_components


class Dullahan(BaseMonster):
    """
    Dullahan - A headless rider who carries his own head.

    Special traits:
    - Highest health (120 HP)
    - Highest damage (20)
    - Wide chase range (omen of death)
    - BOSS-level difficulty
    """

    # Monster stats
    HEALTH = 120
    ATTACK_DAMAGE = 20
    SPEED = 1
    CHASE_RANGE = 8  # Omen of death, wide chase range
    ATTACK_RANGE = 1
    DESCRIPTION = "Headless rider - very powerful, deadly"
    MONSTER_TYPE = "dullahan"

    # Future: Can override execute_turn() for unique behavior
    # For example: death mark on player, summon lesser undead, charge attacks,
    # instant kill below certain HP threshold, etc.

    def draw_body(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Dullahan's headless body and horse."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Dark horse (simplified, since focus is on rider)
        horse_color = (30, 30, 30)
        horse_body = pygame.Rect(
            center_x - width * 0.3, center_y + height * 0.1, width * 0.6, height * 0.3
        )
        pygame.draw.ellipse(screen, horse_color, horse_body)

        # Rider's headless body (dark armor)
        armor_color = (40, 40, 50)
        # Torso
        torso = pygame.Rect(
            center_x - width * 0.2, center_y - height * 0.3, width * 0.4, height * 0.45
        )
        pygame.draw.rect(screen, armor_color, torso)

        # Shoulders (broad, menacing)
        shoulder_color = (50, 50, 60)
        pygame.draw.rect(
            screen,
            shoulder_color,
            (
                center_x - width * 0.3,
                center_y - height * 0.3,
                width * 0.6,
                height * 0.1,
            ),
        )

        # NO HEAD on shoulders (that's the point!)
        # Neck stump (dark, ominous)
        neck_color = (20, 10, 10)
        pygame.draw.ellipse(
            screen,
            neck_color,
            (
                center_x - width * 0.12,
                center_y - height * 0.35,
                width * 0.24,
                height * 0.1,
            ),
        )

        # Left arm holding the severed head
        arm_color = (45, 45, 55)
        # Upper arm
        pygame.draw.rect(
            screen,
            arm_color,
            (
                center_x - width * 0.45,
                center_y - height * 0.25,
                width * 0.15,
                height * 0.3,
            ),
        )
        # Forearm
        pygame.draw.rect(
            screen,
            arm_color,
            (center_x - width * 0.5, center_y, width * 0.12, height * 0.25),
        )

        # THE SEVERED HEAD being held up (glowing, supernatural)
        head_color = (180, 160, 140)  # Pale, dead skin
        head_radius = int(width * 0.15)
        head_pos = (int(center_x - width * 0.45), int(center_y + height * 0.1))
        pygame.draw.circle(screen, head_color, head_pos, head_radius)

        # Glowing eyes in the severed head
        eye_glow = (100, 255, 100)  # Matching green glow
        left_eye = (head_pos[0] - head_radius // 3, head_pos[1] - head_radius // 4)
        right_eye = (head_pos[0] + head_radius // 3, head_pos[1] - head_radius // 4)
        pygame.draw.circle(screen, eye_glow, left_eye, int(head_radius * 0.25))
        pygame.draw.circle(screen, eye_glow, right_eye, int(head_radius * 0.25))

        # Grim mouth
        mouth_color = (80, 80, 80)
        pygame.draw.arc(
            screen,
            mouth_color,
            (
                head_pos[0] - head_radius // 2,
                head_pos[1],
                head_radius,
                head_radius // 2,
            ),
            0,
            math.pi,
            3,
        )

        # Right arm holding reins/whip
        pygame.draw.rect(
            screen,
            arm_color,
            (
                center_x + width * 0.2,
                center_y - height * 0.2,
                width * 0.15,
                height * 0.35,
            ),
        )

        # Whip/reins
        whip_color = (100, 80, 60)
        whip_sway = int(8 * math.sin(self.frame_count * 0.12))
        pygame.draw.line(
            screen,
            whip_color,
            (int(center_x + width * 0.27), int(center_y + height * 0.15)),
            (int(center_x + width * 0.4 + whip_sway), int(center_y + height * 0.4)),
            3,
        )

    def draw_details(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Dullahan's glowing head aura."""
        width, height = visual_components.apply_size_tuple(self.size)

        # THE SEVERED HEAD being held up (glowing, supernatural)
        head_glow_alpha = int(100 + 50 * abs(math.sin(self.frame_count * 0.1)))
        glow_surface = visual_components.create_transparent_surface(
            int(width * 0.4), int(height * 0.4)
        )
        glow_color = (100, 255, 100, head_glow_alpha)  # Eerie green glow
        pygame.draw.circle(
            glow_surface,
            glow_color,
            (int(width * 0.2), int(height * 0.2)),
            int(width * 0.2),
        )
        screen.blit(glow_surface, (center_x - width * 0.65, center_y - height * 0.1))
