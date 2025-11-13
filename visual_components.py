"""
Visual Component Library for Monster Rendering

Provides reusable helper methods for common visual effects used in monster rendering.
"""

import pygame
import math


def apply_floating_effect(
    y: float, frame_count: int, amplitude: float = 3.0, speed: float = 0.05
) -> float:
    """
    Apply a gentle floating/bobbing animation effect.

    Args:
        y: Base y position
        frame_count: Current frame number for animation
        amplitude: How far to float up/down (default 3 pixels)
        speed: Animation speed multiplier (default 0.05)

    Returns:
        Modified y position with floating effect applied
    """
    float_offset = math.sin(frame_count * speed) * amplitude
    return y + float_offset


def create_transparent_surface(width: int, height: int) -> pygame.Surface:
    """
    Create a transparent surface for ghostly/overlay effects.

    Args:
        width: Surface width in pixels
        height: Surface height in pixels

    Returns:
        pygame.Surface with SRCALPHA flag for transparency
    """
    return pygame.Surface((width, height), pygame.SRCALPHA)


def draw_glow_effect(
    surface: pygame.Surface,
    center: tuple[int, int],
    radius: int,
    color: tuple[int, int, int],
    frame_count: int,
    min_alpha: int = 50,
    max_alpha: int = 150,
    speed: float = 0.1,
) -> None:
    """
    Draw an animated glowing aura effect.

    Args:
        surface: pygame surface to draw on
        center: (x, y) center position of glow
        radius: Glow radius in pixels
        color: RGB color tuple (alpha will be animated)
        frame_count: Current frame for animation
        min_alpha: Minimum alpha transparency (0-255)
        max_alpha: Maximum alpha transparency (0-255)
        speed: Animation speed multiplier
    """
    # Calculate pulsing alpha
    alpha = int(
        min_alpha + (max_alpha - min_alpha) * abs(math.sin(frame_count * speed))
    )

    # Create transparent surface for the glow
    glow_surface = create_transparent_surface(radius * 3, radius * 3)
    glow_color = (*color, alpha)

    # Draw the glow circle
    pygame.draw.circle(
        glow_surface,
        glow_color,
        (radius * 1.5, radius * 1.5),
        radius,
    )

    # Blit to main surface
    surface.blit(glow_surface, (center[0] - radius * 1.5, center[1] - radius * 1.5))


def draw_wispy_trail(
    surface: pygame.Surface,
    x: float,
    y: float,
    width: float,
    height: float,
    frame_count: int,
    color: tuple[int, int, int] = (200, 220, 240),
    min_alpha: int = 50,
    max_alpha: int = 150,
) -> None:
    """
    Draw a wispy trailing effect (for ghosts, spirits, etc.).

    Args:
        surface: pygame surface to draw on
        x: Center x position
        y: Base y position for trail
        width: Width reference for sizing
        height: Height reference for positioning
        frame_count: Current frame for animation
        color: RGB color for the wisp
        min_alpha: Minimum alpha transparency
        max_alpha: Maximum alpha transparency
    """
    # Animated transparency
    wisp_alpha = int(
        min_alpha + (max_alpha - min_alpha) * abs(math.sin(frame_count * 0.1))
    )
    wisp_color = (*color, wisp_alpha)

    # Animated vertical offset
    wisp_y_offset = int(10 * math.sin(frame_count * 0.08))

    # Create transparent surface
    temp_surface = create_transparent_surface(int(width), int(height))

    # Draw wispy circle
    pygame.draw.circle(
        temp_surface,
        wisp_color,
        (int(width * 0.5), int(height * 0.95) + wisp_y_offset),
        int(width * 0.15),
    )

    # Blit to main surface
    surface.blit(temp_surface, (int(x - width // 2), int(y - height // 2)))


def apply_size_tuple(size) -> tuple[float, float]:
    """
    Normalize size parameter to (width, height) tuple.

    Args:
        size: Either a single value or (width, height) tuple

    Returns:
        (width, height) tuple
    """
    if isinstance(size, tuple):
        return size
    else:
        return (size, size)


def apply_pulse_effect(
    size: float, frame_count: int, intensity: float = 0.1, speed: float = 0.06
) -> float:
    """
    Apply a pulsing/breathing animation effect to size.

    Args:
        size: Base size value
        frame_count: Current frame for animation
        intensity: Pulse intensity (0.1 = 10% size variation)
        speed: Animation speed multiplier

    Returns:
        Modified size with pulse effect applied
    """
    pulse = math.sin(frame_count * speed) * intensity + 1.0
    return size * pulse


def draw_aura_effect(
    surface: pygame.Surface,
    x: float,
    y: float,
    width: float,
    height: float,
    frame_count: int,
    color: tuple[int, int, int],
    min_alpha: int = 30,
    max_alpha: int = 80,
    size_multiplier: float = 1.3,
) -> None:
    """
    Draw an animated aura/supernatural energy effect around a creature.

    Args:
        surface: pygame surface to draw on
        x: Center x position
        y: Center y position
        width: Reference width for sizing
        height: Reference height for sizing
        frame_count: Current frame for animation
        color: RGB color for the aura
        min_alpha: Minimum alpha transparency
        max_alpha: Maximum alpha transparency
        size_multiplier: How much larger than the creature (default 1.3x)
    """
    # Animated alpha
    aura_alpha = int(
        min_alpha + (max_alpha - min_alpha) * abs(math.sin(frame_count * 0.07))
    )

    # Create transparent surface
    aura_width = int(width * size_multiplier)
    aura_height = int(height * size_multiplier)
    aura_surface = create_transparent_surface(aura_width, aura_height)

    # Draw aura
    aura_color = (*color, aura_alpha)
    pygame.draw.circle(
        aura_surface,
        aura_color,
        (aura_width // 2, aura_height // 2),
        min(aura_width, aura_height) // 2,
    )

    # Blit to main surface
    surface.blit(aura_surface, (x - aura_width // 2, y - aura_height // 2))
