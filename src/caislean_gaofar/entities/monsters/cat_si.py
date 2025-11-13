"""Cat Sí monster - large black fairy cat that steals souls."""

import pygame
import math
from monsters.base_monster import BaseMonster
import visual_components


class CatSi(BaseMonster):
    """
    Cat Sí (Cat Sidhe) - A large black fairy cat with white chest spot.

    Special traits:
    - Fast like a cat (speed 2)
    - High damage (16)
    - Steals souls before they pass to afterlife
    - Prowling movements with swishing tail
    """

    # Monster stats
    HEALTH = 65
    ATTACK_DAMAGE = 16
    SPEED = 2  # Fast like a cat
    CHASE_RANGE = 5
    ATTACK_RANGE = 1
    DESCRIPTION = "Fairy cat - fast and deadly"
    MONSTER_TYPE = "cat_si"

    # Future: Can override execute_turn() for unique behavior
    # For example: pounce attacks with extra range, steal player souls/experience,
    # nine lives (multiple deaths), invisibility/stealth, etc.

    def draw_body(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Cat Sí's large black fairy cat form."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Prowling animation (tail swish)
        tail_swish = int(15 * math.sin(self.frame_count * 0.08))

        # Large cat body (black)
        body_color = (10, 10, 15)  # Almost pure black

        # Main body
        body_ellipse = pygame.Rect(
            center_x - width * 0.35,
            center_y - height * 0.05,
            width * 0.7,
            height * 0.35,
        )
        pygame.draw.ellipse(screen, body_color, body_ellipse)

        # Head
        head_radius = int(width * 0.2)
        head_pos = (int(center_x - width * 0.15), int(center_y - height * 0.25))
        pygame.draw.circle(screen, body_color, head_pos, head_radius)

        # Pointed ears (alert, large)
        ear_color = (15, 15, 20)
        # Left ear
        left_ear = [
            (head_pos[0] - head_radius * 0.6, head_pos[1] - head_radius * 0.4),
            (head_pos[0] - head_radius * 0.8, head_pos[1] - head_radius * 1.2),
            (head_pos[0] - head_radius * 0.3, head_pos[1] - head_radius * 0.7),
        ]
        pygame.draw.polygon(screen, ear_color, left_ear)
        # Right ear
        right_ear = [
            (head_pos[0] + head_radius * 0.6, head_pos[1] - head_radius * 0.4),
            (head_pos[0] + head_radius * 0.8, head_pos[1] - head_radius * 1.2),
            (head_pos[0] + head_radius * 0.3, head_pos[1] - head_radius * 0.7),
        ]
        pygame.draw.polygon(screen, ear_color, right_ear)

        # Inner ear (pink)
        ear_inner = (80, 40, 60)
        pygame.draw.polygon(
            screen,
            ear_inner,
            [
                (left_ear[0][0] + 3, left_ear[0][1] + 2),
                (left_ear[1][0] + 5, left_ear[1][1] + 3),
                (left_ear[2][0] + 2, left_ear[2][1] + 1),
            ],
        )
        pygame.draw.polygon(
            screen,
            ear_inner,
            [
                (right_ear[0][0] - 3, right_ear[0][1] + 2),
                (right_ear[1][0] - 5, right_ear[1][1] + 3),
                (right_ear[2][0] - 2, right_ear[2][1] + 1),
            ],
        )

        # WHITE CHEST SPOT (distinctive feature!)
        chest_color = (240, 240, 245)
        chest_spot = pygame.Rect(
            center_x - width * 0.18, center_y, width * 0.25, height * 0.2
        )
        pygame.draw.ellipse(screen, chest_color, chest_spot)

        # Glowing supernatural eyes (green, like all fairy cats)
        eye_glow_intensity = int(150 + 100 * abs(math.sin(self.frame_count * 0.12)))
        eye_color = (0, eye_glow_intensity, 0)  # Eerie green glow
        eye_glow_color = (0, 100, 0)

        left_eye_pos = (
            head_pos[0] - head_radius * 0.4,
            head_pos[1] - head_radius * 0.2,
        )
        right_eye_pos = (
            head_pos[0] + head_radius * 0.4,
            head_pos[1] - head_radius * 0.2,
        )

        # Glow around eyes
        pygame.draw.circle(
            screen, eye_glow_color, left_eye_pos, int(head_radius * 0.25)
        )
        pygame.draw.circle(
            screen, eye_glow_color, right_eye_pos, int(head_radius * 0.25)
        )
        # Bright eyes
        pygame.draw.circle(screen, eye_color, left_eye_pos, int(head_radius * 0.18))
        pygame.draw.circle(screen, eye_color, right_eye_pos, int(head_radius * 0.18))
        # Slit pupils
        pupil_color = (0, 0, 0)
        pygame.draw.ellipse(
            screen, pupil_color, (left_eye_pos[0] - 2, left_eye_pos[1] - 6, 4, 12)
        )
        pygame.draw.ellipse(
            screen, pupil_color, (right_eye_pos[0] - 2, right_eye_pos[1] - 6, 4, 12)
        )

        # Whiskers
        whisker_color = (200, 200, 210)
        for i in range(-1, 2):
            # Left whiskers
            pygame.draw.line(
                screen,
                whisker_color,
                (int(head_pos[0] - head_radius * 0.2), int(head_pos[1] + i * 5)),
                (int(head_pos[0] - head_radius * 1.2), int(head_pos[1] + i * 8)),
                1,
            )
            # Right whiskers
            pygame.draw.line(
                screen,
                whisker_color,
                (int(head_pos[0] + head_radius * 0.2), int(head_pos[1] + i * 5)),
                (int(head_pos[0] + head_radius * 1.2), int(head_pos[1] + i * 8)),
                1,
            )

        # Four legs (cat stance)
        leg_color = (8, 8, 12)
        leg_width = int(width * 0.08)
        leg_height = int(height * 0.25)
        # Front legs
        pygame.draw.rect(
            screen,
            leg_color,
            (center_x - width * 0.25, center_y + height * 0.25, leg_width, leg_height),
        )
        pygame.draw.rect(
            screen,
            leg_color,
            (center_x - width * 0.1, center_y + height * 0.25, leg_width, leg_height),
        )
        # Back legs
        pygame.draw.rect(
            screen,
            leg_color,
            (center_x + width * 0.1, center_y + height * 0.25, leg_width, leg_height),
        )
        pygame.draw.rect(
            screen,
            leg_color,
            (center_x + width * 0.25, center_y + height * 0.25, leg_width, leg_height),
        )

        # Long swishing tail
        tail_color = (12, 12, 18)
        tail_points = [
            (center_x + width * 0.35, center_y + height * 0.05),
            (center_x + width * 0.45 + tail_swish, center_y - height * 0.1),
            (center_x + width * 0.5 + tail_swish, center_y - height * 0.25),
            (center_x + width * 0.48 + tail_swish, center_y - height * 0.05),
            (center_x + width * 0.38, center_y + height * 0.1),
        ]
        pygame.draw.polygon(screen, tail_color, tail_points)

    def draw_details(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Cat Sí's supernatural fairy aura."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Supernatural aura (fairy creature)
        visual_components.draw_aura_effect(
            screen,
            center_x,
            center_y,
            width,
            height,
            self.frame_count,
            color=(50, 150, 50),  # Green fairy aura
            min_alpha=30,
            max_alpha=50,
            size_multiplier=1.3,
        )
