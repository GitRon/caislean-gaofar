"""State management for HUD."""


class HUDState:
    """Manages the state of the HUD (Heads-Up Display)."""

    def __init__(self):
        """Initialize HUD state."""
        # Animation state
        self.displayed_health = 0  # For smooth health animation
        self.animation_speed = 2.0  # Health bar animation speed

        # Visual feedback for potion use
        self.potion_glow_timer = 0
        self.potion_glow_duration = 500  # milliseconds

        # Critical health warning
        self.critical_health_timer = 0
        self.critical_health_threshold = 0.25  # 25% health

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

    def is_potion_glowing(self) -> bool:
        """Check if potion glow effect is active."""
        return self.potion_glow_timer > 0

    def is_critical_health(self, warrior) -> bool:
        """Check if health is critically low."""
        return warrior.health / warrior.max_health <= self.critical_health_threshold
