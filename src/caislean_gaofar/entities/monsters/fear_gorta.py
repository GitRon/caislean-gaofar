"""Fear Gorta monster - spirit of hunger."""

import pygame
import math
from caislean_gaofar.entities.monsters.base_monster import BaseMonster
from caislean_gaofar.ui import visual_components


class FearGorta(BaseMonster):
    """
    Fear Gorta - A spirit of hunger appearing as a starving beggar.

    Special traits:
    - Emaciated, skeletal appearance
    - Drains vitality from enemies
    - Moderate health and damage
    - Those who defeat him may be rewarded (future feature)
    """

    # Monster stats
    HEALTH = 55
    ATTACK_DAMAGE = 13
    SPEED = 1
    CHASE_RANGE = 6
    ATTACK_RANGE = 1
    DESCRIPTION = "Hunger spirit - drains vitality"
    MONSTER_TYPE = "fear_gorta"

    # Future: Can override execute_turn() for unique behavior
    # For example: life drain attacks, weaken player over time, hunger aura,
    # reward good fortune if player "feeds" him, etc.

    def draw_body(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Fear Gorta's emaciated spirit form."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Weak, trembling movement
        tremble = int(1 * math.sin(self.frame_count * 0.3))
        adjusted_x = center_x + tremble

        # Extremely thin, skeletal body
        body_color = (100, 90, 80)  # Sickly grayish-brown

        # Gaunt head (sunken features)
        head_radius = int(width * 0.16)
        head_pos = (int(adjusted_x), int(center_y - height * 0.25))
        pygame.draw.circle(screen, body_color, head_pos, head_radius)

        # Sunken, hollow eyes
        eye_socket_color = (30, 30, 30)
        left_eye = (int(adjusted_x - head_radius * 0.5), int(center_y - height * 0.27))
        right_eye = (int(adjusted_x + head_radius * 0.5), int(center_y - height * 0.27))
        pygame.draw.circle(screen, eye_socket_color, left_eye, int(head_radius * 0.3))
        pygame.draw.circle(screen, eye_socket_color, right_eye, int(head_radius * 0.3))
        # Faint light in eyes (spirit)
        eye_light = (100, 100, 120)
        pygame.draw.circle(screen, eye_light, left_eye, int(head_radius * 0.15))
        pygame.draw.circle(screen, eye_light, right_eye, int(head_radius * 0.15))

        # Ragged, tattered clothes
        rags_color = (80, 70, 60)
        # Torn robe/cloak
        robe_points = [
            (adjusted_x - width * 0.25, center_y - height * 0.1),
            (adjusted_x + width * 0.25, center_y - height * 0.1),
            (adjusted_x + width * 0.2, center_y + height * 0.4),
            (adjusted_x, center_y + height * 0.45),
            (adjusted_x - width * 0.2, center_y + height * 0.4),
        ]
        pygame.draw.polygon(screen, rags_color, robe_points)

        # Tattered edges (multiple tears)
        tear_color = (60, 50, 40)
        for i in range(4):
            tear_x = adjusted_x - width * 0.2 + i * width * 0.13
            tear_y = center_y + height * 0.4
            pygame.draw.line(
                screen,
                tear_color,
                (int(tear_x), int(tear_y)),
                (int(tear_x + tremble), int(tear_y + height * 0.15)),
                2,
            )

        # Skeletal thin arms reaching out (begging)
        arm_color = (90, 80, 70)
        bone_color = (110, 100, 90)
        # Left arm (reaching/begging)
        pygame.draw.line(
            screen,
            arm_color,
            (int(adjusted_x - width * 0.2), int(center_y)),
            (int(adjusted_x - width * 0.4), int(center_y + height * 0.2)),
            4,
        )
        # Skeletal hand
        pygame.draw.circle(
            screen,
            bone_color,
            (int(adjusted_x - width * 0.4), int(center_y + height * 0.2)),
            int(width * 0.08),
        )
        # Finger bones
        for i in range(3):
            finger_x = adjusted_x - width * 0.4 - width * 0.08
            finger_y = center_y + height * 0.18 + i * 4
            pygame.draw.line(
                screen,
                bone_color,
                (int(adjusted_x - width * 0.4), int(center_y + height * 0.2)),
                (int(finger_x), int(finger_y)),
                2,
            )

        # Right arm
        pygame.draw.line(
            screen,
            arm_color,
            (int(adjusted_x + width * 0.2), int(center_y)),
            (int(adjusted_x + width * 0.35), int(center_y + height * 0.15)),
            4,
        )

        # Stick legs (barely supporting)
        leg_color = (85, 75, 65)
        pygame.draw.line(
            screen,
            leg_color,
            (int(adjusted_x - width * 0.08), int(center_y + height * 0.4)),
            (int(adjusted_x - width * 0.1), int(center_y + height * 0.6)),
            4,
        )
        pygame.draw.line(
            screen,
            leg_color,
            (int(adjusted_x + width * 0.08), int(center_y + height * 0.4)),
            (int(adjusted_x + width * 0.1), int(center_y + height * 0.6)),
            4,
        )

        # Begging bowl (empty)
        bowl_color = (60, 50, 40)
        bowl_x = int(adjusted_x - width * 0.4)
        bowl_y = int(center_y + height * 0.25)
        pygame.draw.arc(
            screen, bowl_color, (bowl_x - 10, bowl_y - 5, 20, 15), 0, math.pi, 3
        )

    def draw_details(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Fear Gorta's faint ghostly aura."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Adjust x position for tremble effect
        tremble = int(1 * math.sin(self.frame_count * 0.3))
        adjusted_x = center_x + tremble

        # Faint ghostly aura (spirit nature)
        aura_alpha = int(40 + 20 * abs(math.sin(self.frame_count * 0.06)))
        aura_surface = visual_components.create_transparent_surface(
            int(width * 1.4), int(height * 1.4)
        )
        aura_color = (120, 100, 80, aura_alpha)
        pygame.draw.ellipse(
            aura_surface, aura_color, (0, 0, int(width * 1.4), int(height * 1.4))
        )
        screen.blit(aura_surface, (adjusted_x - width * 0.7, center_y - height * 0.7))
