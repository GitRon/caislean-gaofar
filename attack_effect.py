"""Visual effects for attacks."""

import pygame
import math


class AttackEffect:
    """Visual effect shown when an entity attacks."""

    def __init__(self, x: float, y: float, is_crit: bool = False):
        """
        Initialize an attack effect.

        Args:
            x: X position in pixels (center of effect)
            y: Y position in pixels (center of effect)
            is_crit: Whether this was a critical hit
        """
        self.x = x
        self.y = y
        self.is_crit = is_crit
        self.active = True
        self.effect_time = 0.5  # 0.5 second effect duration
        self.animation_time = 0.0
        self.max_duration = 0.5

    def update(self, dt: float):
        """
        Update the attack effect animation.

        Args:
            dt: Delta time since last update
        """
        if not self.active:
            return

        self.animation_time += dt
        self.effect_time -= dt

        if self.effect_time <= 0:
            self.active = False

    def draw(self, screen: pygame.Surface):
        """
        Draw the attack effect.

        Args:
            screen: Pygame surface to draw on
        """
        if not self.active:
            return

        # Calculate progress (0.0 to 1.0, where 1.0 is complete)
        progress = 1.0 - (self.effect_time / self.max_duration)

        # Pulsing effect using sine wave
        pulse = abs(math.sin(self.animation_time * 12))

        # Choose color based on crit status
        if self.is_crit:
            # Critical hits are bright yellow/orange
            base_color = (255, 215, 0)  # Gold
        else:
            # Normal attacks are red/orange
            base_color = (255, 100, 50)  # Red-orange

        # Calculate radius based on progress (expands then fades)
        max_radius = 35 if self.is_crit else 25
        radius = int(max_radius * (0.5 + progress * 0.5))

        # Multiple glow layers for soft effect (similar to temple healing)
        for i in range(3):
            # Alpha decreases as effect progresses and by layer
            alpha_value = int(200 * (1 - progress) * (1 - i / 3) * pulse)
            layer_radius = radius - (i * 6)

            if layer_radius > 0:
                # Create surface with per-pixel alpha
                glow_surface = pygame.Surface(
                    (layer_radius * 2, layer_radius * 2), pygame.SRCALPHA
                )
                glow_color = (*base_color, alpha_value)
                pygame.draw.circle(
                    glow_surface, glow_color, (layer_radius, layer_radius), layer_radius
                )
                screen.blit(
                    glow_surface, (self.x - layer_radius, self.y - layer_radius)
                )

        # Add impact flash lines for crits
        if self.is_crit and progress < 0.5:
            # Draw impact lines radiating outward
            line_length = int(20 * (1 - progress * 2))
            line_alpha = int(255 * (1 - progress * 2))
            line_color = (255, 255, 255, line_alpha)

            # Create surface for lines
            line_surface = pygame.Surface((80, 80), pygame.SRCALPHA)

            # Draw 8 lines in different directions
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                start_x = 40 + int(math.cos(rad) * 10)
                start_y = 40 + int(math.sin(rad) * 10)
                end_x = 40 + int(math.cos(rad) * (10 + line_length))
                end_y = 40 + int(math.sin(rad) * (10 + line_length))

                pygame.draw.line(
                    line_surface, line_color, (start_x, start_y), (end_x, end_y), 2
                )

            screen.blit(line_surface, (self.x - 40, self.y - 40))


class AttackEffectManager:
    """Manages multiple attack effects."""

    def __init__(self):
        """Initialize the attack effect manager."""
        self.effects = []

    def add_effect(self, x: float, y: float, is_crit: bool = False):
        """
        Add a new attack effect.

        Args:
            x: X position in pixels (center of effect)
            y: Y position in pixels (center of effect)
            is_crit: Whether this was a critical hit
        """
        effect = AttackEffect(x, y, is_crit)
        self.effects.append(effect)

    def update(self, dt: float):
        """
        Update all active attack effects.

        Args:
            dt: Delta time since last update
        """
        for effect in self.effects:
            effect.update(dt)

        # Remove inactive effects
        self.effects = [e for e in self.effects if e.active]

    def draw(self, screen: pygame.Surface):
        """
        Draw all active attack effects.

        Args:
            screen: Pygame surface to draw on
        """
        for effect in self.effects:
            effect.draw(screen)

    def clear(self):
        """Clear all attack effects."""
        self.effects = []
