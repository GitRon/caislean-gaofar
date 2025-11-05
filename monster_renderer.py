"""
Monster Rendering Module
Procedural drawing functions for different monster types
"""

import pygame
import math
from config import *  # noqa: F403


def draw_banshee(surface, x, y, size, frame_count=0):
    """
    Draw a Banshee (Bean Sí) - ghostly wailing spirit

    Args:
        surface: pygame surface to draw on
        x, y: center position
        size: base size (width, height tuple or single value)
        frame_count: for animation effects
    """
    if isinstance(size, tuple):
        width, height = size
    else:
        width = height = size

    # Animation: gentle floating effect
    float_offset = math.sin(frame_count * 0.05) * 3
    y += float_offset

    # Semi-transparent surface for ghostly effect
    ghost_surface = pygame.Surface((width, height), pygame.SRCALPHA)

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
        ghost_surface, head_color, (int(width * 0.5), int(height * 0.15)), head_radius
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
    pygame.draw.circle(ghost_surface, mouth_color, mouth_center, int(head_radius * 0.4))

    # Dark hollow eyes
    eye_color = (30, 30, 50, 200)
    left_eye = (int(width * 0.45), int(height * 0.13))
    right_eye = (int(width * 0.55), int(height * 0.13))
    eye_radius = int(head_radius * 0.25)
    pygame.draw.circle(ghost_surface, eye_color, left_eye, eye_radius)
    pygame.draw.circle(ghost_surface, eye_color, right_eye, eye_radius)

    # Wispy trailing effect (animated)
    wisp_alpha = int(100 + 50 * math.sin(frame_count * 0.1))
    wisp_color = (200, 220, 240, wisp_alpha)
    wisp_y_offset = int(10 * math.sin(frame_count * 0.08))
    pygame.draw.circle(
        ghost_surface,
        wisp_color,
        (int(width * 0.5), int(height * 0.95) + wisp_y_offset),
        int(width * 0.15),
    )

    # Blit to main surface
    surface.blit(ghost_surface, (x - width // 2, y - height // 2))


def draw_leprechaun(surface, x, y, size, frame_count=0):
    """
    Draw a Leprechaun - small, mischievous fairy in green

    Args:
        surface: pygame surface to draw on
        x, y: center position
        size: base size (width, height tuple or single value)
        frame_count: for animation effects
    """
    if isinstance(size, tuple):
        width, height = size
    else:
        width = height = size

    # Small bounce animation (mischievous hopping)
    bounce = abs(math.sin(frame_count * 0.08)) * 4
    y -= bounce

    # Body (green coat)
    coat_color = (34, 139, 34)  # Forest green
    coat_rect = pygame.Rect(
        x - width * 0.3, y - height * 0.1, width * 0.6, height * 0.5
    )
    pygame.draw.rect(surface, coat_color, coat_rect)

    # Head (peachy skin tone)
    head_color = (255, 218, 185)
    head_radius = int(width * 0.2)
    head_pos = (int(x), int(y - height * 0.25))
    pygame.draw.circle(surface, head_color, head_pos, head_radius)

    # Famous green hat
    hat_color = (0, 100, 0)  # Dark green
    hat_brim = pygame.Rect(
        x - width * 0.25, y - height * 0.4, width * 0.5, height * 0.08
    )
    pygame.draw.rect(surface, hat_color, hat_brim)
    # Hat top (tall)
    hat_top = pygame.Rect(
        x - width * 0.18, y - height * 0.65, width * 0.36, height * 0.25
    )
    pygame.draw.rect(surface, hat_color, hat_top)
    # Gold buckle on hat
    buckle_color = (255, 215, 0)  # Gold
    buckle = pygame.Rect(
        x - width * 0.08, y - height * 0.48, width * 0.16, height * 0.08
    )
    pygame.draw.rect(surface, buckle_color, buckle)

    # Red beard (distinctive feature)
    beard_color = (180, 60, 0)  # Reddish-orange
    beard_points = [
        (x - head_radius * 0.6, y - height * 0.22),
        (x + head_radius * 0.6, y - height * 0.22),
        (x + head_radius * 0.4, y - height * 0.1),
        (x, y - height * 0.05),
        (x - head_radius * 0.4, y - height * 0.1),
    ]
    pygame.draw.polygon(surface, beard_color, beard_points)

    # Eyes (mischievous expression)
    eye_color = (50, 50, 50)
    left_eye = (int(x - head_radius * 0.4), int(y - height * 0.28))
    right_eye = (int(x + head_radius * 0.4), int(y - height * 0.28))
    pygame.draw.circle(surface, eye_color, left_eye, int(head_radius * 0.2))
    pygame.draw.circle(surface, eye_color, right_eye, int(head_radius * 0.2))

    # Gleam in eyes (mischief!)
    gleam_color = (255, 255, 255)
    pygame.draw.circle(surface, gleam_color, left_eye, int(head_radius * 0.1))
    pygame.draw.circle(surface, gleam_color, right_eye, int(head_radius * 0.1))

    # Legs (black pants/boots)
    leg_color = (40, 40, 40)
    left_leg = pygame.Rect(
        x - width * 0.2, y + height * 0.35, width * 0.15, height * 0.25
    )
    right_leg = pygame.Rect(
        x + width * 0.05, y + height * 0.35, width * 0.15, height * 0.25
    )
    pygame.draw.rect(surface, leg_color, left_leg)
    pygame.draw.rect(surface, leg_color, right_leg)

    # Gold coin (treasure!) - floats beside him
    coin_x = int(x + width * 0.5 + 5 * math.sin(frame_count * 0.1))
    coin_y = int(y - height * 0.3 + 3 * math.cos(frame_count * 0.1))
    pygame.draw.circle(surface, buckle_color, (coin_x, coin_y), int(width * 0.1))
    coin_inner = (218, 165, 32)  # Darker gold for detail
    pygame.draw.circle(surface, coin_inner, (coin_x, coin_y), int(width * 0.06))


def draw_pooka(surface, x, y, size, frame_count=0):
    """
    Draw a Pooka (Púca) - shape-shifting creature as a shadowy black horse

    Args:
        surface: pygame surface to draw on
        x, y: center position
        size: base size (width, height tuple or single value)
        frame_count: for animation effects
    """
    if isinstance(size, tuple):
        width, height = size
    else:
        width = height = size

    # Supernatural breathing/pulsing effect
    pulse = math.sin(frame_count * 0.06) * 0.1 + 1.0
    effective_width = width * pulse
    effective_height = height * pulse

    # Shadow aura (dark supernatural energy)
    aura_surface = pygame.Surface(
        (int(effective_width * 1.3), int(effective_height * 1.3)), pygame.SRCALPHA
    )
    aura_color = (20, 0, 40, 60)  # Very dark purple, semi-transparent
    aura_radius = int(effective_width * 0.6)
    pygame.draw.circle(
        aura_surface,
        aura_color,
        (int(effective_width * 0.65), int(effective_height * 0.65)),
        aura_radius,
    )
    surface.blit(
        aura_surface, (x - effective_width * 0.65, y - effective_height * 0.65)
    )

    # Main body (black, horse-like)
    body_color = (15, 15, 15)  # Nearly black
    body_rect = pygame.Rect(
        x - effective_width * 0.35,
        y - effective_height * 0.1,
        effective_width * 0.7,
        effective_height * 0.4,
    )
    pygame.draw.ellipse(surface, body_color, body_rect)

    # Head/neck (horse-like profile)
    head_points = [
        (x - effective_width * 0.3, y - effective_height * 0.05),  # Neck base
        (x - effective_width * 0.45, y - effective_height * 0.25),  # Back of head
        (x - effective_width * 0.5, y - effective_height * 0.3),  # Top of head
        (x - effective_width * 0.55, y - effective_height * 0.25),  # Snout
        (x - effective_width * 0.5, y - effective_height * 0.15),  # Mouth area
    ]
    pygame.draw.polygon(surface, body_color, head_points)

    # Mane (wild, shadowy)
    mane_color = (25, 25, 30)
    mane_offset = int(3 * math.sin(frame_count * 0.1))
    for i in range(3):
        mane_x = x - effective_width * 0.4 + i * effective_width * 0.05
        mane_y = y - effective_height * 0.3 - i * effective_height * 0.05 + mane_offset
        mane_width = int(effective_width * 0.08)
        mane_height = int(effective_height * 0.25)
        pygame.draw.ellipse(
            surface, mane_color, (mane_x, mane_y, mane_width, mane_height)
        )

    # Glowing supernatural eyes (eerie!)
    eye_glow_color = (150, 0, 0)  # Red glow
    eye_intensity = int(150 + 105 * abs(math.sin(frame_count * 0.15)))
    eye_color = (eye_intensity, 0, 0)

    eye_pos = (int(x - effective_width * 0.48), int(y - effective_height * 0.25))
    # Outer glow
    pygame.draw.circle(surface, eye_glow_color, eye_pos, int(effective_width * 0.08))
    # Bright center
    pygame.draw.circle(surface, eye_color, eye_pos, int(effective_width * 0.05))

    # Legs (four horse legs)
    leg_color = (10, 10, 10)
    leg_width = int(effective_width * 0.1)
    leg_height = int(effective_height * 0.35)

    # Front legs
    front_left = pygame.Rect(
        x - effective_width * 0.25, y + effective_height * 0.25, leg_width, leg_height
    )
    front_right = pygame.Rect(
        x - effective_width * 0.1, y + effective_height * 0.25, leg_width, leg_height
    )
    # Back legs
    back_left = pygame.Rect(
        x + effective_width * 0.05, y + effective_height * 0.25, leg_width, leg_height
    )
    back_right = pygame.Rect(
        x + effective_width * 0.2, y + effective_height * 0.25, leg_width, leg_height
    )

    pygame.draw.rect(surface, leg_color, front_left)
    pygame.draw.rect(surface, leg_color, front_right)
    pygame.draw.rect(surface, leg_color, back_left)
    pygame.draw.rect(surface, leg_color, back_right)

    # Tail (wispy, shadowy)
    tail_color = (20, 20, 25)
    tail_sway = int(10 * math.sin(frame_count * 0.07))
    tail_points = [
        (x + effective_width * 0.35, y),
        (x + effective_width * 0.5 + tail_sway, y - effective_height * 0.2),
        (x + effective_width * 0.55 + tail_sway, y + effective_height * 0.1),
        (x + effective_width * 0.4, y + effective_height * 0.15),
    ]
    pygame.draw.polygon(surface, tail_color, tail_points)

    # Hooves (darker accents)
    hoof_color = (5, 5, 5)
    hoof_height = int(effective_height * 0.08)
    pygame.draw.rect(
        surface,
        hoof_color,
        (front_left.x, front_left.bottom - hoof_height, leg_width, hoof_height),
    )
    pygame.draw.rect(
        surface,
        hoof_color,
        (front_right.x, front_right.bottom - hoof_height, leg_width, hoof_height),
    )
    pygame.draw.rect(
        surface,
        hoof_color,
        (back_left.x, back_left.bottom - hoof_height, leg_width, hoof_height),
    )
    pygame.draw.rect(
        surface,
        hoof_color,
        (back_right.x, back_right.bottom - hoof_height, leg_width, hoof_height),
    )


def draw_selkie(surface, x, y, size, frame_count=0):
    """
    Draw a Selkie - seal that can transform to human

    Shows a hybrid form with seal-like features
    """
    if isinstance(size, tuple):
        width, height = size
    else:
        width = height = size

    # Gentle swimming/bobbing motion
    float_offset = math.sin(frame_count * 0.04) * 4
    y += float_offset

    # Sleek seal-like body (gray-blue)
    body_color = (100, 120, 140)
    # Main body (rounded seal shape)
    body_ellipse = pygame.Rect(
        x - width * 0.35, y - height * 0.15, width * 0.7, height * 0.5
    )
    pygame.draw.ellipse(surface, body_color, body_ellipse)

    # Human-like head (transformation aspect)
    head_color = (210, 180, 160)  # Skin tone
    head_radius = int(width * 0.18)
    head_pos = (int(x), int(y - height * 0.25))
    pygame.draw.circle(surface, head_color, head_pos, head_radius)

    # Long flowing hair (dark, wet-looking)
    hair_color = (40, 60, 80)
    hair_sway = int(5 * math.sin(frame_count * 0.06))
    pygame.draw.ellipse(
        surface,
        hair_color,
        (x - width * 0.22 + hair_sway, y - height * 0.35, width * 0.44, height * 0.3),
    )

    # Eyes (large, dark, seal-like)
    eye_color = (20, 20, 20)
    left_eye = (int(x - head_radius * 0.4), int(y - height * 0.27))
    right_eye = (int(x + head_radius * 0.4), int(y - height * 0.27))
    pygame.draw.ellipse(surface, eye_color, (left_eye[0] - 4, left_eye[1] - 6, 8, 12))
    pygame.draw.ellipse(surface, eye_color, (right_eye[0] - 4, right_eye[1] - 6, 8, 12))
    # Gleam
    gleam_color = (200, 220, 255)
    pygame.draw.circle(surface, gleam_color, left_eye, 2)
    pygame.draw.circle(surface, gleam_color, right_eye, 2)

    # Seal flippers (transforming to arms)
    flipper_color = (80, 100, 120)
    # Left flipper
    left_flipper = [
        (x - width * 0.35, y),
        (x - width * 0.5, y + height * 0.1),
        (x - width * 0.45, y + height * 0.25),
        (x - width * 0.3, y + height * 0.15),
    ]
    pygame.draw.polygon(surface, flipper_color, left_flipper)
    # Right flipper
    right_flipper = [
        (x + width * 0.35, y),
        (x + width * 0.5, y + height * 0.1),
        (x + width * 0.45, y + height * 0.25),
        (x + width * 0.3, y + height * 0.15),
    ]
    pygame.draw.polygon(surface, flipper_color, right_flipper)

    # Seal tail (lower body)
    tail_color = (90, 110, 130)
    tail_points = [
        (x - width * 0.15, y + height * 0.3),
        (x + width * 0.15, y + height * 0.3),
        (x + width * 0.1, y + height * 0.5),
        (x, y + height * 0.55),
        (x - width * 0.1, y + height * 0.5),
    ]
    pygame.draw.polygon(surface, tail_color, tail_points)

    # Water droplets around (magical transformation)
    droplet_color = (150, 200, 255, 150)
    for i in range(3):
        drop_x = int(x + width * 0.3 * math.sin(frame_count * 0.1 + i))
        drop_y = int(y - height * 0.4 + i * 10 + 5 * math.cos(frame_count * 0.1))
        pygame.draw.circle(surface, droplet_color, (drop_x, drop_y), 3)


def draw_dullahan(surface, x, y, size, frame_count=0):
    """
    Draw a Dullahan - headless rider carrying his own head
    """
    if isinstance(size, tuple):
        width, height = size
    else:
        width = height = size

    # Dark horse (simplified, since focus is on rider)
    horse_color = (30, 30, 30)
    horse_body = pygame.Rect(
        x - width * 0.3, y + height * 0.1, width * 0.6, height * 0.3
    )
    pygame.draw.ellipse(surface, horse_color, horse_body)

    # Rider's headless body (dark armor)
    armor_color = (40, 40, 50)
    # Torso
    torso = pygame.Rect(x - width * 0.2, y - height * 0.3, width * 0.4, height * 0.45)
    pygame.draw.rect(surface, armor_color, torso)

    # Shoulders (broad, menacing)
    shoulder_color = (50, 50, 60)
    pygame.draw.rect(
        surface,
        shoulder_color,
        (x - width * 0.3, y - height * 0.3, width * 0.6, height * 0.1),
    )

    # NO HEAD on shoulders (that's the point!)
    # Neck stump (dark, ominous)
    neck_color = (20, 10, 10)
    pygame.draw.ellipse(
        surface,
        neck_color,
        (x - width * 0.12, y - height * 0.35, width * 0.24, height * 0.1),
    )

    # Left arm holding the severed head
    arm_color = (45, 45, 55)
    # Upper arm
    pygame.draw.rect(
        surface,
        arm_color,
        (x - width * 0.45, y - height * 0.25, width * 0.15, height * 0.3),
    )
    # Forearm
    pygame.draw.rect(
        surface, arm_color, (x - width * 0.5, y, width * 0.12, height * 0.25)
    )

    # THE SEVERED HEAD being held up (glowing, supernatural)
    head_glow_alpha = int(100 + 50 * abs(math.sin(frame_count * 0.1)))
    glow_surface = pygame.Surface(
        (int(width * 0.4), int(height * 0.4)), pygame.SRCALPHA
    )
    glow_color = (100, 255, 100, head_glow_alpha)  # Eerie green glow
    pygame.draw.circle(
        glow_surface,
        glow_color,
        (int(width * 0.2), int(height * 0.2)),
        int(width * 0.2),
    )
    surface.blit(glow_surface, (x - width * 0.65, y - height * 0.1))

    # The actual severed head
    head_color = (180, 160, 140)  # Pale, dead skin
    head_radius = int(width * 0.15)
    head_pos = (int(x - width * 0.45), int(y + height * 0.1))
    pygame.draw.circle(surface, head_color, head_pos, head_radius)

    # Glowing eyes in the severed head
    eye_glow = (100, 255, 100)  # Matching green glow
    left_eye = (head_pos[0] - head_radius // 3, head_pos[1] - head_radius // 4)
    right_eye = (head_pos[0] + head_radius // 3, head_pos[1] - head_radius // 4)
    pygame.draw.circle(surface, eye_glow, left_eye, int(head_radius * 0.25))
    pygame.draw.circle(surface, eye_glow, right_eye, int(head_radius * 0.25))

    # Grim mouth
    mouth_color = (80, 80, 80)
    pygame.draw.arc(
        surface,
        mouth_color,
        (head_pos[0] - head_radius // 2, head_pos[1], head_radius, head_radius // 2),
        0,
        math.pi,
        3,
    )

    # Right arm holding reins/whip
    pygame.draw.rect(
        surface,
        arm_color,
        (x + width * 0.2, y - height * 0.2, width * 0.15, height * 0.35),
    )

    # Whip/reins
    whip_color = (100, 80, 60)
    whip_sway = int(8 * math.sin(frame_count * 0.12))
    pygame.draw.line(
        surface,
        whip_color,
        (int(x + width * 0.27), int(y + height * 0.15)),
        (int(x + width * 0.4 + whip_sway), int(y + height * 0.4)),
        3,
    )


def draw_changeling(surface, x, y, size, frame_count=0):
    """
    Draw a Changeling - fairy child left in place of human baby

    Small, unsettling child-like creature with fairy features
    """
    if isinstance(size, tuple):
        width, height = size
    else:
        width = height = size

    # Twitchy, unnatural movements
    twitch_x = int(2 * math.sin(frame_count * 0.2))
    twitch_y = int(2 * math.cos(frame_count * 0.25))
    x += twitch_x
    y += twitch_y

    # Small body (child-like, but wrong proportions)
    body_color = (200, 190, 180)
    # Oversized head for creepy effect
    head_radius = int(width * 0.22)
    head_pos = (int(x), int(y - height * 0.2))
    pygame.draw.circle(surface, body_color, head_pos, head_radius)

    # Small body/dress
    dress_color = (220, 200, 180)
    dress_points = [
        (x - width * 0.15, y),
        (x + width * 0.15, y),
        (x + width * 0.25, y + height * 0.4),
        (x - width * 0.25, y + height * 0.4),
    ]
    pygame.draw.polygon(surface, dress_color, dress_points)

    # Unsettling large eyes (too big, too knowing)
    eye_white = (240, 240, 255)
    eye_color = (20, 20, 60)  # Deep, unnatural blue
    # Left eye
    left_eye_pos = (int(x - head_radius * 0.4), int(y - height * 0.22))
    pygame.draw.circle(surface, eye_white, left_eye_pos, int(head_radius * 0.35))
    pygame.draw.circle(surface, eye_color, left_eye_pos, int(head_radius * 0.25))
    # Right eye
    right_eye_pos = (int(x + head_radius * 0.4), int(y - height * 0.22))
    pygame.draw.circle(surface, eye_white, right_eye_pos, int(head_radius * 0.35))
    pygame.draw.circle(surface, eye_color, right_eye_pos, int(head_radius * 0.25))

    # Unnatural gleam in eyes
    gleam = (200, 200, 255)
    pygame.draw.circle(surface, gleam, left_eye_pos, int(head_radius * 0.1))
    pygame.draw.circle(surface, gleam, right_eye_pos, int(head_radius * 0.1))

    # Too-wide smile (unsettling)
    smile_color = (100, 80, 80)
    smile_rect = pygame.Rect(
        x - head_radius * 0.5, y - height * 0.1, head_radius, head_radius * 0.3
    )
    pygame.draw.arc(surface, smile_color, smile_rect, 0, math.pi, 2)

    # Thin, spindly limbs (unnatural)
    limb_color = (190, 180, 170)
    # Arms
    pygame.draw.line(
        surface,
        limb_color,
        (int(x - width * 0.15), int(y + height * 0.05)),
        (int(x - width * 0.25), int(y + height * 0.25)),
        4,
    )
    pygame.draw.line(
        surface,
        limb_color,
        (int(x + width * 0.15), int(y + height * 0.05)),
        (int(x + width * 0.25), int(y + height * 0.25)),
        4,
    )

    # Legs
    pygame.draw.line(
        surface,
        limb_color,
        (int(x - width * 0.1), int(y + height * 0.4)),
        (int(x - width * 0.15), int(y + height * 0.6)),
        4,
    )
    pygame.draw.line(
        surface,
        limb_color,
        (int(x + width * 0.1), int(y + height * 0.4)),
        (int(x + width * 0.15), int(y + height * 0.6)),
        4,
    )

    # Faint fairy aura (revealing true nature)
    aura_alpha = int(50 + 30 * abs(math.sin(frame_count * 0.09)))
    aura_surface = pygame.Surface(
        (int(width * 1.2), int(height * 1.2)), pygame.SRCALPHA
    )
    aura_color = (180, 150, 255, aura_alpha)
    pygame.draw.circle(
        aura_surface,
        aura_color,
        (int(width * 0.6), int(height * 0.6)),
        int(width * 0.5),
    )
    surface.blit(aura_surface, (x - width * 0.6, y - height * 0.6))


def draw_clurichaun(surface, x, y, size, frame_count=0):
    """
    Draw a Clurichaun - drunk cousin of leprechaun, guards wine

    Similar to leprechaun but with disheveled appearance and wine bottle
    """
    if isinstance(size, tuple):
        width, height = size
    else:
        width = height = size

    # Drunken swaying motion
    sway = int(5 * math.sin(frame_count * 0.1))
    x += sway

    # Body (red coat instead of green - distinguishes from leprechaun)
    coat_color = (139, 0, 0)  # Dark red
    coat_rect = pygame.Rect(
        x - width * 0.3, y - height * 0.1, width * 0.6, height * 0.5
    )
    pygame.draw.rect(surface, coat_color, coat_rect)

    # Head (ruddy complexion from drinking)
    head_color = (255, 200, 180)  # Reddish skin
    head_radius = int(width * 0.2)
    head_pos = (int(x), int(y - height * 0.25))
    pygame.draw.circle(surface, head_color, head_pos, head_radius)

    # Red cap (slouched, disheveled)
    cap_color = (180, 0, 0)
    cap_tilt = int(3 * math.sin(frame_count * 0.08))
    # Brim
    cap_brim = pygame.Rect(
        x - width * 0.25 + cap_tilt, y - height * 0.38, width * 0.5, height * 0.08
    )
    pygame.draw.rect(surface, cap_color, cap_brim)
    # Top (tilted)
    cap_top = pygame.Rect(
        x - width * 0.18 + cap_tilt, y - height * 0.58, width * 0.36, height * 0.2
    )
    pygame.draw.rect(surface, cap_color, cap_top)

    # Orange/ginger beard (messy, unkempt)
    beard_color = (200, 100, 0)
    beard_points = [
        (x - head_radius * 0.7, y - height * 0.22),
        (x + head_radius * 0.7, y - height * 0.22),
        (x + head_radius * 0.5, y - height * 0.08),
        (x, y - height * 0.02),
        (x - head_radius * 0.5, y - height * 0.08),
    ]
    pygame.draw.polygon(surface, beard_color, beard_points)

    # Half-closed, drowsy eyes
    eye_color = (50, 50, 50)
    left_eye = (int(x - head_radius * 0.4), int(y - height * 0.28))
    right_eye = (int(x + head_radius * 0.4), int(y - height * 0.28))
    # Draw as slits (half-closed)
    pygame.draw.ellipse(surface, eye_color, (left_eye[0] - 4, left_eye[1] - 2, 8, 4))
    pygame.draw.ellipse(surface, eye_color, (right_eye[0] - 4, right_eye[1] - 2, 8, 4))

    # Rosy cheeks (from drinking)
    cheek_color = (255, 120, 120)
    pygame.draw.circle(
        surface,
        cheek_color,
        (int(x - head_radius * 0.6), int(y - height * 0.22)),
        int(head_radius * 0.3),
    )
    pygame.draw.circle(
        surface,
        cheek_color,
        (int(x + head_radius * 0.6), int(y - height * 0.22)),
        int(head_radius * 0.3),
    )

    # Legs
    leg_color = (40, 40, 40)
    left_leg = pygame.Rect(
        x - width * 0.2, y + height * 0.35, width * 0.15, height * 0.25
    )
    right_leg = pygame.Rect(
        x + width * 0.05, y + height * 0.35, width * 0.15, height * 0.25
    )
    pygame.draw.rect(surface, leg_color, left_leg)
    pygame.draw.rect(surface, leg_color, right_leg)

    # WINE BOTTLE in hand (key feature!)
    bottle_color = (40, 80, 40)  # Dark green glass
    bottle_x = int(x + width * 0.4)
    bottle_y = int(y - height * 0.05)
    # Bottle body
    pygame.draw.rect(
        surface, bottle_color, (bottle_x, bottle_y, width * 0.12, height * 0.25)
    )
    # Bottle neck
    pygame.draw.rect(
        surface,
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
        surface,
        cork_color,
        (bottle_x + width * 0.03, bottle_y - height * 0.1, width * 0.06, height * 0.03),
    )

    # Wine splash/drops (sloppy drinker)
    drop_color = (100, 20, 40)
    for i in range(2):
        drop_y = int(y + height * 0.15 + i * 8)
        pygame.draw.circle(surface, drop_color, (bottle_x, drop_y), 2)


def draw_merrow(surface, x, y, size, frame_count=0):
    """
    Draw a Merrow - Irish mermaid/merman

    Showing female version (beautiful) with optional hint at male version
    """
    if isinstance(size, tuple):
        width, height = size
    else:
        width = height = size

    # Graceful swimming motion
    swim_wave = math.sin(frame_count * 0.05) * 5
    y += swim_wave
    tail_sway = int(10 * math.sin(frame_count * 0.06))

    # Upper body (human, pale from ocean depths)
    skin_color = (220, 240, 235)  # Pale with slight green tint

    # Torso
    torso_rect = pygame.Rect(
        x - width * 0.2, y - height * 0.1, width * 0.4, height * 0.35
    )
    pygame.draw.ellipse(surface, skin_color, torso_rect)

    # Head
    head_radius = int(width * 0.18)
    head_pos = (int(x), int(y - height * 0.3))
    pygame.draw.circle(surface, skin_color, head_pos, head_radius)

    # Long flowing seaweed-like hair (green)
    hair_color = (60, 120, 80)
    hair_flow = int(15 * math.sin(frame_count * 0.07))
    # Multiple hair strands
    for i in range(5):
        hair_x = x - width * 0.2 + i * width * 0.1 + hair_flow
        hair_y_start = y - height * 0.35
        hair_y_end = y + height * 0.2 + i * 5
        pygame.draw.line(
            surface,
            hair_color,
            (int(hair_x), int(hair_y_start)),
            (int(hair_x + hair_flow * 0.5), int(hair_y_end)),
            3,
        )

    # Beautiful eyes (large, ocean-colored)
    eye_color = (100, 180, 200)  # Sea blue
    left_eye = (int(x - head_radius * 0.4), int(y - height * 0.32))
    right_eye = (int(x + head_radius * 0.4), int(y - height * 0.32))
    pygame.draw.circle(surface, eye_color, left_eye, int(head_radius * 0.25))
    pygame.draw.circle(surface, eye_color, right_eye, int(head_radius * 0.25))
    # Pupils
    pupil_color = (20, 20, 60)
    pygame.draw.circle(surface, pupil_color, left_eye, int(head_radius * 0.12))
    pygame.draw.circle(surface, pupil_color, right_eye, int(head_radius * 0.12))

    # Arms
    arm_color = skin_color
    # Left arm
    pygame.draw.line(
        surface,
        arm_color,
        (int(x - width * 0.2), int(y)),
        (int(x - width * 0.35), int(y + height * 0.15)),
        8,
    )
    # Right arm
    pygame.draw.line(
        surface,
        arm_color,
        (int(x + width * 0.2), int(y)),
        (int(x + width * 0.35), int(y + height * 0.15)),
        8,
    )

    # Fish tail (green/blue scales)
    tail_color = (80, 160, 140)
    scale_color = (60, 140, 120)

    # Main tail body
    tail_points = [
        (x - width * 0.2, y + height * 0.25),
        (x + width * 0.2, y + height * 0.25),
        (x + width * 0.15 + tail_sway, y + height * 0.5),
        (x - width * 0.15 + tail_sway, y + height * 0.5),
    ]
    pygame.draw.polygon(surface, tail_color, tail_points)

    # Tail fin (split)
    fin_left = [
        (x - width * 0.15 + tail_sway, y + height * 0.5),
        (x - width * 0.25 + tail_sway, y + height * 0.65),
        (x + tail_sway, y + height * 0.55),
    ]
    fin_right = [
        (x + width * 0.15 + tail_sway, y + height * 0.5),
        (x + width * 0.25 + tail_sway, y + height * 0.65),
        (x + tail_sway, y + height * 0.55),
    ]
    pygame.draw.polygon(surface, tail_color, fin_left)
    pygame.draw.polygon(surface, tail_color, fin_right)

    # Scale details
    for i in range(3):
        scale_y = y + height * 0.3 + i * height * 0.08
        pygame.draw.circle(
            surface,
            scale_color,
            (int(x - width * 0.1), int(scale_y)),
            int(width * 0.08),
        )
        pygame.draw.circle(
            surface,
            scale_color,
            (int(x + width * 0.1), int(scale_y)),
            int(width * 0.08),
        )

    # Bubbles (underwater)
    bubble_color = (200, 230, 255, 150)
    for i in range(3):
        bubble_x = int(x + width * 0.2 + 10 * math.sin(frame_count * 0.05 + i))
        bubble_y = int(y - height * 0.2 - i * 15 - (frame_count * 0.5) % 30)
        pygame.draw.circle(surface, bubble_color, (bubble_x, bubble_y), 4)


def draw_fear_gorta(surface, x, y, size, frame_count=0):
    """
    Draw a Fear Gorta - spirit of hunger as starving beggar

    Emaciated, desperate figure
    """
    if isinstance(size, tuple):
        width, height = size
    else:
        width = height = size

    # Weak, trembling movement
    tremble = int(1 * math.sin(frame_count * 0.3))
    x += tremble

    # Extremely thin, skeletal body
    body_color = (100, 90, 80)  # Sickly grayish-brown

    # Gaunt head (sunken features)
    head_radius = int(width * 0.16)
    head_pos = (int(x), int(y - height * 0.25))
    pygame.draw.circle(surface, body_color, head_pos, head_radius)

    # Sunken, hollow eyes
    eye_socket_color = (30, 30, 30)
    left_eye = (int(x - head_radius * 0.5), int(y - height * 0.27))
    right_eye = (int(x + head_radius * 0.5), int(y - height * 0.27))
    pygame.draw.circle(surface, eye_socket_color, left_eye, int(head_radius * 0.3))
    pygame.draw.circle(surface, eye_socket_color, right_eye, int(head_radius * 0.3))
    # Faint light in eyes (spirit)
    eye_light = (100, 100, 120)
    pygame.draw.circle(surface, eye_light, left_eye, int(head_radius * 0.15))
    pygame.draw.circle(surface, eye_light, right_eye, int(head_radius * 0.15))

    # Ragged, tattered clothes
    rags_color = (80, 70, 60)
    # Torn robe/cloak
    robe_points = [
        (x - width * 0.25, y - height * 0.1),
        (x + width * 0.25, y - height * 0.1),
        (x + width * 0.2, y + height * 0.4),
        (x, y + height * 0.45),
        (x - width * 0.2, y + height * 0.4),
    ]
    pygame.draw.polygon(surface, rags_color, robe_points)

    # Tattered edges (multiple tears)
    tear_color = (60, 50, 40)
    for i in range(4):
        tear_x = x - width * 0.2 + i * width * 0.13
        tear_y = y + height * 0.4
        pygame.draw.line(
            surface,
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
        surface,
        arm_color,
        (int(x - width * 0.2), int(y)),
        (int(x - width * 0.4), int(y + height * 0.2)),
        4,
    )
    # Skeletal hand
    pygame.draw.circle(
        surface,
        bone_color,
        (int(x - width * 0.4), int(y + height * 0.2)),
        int(width * 0.08),
    )
    # Finger bones
    for i in range(3):
        finger_x = x - width * 0.4 - width * 0.08
        finger_y = y + height * 0.18 + i * 4
        pygame.draw.line(
            surface,
            bone_color,
            (int(x - width * 0.4), int(y + height * 0.2)),
            (int(finger_x), int(finger_y)),
            2,
        )

    # Right arm
    pygame.draw.line(
        surface,
        arm_color,
        (int(x + width * 0.2), int(y)),
        (int(x + width * 0.35), int(y + height * 0.15)),
        4,
    )

    # Stick legs (barely supporting)
    leg_color = (85, 75, 65)
    pygame.draw.line(
        surface,
        leg_color,
        (int(x - width * 0.08), int(y + height * 0.4)),
        (int(x - width * 0.1), int(y + height * 0.6)),
        4,
    )
    pygame.draw.line(
        surface,
        leg_color,
        (int(x + width * 0.08), int(y + height * 0.4)),
        (int(x + width * 0.1), int(y + height * 0.6)),
        4,
    )

    # Faint ghostly aura (spirit nature)
    aura_alpha = int(40 + 20 * abs(math.sin(frame_count * 0.06)))
    aura_surface = pygame.Surface(
        (int(width * 1.4), int(height * 1.4)), pygame.SRCALPHA
    )
    aura_color = (120, 100, 80, aura_alpha)
    pygame.draw.ellipse(
        aura_surface, aura_color, (0, 0, int(width * 1.4), int(height * 1.4))
    )
    surface.blit(aura_surface, (x - width * 0.7, y - height * 0.7))

    # Begging bowl (empty)
    bowl_color = (60, 50, 40)
    bowl_x = int(x - width * 0.4)
    bowl_y = int(y + height * 0.25)
    pygame.draw.arc(
        surface, bowl_color, (bowl_x - 10, bowl_y - 5, 20, 15), 0, math.pi, 3
    )


def draw_cat_si(surface, x, y, size, frame_count=0):
    """
    Draw a Cat Sí (Cat Sidhe) - large black fairy cat with white chest spot

    Soul-stealing feline
    """
    if isinstance(size, tuple):
        width, height = size
    else:
        width = height = size

    # Prowling animation (tail swish)
    tail_swish = int(15 * math.sin(frame_count * 0.08))

    # Large cat body (black)
    body_color = (10, 10, 15)  # Almost pure black

    # Main body
    body_ellipse = pygame.Rect(
        x - width * 0.35, y - height * 0.05, width * 0.7, height * 0.35
    )
    pygame.draw.ellipse(surface, body_color, body_ellipse)

    # Head
    head_radius = int(width * 0.2)
    head_pos = (int(x - width * 0.15), int(y - height * 0.25))
    pygame.draw.circle(surface, body_color, head_pos, head_radius)

    # Pointed ears (alert, large)
    ear_color = (15, 15, 20)
    # Left ear
    left_ear = [
        (head_pos[0] - head_radius * 0.6, head_pos[1] - head_radius * 0.4),
        (head_pos[0] - head_radius * 0.8, head_pos[1] - head_radius * 1.2),
        (head_pos[0] - head_radius * 0.3, head_pos[1] - head_radius * 0.7),
    ]
    pygame.draw.polygon(surface, ear_color, left_ear)
    # Right ear
    right_ear = [
        (head_pos[0] + head_radius * 0.6, head_pos[1] - head_radius * 0.4),
        (head_pos[0] + head_radius * 0.8, head_pos[1] - head_radius * 1.2),
        (head_pos[0] + head_radius * 0.3, head_pos[1] - head_radius * 0.7),
    ]
    pygame.draw.polygon(surface, ear_color, right_ear)

    # Inner ear (pink)
    ear_inner = (80, 40, 60)
    pygame.draw.polygon(
        surface,
        ear_inner,
        [
            (left_ear[0][0] + 3, left_ear[0][1] + 2),
            (left_ear[1][0] + 5, left_ear[1][1] + 3),
            (left_ear[2][0] + 2, left_ear[2][1] + 1),
        ],
    )
    pygame.draw.polygon(
        surface,
        ear_inner,
        [
            (right_ear[0][0] - 3, right_ear[0][1] + 2),
            (right_ear[1][0] - 5, right_ear[1][1] + 3),
            (right_ear[2][0] - 2, right_ear[2][1] + 1),
        ],
    )

    # WHITE CHEST SPOT (distinctive feature!)
    chest_color = (240, 240, 245)
    chest_spot = pygame.Rect(x - width * 0.18, y, width * 0.25, height * 0.2)
    pygame.draw.ellipse(surface, chest_color, chest_spot)

    # Glowing supernatural eyes (green, like all fairy cats)
    eye_glow_intensity = int(150 + 100 * abs(math.sin(frame_count * 0.12)))
    eye_color = (0, eye_glow_intensity, 0)  # Eerie green glow
    eye_glow_color = (0, 100, 0)

    left_eye_pos = (head_pos[0] - head_radius * 0.4, head_pos[1] - head_radius * 0.2)
    right_eye_pos = (head_pos[0] + head_radius * 0.4, head_pos[1] - head_radius * 0.2)

    # Glow around eyes
    pygame.draw.circle(surface, eye_glow_color, left_eye_pos, int(head_radius * 0.25))
    pygame.draw.circle(surface, eye_glow_color, right_eye_pos, int(head_radius * 0.25))
    # Bright eyes
    pygame.draw.circle(surface, eye_color, left_eye_pos, int(head_radius * 0.18))
    pygame.draw.circle(surface, eye_color, right_eye_pos, int(head_radius * 0.18))
    # Slit pupils
    pupil_color = (0, 0, 0)
    pygame.draw.ellipse(
        surface, pupil_color, (left_eye_pos[0] - 2, left_eye_pos[1] - 6, 4, 12)
    )
    pygame.draw.ellipse(
        surface, pupil_color, (right_eye_pos[0] - 2, right_eye_pos[1] - 6, 4, 12)
    )

    # Whiskers
    whisker_color = (200, 200, 210)
    for i in range(-1, 2):
        # Left whiskers
        pygame.draw.line(
            surface,
            whisker_color,
            (int(head_pos[0] - head_radius * 0.2), int(head_pos[1] + i * 5)),
            (int(head_pos[0] - head_radius * 1.2), int(head_pos[1] + i * 8)),
            1,
        )
        # Right whiskers
        pygame.draw.line(
            surface,
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
        surface, leg_color, (x - width * 0.25, y + height * 0.25, leg_width, leg_height)
    )
    pygame.draw.rect(
        surface, leg_color, (x - width * 0.1, y + height * 0.25, leg_width, leg_height)
    )
    # Back legs
    pygame.draw.rect(
        surface, leg_color, (x + width * 0.1, y + height * 0.25, leg_width, leg_height)
    )
    pygame.draw.rect(
        surface, leg_color, (x + width * 0.25, y + height * 0.25, leg_width, leg_height)
    )

    # Long swishing tail
    tail_color = (12, 12, 18)
    tail_points = [
        (x + width * 0.35, y + height * 0.05),
        (x + width * 0.45 + tail_swish, y - height * 0.1),
        (x + width * 0.5 + tail_swish, y - height * 0.25),
        (x + width * 0.48 + tail_swish, y - height * 0.05),
        (x + width * 0.38, y + height * 0.1),
    ]
    pygame.draw.polygon(surface, tail_color, tail_points)

    # Supernatural aura (fairy creature)
    aura_alpha = int(30 + 20 * abs(math.sin(frame_count * 0.07)))
    aura_surface = pygame.Surface(
        (int(width * 1.3), int(height * 1.3)), pygame.SRCALPHA
    )
    aura_color = (50, 150, 50, aura_alpha)  # Green fairy aura
    pygame.draw.circle(
        aura_surface,
        aura_color,
        (int(width * 0.65), int(height * 0.65)),
        int(width * 0.5),
    )
    surface.blit(aura_surface, (x - width * 0.65, y - height * 0.65))


# Dictionary mapping monster type names to their drawing functions
MONSTER_RENDERERS = {
    "banshee": draw_banshee,
    "leprechaun": draw_leprechaun,
    "pooka": draw_pooka,
    "selkie": draw_selkie,
    "dullahan": draw_dullahan,
    "changeling": draw_changeling,
    "clurichaun": draw_clurichaun,
    "merrow": draw_merrow,
    "fear_gorta": draw_fear_gorta,
    "cat_si": draw_cat_si,
}
