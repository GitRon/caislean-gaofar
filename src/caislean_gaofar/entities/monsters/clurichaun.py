"""Clurichaun monster - drunk cousin of leprechaun."""

import pygame
import math
from caislean_gaofar.entities.monsters.base_monster import BaseMonster
from caislean_gaofar.ui import visual_components


class Clurichaun(BaseMonster):
    """
    Clurichaun - Related to leprechaun but fond of drinking wine.

    Special traits:
    - Low health and damage
    - Short chase range (guards wine cellars)
    - Unpredictable due to drunkenness
    - Red coat with wine bottle
    """

    # Monster stats
    HEALTH = 45
    ATTACK_DAMAGE = 9
    SPEED = 1  # Drunk, slower reactions
    CHASE_RANGE = 3  # Short chase (guards wine cellars)
    ATTACK_RANGE = 1
    DESCRIPTION = "Drunken fairy - weak but unpredictable"
    MONSTER_TYPE = "clurichaun"

    # Future: Can override execute_turn() for unique behavior
    # For example: random movement (drunk), throw wine bottles, berserker rage,
    # sleep randomly, defensive territory behavior, etc.

    def draw_body(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw the Clurichaun's drunken fairy form."""
        width, height = visual_components.apply_size_tuple(self.size)

        # Drunken swaying motion
        sway = int(5 * math.sin(self.frame_count * 0.1))
        adjusted_x = center_x + sway

        # Body (red coat instead of green - distinguishes from leprechaun)
        coat_color = (139, 0, 0)  # Dark red
        coat_rect = pygame.Rect(
            adjusted_x - width * 0.3, center_y - height * 0.1, width * 0.6, height * 0.5
        )
        pygame.draw.rect(screen, coat_color, coat_rect)

        # Head (ruddy complexion from drinking)
        head_color = (255, 200, 180)  # Reddish skin
        head_radius = int(width * 0.2)
        head_pos = (int(adjusted_x), int(center_y - height * 0.25))
        pygame.draw.circle(screen, head_color, head_pos, head_radius)

        # Red cap (slouched, disheveled)
        cap_color = (180, 0, 0)
        cap_tilt = int(3 * math.sin(self.frame_count * 0.08))
        # Brim
        cap_brim = pygame.Rect(
            adjusted_x - width * 0.25 + cap_tilt,
            center_y - height * 0.38,
            width * 0.5,
            height * 0.08,
        )
        pygame.draw.rect(screen, cap_color, cap_brim)
        # Top (tilted)
        cap_top = pygame.Rect(
            adjusted_x - width * 0.18 + cap_tilt,
            center_y - height * 0.58,
            width * 0.36,
            height * 0.2,
        )
        pygame.draw.rect(screen, cap_color, cap_top)

        # Orange/ginger beard (messy, unkempt)
        beard_color = (200, 100, 0)
        beard_points = [
            (adjusted_x - head_radius * 0.7, center_y - height * 0.22),
            (adjusted_x + head_radius * 0.7, center_y - height * 0.22),
            (adjusted_x + head_radius * 0.5, center_y - height * 0.08),
            (adjusted_x, center_y - height * 0.02),
            (adjusted_x - head_radius * 0.5, center_y - height * 0.08),
        ]
        pygame.draw.polygon(screen, beard_color, beard_points)

        # Half-closed, drowsy eyes
        eye_color = (50, 50, 50)
        left_eye = (int(adjusted_x - head_radius * 0.4), int(center_y - height * 0.28))
        right_eye = (int(adjusted_x + head_radius * 0.4), int(center_y - height * 0.28))
        # Draw as slits (half-closed)
        pygame.draw.ellipse(screen, eye_color, (left_eye[0] - 4, left_eye[1] - 2, 8, 4))
        pygame.draw.ellipse(
            screen, eye_color, (right_eye[0] - 4, right_eye[1] - 2, 8, 4)
        )

        # Rosy cheeks (from drinking)
        cheek_color = (255, 120, 120)
        pygame.draw.circle(
            screen,
            cheek_color,
            (int(adjusted_x - head_radius * 0.6), int(center_y - height * 0.22)),
            int(head_radius * 0.3),
        )
        pygame.draw.circle(
            screen,
            cheek_color,
            (int(adjusted_x + head_radius * 0.6), int(center_y - height * 0.22)),
            int(head_radius * 0.3),
        )

        # Legs
        leg_color = (40, 40, 40)
        left_leg = pygame.Rect(
            adjusted_x - width * 0.2,
            center_y + height * 0.35,
            width * 0.15,
            height * 0.25,
        )
        right_leg = pygame.Rect(
            adjusted_x + width * 0.05,
            center_y + height * 0.35,
            width * 0.15,
            height * 0.25,
        )
        pygame.draw.rect(screen, leg_color, left_leg)
        pygame.draw.rect(screen, leg_color, right_leg)

        # WINE BOTTLE in hand (key feature!)
        bottle_color = (40, 80, 40)  # Dark green glass
        bottle_x = int(adjusted_x + width * 0.4)
        bottle_y = int(center_y - height * 0.05)
        # Bottle body
        pygame.draw.rect(
            screen, bottle_color, (bottle_x, bottle_y, width * 0.12, height * 0.25)
        )
        # Bottle neck
        pygame.draw.rect(
            screen,
            bottle_color,
            (
                bottle_x + width * 0.03,
                bottle_y - height * 0.08,
                width * 0.06,
                height * 0.08,
            ),
        )
        # Cork
        cork_color = (139, 90, 60)
        pygame.draw.rect(
            screen,
            cork_color,
            (
                bottle_x + width * 0.03,
                bottle_y - height * 0.1,
                width * 0.06,
                height * 0.03,
            ),
        )

        # Wine splash/drops (sloppy drinker)
        drop_color = (100, 20, 40)
        for i in range(2):
            drop_y = int(center_y + height * 0.15 + i * 8)
            pygame.draw.circle(screen, drop_color, (bottle_x, drop_y), 2)

    def draw_details(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw any additional details for Clurichaun."""
        pass  # No additional overlay effects needed for Clurichaun
