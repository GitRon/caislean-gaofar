"""Warrior class - player controlled character."""

import pygame
from entity import Entity
from inventory import Inventory
from grid import Grid
import config


class Warrior(Entity):
    """Player-controlled warrior character."""

    def __init__(self, grid_x: int, grid_y: int):
        """Initialize the warrior at the given grid position."""
        super().__init__(
            grid_x=grid_x,
            grid_y=grid_y,
            size=config.WARRIOR_SIZE,
            color=config.BLUE,
            max_health=config.WARRIOR_MAX_HEALTH,
            speed=config.WARRIOR_SPEED,
            attack_damage=config.WARRIOR_ATTACK_DAMAGE,
            attack_cooldown=config.WARRIOR_ATTACK_COOLDOWN
        )
        self.inventory = Inventory()
        self.base_attack_damage = config.WARRIOR_ATTACK_DAMAGE
        self.pending_action = None  # Store pending action for this turn

    def get_effective_attack_damage(self) -> int:
        """Get total attack damage including inventory bonuses."""
        return self.base_attack_damage + self.inventory.get_total_attack_bonus()

    def attack(self, target: 'Entity') -> bool:
        """
        Attempt to attack a target with effective damage.

        Returns:
            True if attack was successful, False otherwise
        """
        if not self.can_attack():
            return False

        effective_damage = self.get_effective_attack_damage()
        target.take_damage(effective_damage)
        self.turns_since_last_attack = 0
        return True

    def queue_movement(self, dx: int, dy: int):
        """
        Queue a movement action for the next turn.

        Args:
            dx: Delta x in tiles
            dy: Delta y in tiles
        """
        self.pending_action = ('move', dx, dy)

    def queue_attack(self):
        """Queue an attack action for the next turn."""
        self.pending_action = ('attack',)

    def execute_turn(self, target: 'Entity' = None) -> bool:
        """
        Execute the queued action for this turn.

        Args:
            target: Target entity for attack actions

        Returns:
            True if an action was executed, False otherwise
        """
        if self.pending_action is None:
            return False

        action_type = self.pending_action[0]

        if action_type == 'move':
            _, dx, dy = self.pending_action
            self.move(dx, dy)
            self.pending_action = None
            return True
        elif action_type == 'attack':
            if target and self.grid_distance_to(target) <= config.MONSTER_ATTACK_RANGE:
                success = self.attack(target)
                self.pending_action = None
                return success
            self.pending_action = None
            return False

        return False

    def draw(self, screen: pygame.Surface):
        """Draw the warrior with special styling."""
        # Draw the entity
        super().draw(screen)

        # Draw a cross pattern to make it look like a warrior
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2

        # Vertical line
        pygame.draw.line(screen, config.WHITE,
                        (center_x, self.y + 5),
                        (center_x, self.y + self.size - 5), 2)

        # Horizontal line
        pygame.draw.line(screen, config.WHITE,
                        (self.x + 5, center_y),
                        (self.x + self.size - 5, center_y), 2)
