"""HUD (Heads-Up Display) for displaying player stats and resources."""

import pygame
import math
import config


class HUD:
    """Manages the player's heads-up display showing health, potions, and currency."""

    def __init__(self):
        """Initialize the HUD with default values."""
        # Animation state
        self.displayed_health = 0  # For smooth health animation
        self.animation_speed = 2.0  # Health bar animation speed

        # Visual feedback for potion use
        self.potion_glow_timer = 0
        self.potion_glow_duration = 500  # milliseconds

        # Critical health warning
        self.critical_health_timer = 0
        self.critical_health_threshold = 0.25  # 25% health

        # Colors for medieval-fantasy theme
        self.wood_color = (101, 67, 33)  # Dark brown wood
        self.wood_border = (65, 43, 21)  # Darker wood border
        self.ornate_gold = (218, 165, 32)  # Ornate golden color
        self.health_green = (76, 187, 23)  # Vibrant health green
        self.health_red = (220, 50, 50)  # Health red
        self.health_critical = (139, 0, 0)  # Critical health dark red
        self.text_color = (255, 248, 220)  # Cornsilk for readable text

    def update(self, warrior, dt: float):
        """
        Update HUD animations and timers.

        Args:
            warrior: The warrior entity to track
            dt: Delta time in seconds
        """
        # Initialize displayed health on first update
        if self.displayed_health == 0 and warrior.health > 0:
            self.displayed_health = warrior.health

        # Smooth health bar animation
        if self.displayed_health < warrior.health:
            self.displayed_health = min(
                self.displayed_health + self.animation_speed * dt * 100, warrior.health
            )
        elif self.displayed_health > warrior.health:
            self.displayed_health = max(
                self.displayed_health - self.animation_speed * dt * 100, warrior.health
            )

        # Update potion glow timer
        if self.potion_glow_timer > 0:
            self.potion_glow_timer -= dt * 1000  # Convert to milliseconds

        # Update critical health warning timer
        if warrior.health / warrior.max_health <= self.critical_health_threshold:
            self.critical_health_timer += dt * 1000
        else:
            self.critical_health_timer = 0

    def trigger_potion_glow(self):
        """Trigger visual feedback when a potion is used."""
        self.potion_glow_timer = self.potion_glow_duration

    def draw(self, screen: pygame.Surface, warrior):
        """
        Draw the HUD on screen.

        Args:
            screen: Pygame surface to draw on
            warrior: The warrior entity to display stats for
        """
        # Draw health bar panel
        self._draw_health_panel(screen, warrior)

        # Draw potion count panel
        self._draw_potion_panel(screen, warrior)

        # Draw currency panel
        self._draw_currency_panel(screen, warrior)

        # Draw critical health warning if needed
        if warrior.health / warrior.max_health <= self.critical_health_threshold:
            self._draw_critical_health_warning(screen)

    def _draw_ornate_border(self, surface: pygame.Surface, rect: pygame.Rect):
        """
        Draw an ornate medieval-style border around a rectangle.

        Args:
            surface: Surface to draw on
            rect: Rectangle to draw border around
        """
        # Draw outer border (darker)
        pygame.draw.rect(surface, self.wood_border, rect, 3)

        # Draw inner ornate line (golden)
        inner_rect = rect.inflate(-6, -6)
        pygame.draw.rect(surface, self.ornate_gold, inner_rect, 1)

        # Draw corner decorations (small circles)
        corner_radius = 3
        corners = [
            (rect.left + 5, rect.top + 5),
            (rect.right - 5, rect.top + 5),
            (rect.left + 5, rect.bottom - 5),
            (rect.right - 5, rect.bottom - 5),
        ]
        for corner in corners:
            pygame.draw.circle(surface, self.ornate_gold, corner, corner_radius)

    def _draw_health_panel(self, screen: pygame.Surface, warrior):
        """
        Draw the health panel with visual and numerical display.

        Args:
            screen: Pygame surface to draw on
            warrior: The warrior entity
        """
        # Panel dimensions and position (top-left)
        panel_width = 280
        panel_height = 80
        panel_x = 10
        panel_y = 10

        # Create panel background (wooden frame)
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, self.wood_color, panel_rect)
        self._draw_ornate_border(screen, panel_rect)

        # Draw title
        font_title = pygame.font.Font(None, 24)
        title_text = font_title.render("Health", True, self.ornate_gold)
        screen.blit(title_text, (panel_x + 10, panel_y + 8))

        # Health bar dimensions
        bar_width = 240
        bar_height = 24
        bar_x = panel_x + 20
        bar_y = panel_y + 38

        # Calculate health percentage
        health_percentage = warrior.health / warrior.max_health
        displayed_percentage = self.displayed_health / warrior.max_health

        # Draw health bar background (darker)
        bar_bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, self.wood_border, bar_bg_rect)

        # Draw health bar fill with color gradient based on health
        if displayed_percentage > 0:
            fill_width = int(bar_width * displayed_percentage)
            bar_fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)

            # Color changes from green -> yellow -> red as health decreases
            if health_percentage > 0.5:
                bar_color = self.health_green
            elif health_percentage > 0.25:
                bar_color = (220, 220, 50)  # Yellow
            else:
                bar_color = self.health_red

            pygame.draw.rect(screen, bar_color, bar_fill_rect)

        # Draw health bar border
        pygame.draw.rect(screen, self.ornate_gold, bar_bg_rect, 2)

        # Draw numerical health display
        font_health = pygame.font.Font(None, 28)
        health_text = font_health.render(
            f"{int(warrior.health)}/{warrior.max_health} HP", True, self.text_color
        )
        # Center text on health bar
        text_rect = health_text.get_rect(
            center=(bar_x + bar_width // 2, bar_y + bar_height // 2)
        )

        # Add text shadow for better readability
        shadow_text = font_health.render(
            f"{int(warrior.health)}/{warrior.max_health} HP", True, (0, 0, 0)
        )
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        screen.blit(shadow_text, shadow_rect)
        screen.blit(health_text, text_rect)

    def _draw_potion_panel(self, screen: pygame.Surface, warrior):
        """
        Draw the health potion panel with count and visual feedback.

        Args:
            screen: Pygame surface to draw on
            warrior: The warrior entity
        """
        # Panel dimensions and position (below health)
        panel_width = 280
        panel_height = 70
        panel_x = 10
        panel_y = 100

        # Create panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, self.wood_color, panel_rect)
        self._draw_ornate_border(screen, panel_rect)

        # Draw potion icon (stylized bottle)
        icon_size = 40
        icon_x = panel_x + 15
        icon_y = panel_y + 15

        # Apply glow effect if potion was just used
        glow_active = self.potion_glow_timer > 0
        if glow_active:
            # Pulsing glow effect
            glow_alpha = int(128 * (self.potion_glow_timer / self.potion_glow_duration))
            glow_surface = pygame.Surface((icon_size + 10, icon_size + 10))
            glow_surface.set_alpha(glow_alpha)
            pygame.draw.circle(
                glow_surface,
                (100, 255, 100),
                (icon_size // 2 + 5, icon_size // 2 + 5),
                icon_size // 2 + 5,
            )
            screen.blit(glow_surface, (icon_x - 5, icon_y - 5))

        # Draw potion bottle
        bottle_rect = pygame.Rect(icon_x + 10, icon_y + 8, 20, 24)
        pygame.draw.rect(screen, (200, 50, 50), bottle_rect)  # Red potion
        # Bottle neck
        neck_rect = pygame.Rect(icon_x + 14, icon_y + 4, 12, 8)
        pygame.draw.rect(screen, (200, 50, 50), neck_rect)
        # Cork
        cork_rect = pygame.Rect(icon_x + 16, icon_y, 8, 6)
        pygame.draw.rect(screen, (139, 69, 19), cork_rect)
        # Highlight on bottle
        highlight = pygame.Rect(icon_x + 12, icon_y + 10, 4, 10)
        pygame.draw.rect(screen, (255, 100, 100), highlight)

        # Draw potion count
        font_title = pygame.font.Font(None, 24)
        title_text = font_title.render("Health Potions", True, self.ornate_gold)
        screen.blit(title_text, (panel_x + 65, panel_y + 10))

        # Draw count (large and prominent)
        font_count = pygame.font.Font(None, 42)
        count_text = font_count.render(
            f"x {warrior.health_potions}", True, self.text_color
        )
        screen.blit(count_text, (panel_x + 70, panel_y + 30))

        # Draw usage hint
        font_hint = pygame.font.Font(None, 18)
        hint_text = font_hint.render("Press P to use", True, config.GRAY)
        screen.blit(hint_text, (panel_x + 180, panel_y + 42))

    def _draw_currency_panel(self, screen: pygame.Surface, warrior):
        """
        Draw the currency/gold panel.

        Args:
            screen: Pygame surface to draw on
            warrior: The warrior entity
        """
        # Panel dimensions and position (below potions)
        panel_width = 280
        panel_height = 60
        panel_x = 10
        panel_y = 180

        # Create panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, self.wood_color, panel_rect)
        self._draw_ornate_border(screen, panel_rect)

        # Draw gold coin icon
        coin_center_x = panel_x + 30
        coin_center_y = panel_y + 30
        coin_radius = 15

        # Outer gold circle
        pygame.draw.circle(
            screen, self.ornate_gold, (coin_center_x, coin_center_y), coin_radius
        )
        # Inner darker circle for depth
        pygame.draw.circle(
            screen, (184, 134, 11), (coin_center_x, coin_center_y), coin_radius - 3
        )
        # Center decoration
        pygame.draw.circle(
            screen, self.ornate_gold, (coin_center_x, coin_center_y), coin_radius - 6
        )

        # Draw gold amount
        font_title = pygame.font.Font(None, 24)
        title_text = font_title.render("Gold", True, self.ornate_gold)
        screen.blit(title_text, (panel_x + 60, panel_y + 8))

        font_gold = pygame.font.Font(None, 36)
        gold_text = font_gold.render(f"{warrior.gold}", True, self.text_color)
        screen.blit(gold_text, (panel_x + 60, panel_y + 26))

    def _draw_critical_health_warning(self, screen: pygame.Surface):
        """
        Draw a visual warning when health is critically low.

        Args:
            screen: Pygame surface to draw on
        """
        # Pulsing red vignette effect
        alpha = int(80 * (0.5 + 0.5 * math.sin(self.critical_health_timer / 200)))

        # Create semi-transparent red overlay at screen edges
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(alpha)
        overlay.fill((139, 0, 0))

        # Draw vignette (darker at edges)
        # Top
        pygame.draw.rect(overlay, (139, 0, 0), (0, 0, config.SCREEN_WIDTH, 50))
        # Bottom
        pygame.draw.rect(
            overlay,
            (139, 0, 0),
            (0, config.SCREEN_HEIGHT - 50, config.SCREEN_WIDTH, 50),
        )
        # Left
        pygame.draw.rect(overlay, (139, 0, 0), (0, 0, 50, config.SCREEN_HEIGHT))
        # Right
        pygame.draw.rect(
            overlay,
            (139, 0, 0),
            (config.SCREEN_WIDTH - 50, 0, 50, config.SCREEN_HEIGHT),
        )

        screen.blit(overlay, (0, 0))

        # Draw warning text (pulsing)
        if int(self.critical_health_timer / 500) % 2 == 0:
            font_warning = pygame.font.Font(None, 32)
            warning_text = font_warning.render(
                "LOW HEALTH!", True, self.health_critical
            )
            warning_rect = warning_text.get_rect(
                center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 30)
            )

            # Add shadow
            shadow_text = font_warning.render("LOW HEALTH!", True, (0, 0, 0))
            shadow_rect = warning_rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            screen.blit(shadow_text, shadow_rect)
            screen.blit(warning_text, warning_rect)
