"""Warrior class - player controlled character."""

import pygame
from entity import Entity
from inventory import Inventory
from item import ItemType
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
            attack_cooldown=config.WARRIOR_ATTACK_COOLDOWN,
        )
        self.inventory = Inventory()
        self.base_attack_damage = config.WARRIOR_ATTACK_DAMAGE
        self.pending_action = None  # Store pending action for this turn
        self.gold = 0  # Track gold as separate currency

    def get_effective_attack_damage(self) -> int:
        """Get total attack damage including inventory bonuses."""
        return self.base_attack_damage + self.inventory.get_total_attack_bonus()

    def get_effective_defense(self) -> int:
        """Get total defense including inventory bonuses."""
        return self.inventory.get_total_defense_bonus()

    def take_damage(self, damage: int, defense: int = 0):
        """
        Take damage with defense bonus automatically applied.

        Args:
            damage: Raw damage amount
            defense: Additional defense (default 0, uses inventory defense)
        """
        total_defense = self.get_effective_defense() + defense
        super().take_damage(damage, total_defense)

    def count_health_potions(self) -> int:
        """
        Count health potions in inventory.

        Returns:
            Number of health potions in inventory
        """
        count = 0
        for item in self.inventory.backpack_slots:
            if (
                item
                and item.item_type == ItemType.CONSUMABLE
                and item.name != "Town Portal"
                and item.health_bonus > 0
            ):
                count += 1
        return count

    def count_town_portals(self) -> int:
        """
        Count town portals in inventory.

        Returns:
            Number of town portals in inventory
        """
        count = 0
        for item in self.inventory.backpack_slots:
            if item and item.name == "Town Portal":
                count += 1
        return count

    def count_gold(self) -> int:
        """
        Get current gold amount.

        Returns:
            Current gold currency amount
        """
        return self.gold

    def add_gold(self, amount: int):
        """
        Add gold to the warrior's currency.

        Args:
            amount: Amount of gold to add
        """
        self.gold += amount

    def remove_gold(self, amount: int) -> bool:
        """
        Remove gold from the warrior's currency.

        Args:
            amount: Amount of gold to remove

        Returns:
            True if successful, False if not enough gold
        """
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def use_health_potion(self) -> bool:
        """
        Use a health potion from inventory to restore health.

        Returns:
            True if potion was used successfully, False if no potions available
        """
        if self.health >= self.max_health:
            return False

        # Find first health potion in backpack (not town portal)
        for i, item in enumerate(self.inventory.backpack_slots):
            if (
                item
                and item.item_type == ItemType.CONSUMABLE
                and item.name != "Town Portal"
                and item.health_bonus > 0
            ):
                # Use the potion
                heal_amount = item.health_bonus if item.health_bonus > 0 else 30
                self.health = min(self.max_health, self.health + heal_amount)
                # Remove from inventory
                self.inventory.backpack_slots[i] = None
                return True

        return False

    def use_town_portal(self) -> bool:
        """
        Use a town portal from inventory to open a portal.

        Returns:
            True if portal was used successfully, False if no portals available
        """
        # Find first town portal in backpack
        for i, item in enumerate(self.inventory.backpack_slots):
            if item and item.name == "Town Portal":
                # Remove from inventory
                self.inventory.backpack_slots[i] = None
                return True

        return False

    def attack(self, target: "Entity") -> bool:
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
        self.pending_action = ("move", dx, dy)

    def queue_attack(self):
        """Queue an attack action for the next turn."""
        self.pending_action = ("attack",)

    def execute_turn(self, target: "Entity" = None, world_map=None) -> bool:
        """
        Execute the queued action for this turn.

        Args:
            target: Target entity for attack actions
            world_map: Optional WorldMap object for movement validation

        Returns:
            True if an action was executed, False otherwise
        """
        if self.pending_action is None:
            return False

        action_type = self.pending_action[0]

        if action_type == "move":
            _, dx, dy = self.pending_action
            self.move(dx, dy, world_map)
            self.pending_action = None
            return True
        elif action_type == "attack":
            # Warrior attacks in melee range (1 tile)
            if target and self.grid_distance_to(target) <= 1:
                success = self.attack(target)
                self.pending_action = None
                return success
            self.pending_action = None
            return False

        return False

    def draw(self, screen: pygame.Surface):
        """Draw the warrior as a human player character."""
        # Define colors for the human character
        SKIN_COLOR = (255, 220, 177)  # Flesh tone
        ARMOR_COLOR = (70, 130, 180)  # Steel blue armor
        HAIR_COLOR = (101, 67, 33)  # Brown hair
        BOOT_COLOR = (60, 60, 60)  # Dark gray boots
        SWORD_COLOR = (192, 192, 192)  # Silver sword
        SWORD_HANDLE = (139, 69, 19)  # Brown handle

        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2

        # Calculate scaled dimensions based on tile size
        scale = self.size / 50  # Base scale on 50px tiles

        # Draw legs (behind body)
        leg_width = int(6 * scale)
        leg_height = int(14 * scale)
        leg_offset = int(4 * scale)
        # Left leg
        pygame.draw.rect(
            screen,
            ARMOR_COLOR,
            (
                center_x - leg_offset - leg_width,
                center_y + int(6 * scale),
                leg_width,
                leg_height,
            ),
        )
        # Right leg
        pygame.draw.rect(
            screen,
            ARMOR_COLOR,
            (center_x + leg_offset, center_y + int(6 * scale), leg_width, leg_height),
        )

        # Draw boots
        boot_height = int(4 * scale)
        # Left boot
        pygame.draw.rect(
            screen,
            BOOT_COLOR,
            (
                center_x - leg_offset - leg_width,
                center_y + int(6 * scale) + leg_height - boot_height,
                leg_width,
                boot_height,
            ),
        )
        # Right boot
        pygame.draw.rect(
            screen,
            BOOT_COLOR,
            (
                center_x + leg_offset,
                center_y + int(6 * scale) + leg_height - boot_height,
                leg_width,
                boot_height,
            ),
        )

        # Draw body (torso with armor)
        body_width = int(16 * scale)
        body_height = int(18 * scale)
        pygame.draw.rect(
            screen,
            ARMOR_COLOR,
            (
                center_x - body_width // 2,
                center_y - int(4 * scale),
                body_width,
                body_height,
            ),
        )

        # Draw armor detail (chest plate accent)
        pygame.draw.rect(
            screen,
            (100, 150, 200),  # Lighter blue accent
            (
                center_x - body_width // 2 + 2,
                center_y - int(2 * scale),
                body_width - 4,
                int(8 * scale),
            ),
            1,
        )

        # Draw arms
        arm_width = int(5 * scale)
        arm_height = int(16 * scale)
        # Left arm
        pygame.draw.rect(
            screen,
            ARMOR_COLOR,
            (
                center_x - body_width // 2 - arm_width,
                center_y - int(2 * scale),
                arm_width,
                arm_height,
            ),
        )
        # Right arm (holding sword)
        pygame.draw.rect(
            screen,
            ARMOR_COLOR,
            (
                center_x + body_width // 2,
                center_y - int(2 * scale),
                arm_width,
                arm_height,
            ),
        )

        # Draw sword in right hand
        sword_width = int(3 * scale)
        sword_length = int(18 * scale)
        sword_x = center_x + body_width // 2 + arm_width // 2 - sword_width // 2
        sword_y = center_y + int(8 * scale)
        # Sword blade
        pygame.draw.rect(
            screen, SWORD_COLOR, (sword_x, sword_y, sword_width, sword_length)
        )
        # Sword handle
        pygame.draw.rect(
            screen,
            SWORD_HANDLE,
            (sword_x - 1, sword_y - int(4 * scale), sword_width + 2, int(4 * scale)),
        )
        # Sword guard
        pygame.draw.rect(
            screen,
            SWORD_HANDLE,
            (sword_x - int(3 * scale), sword_y - 1, sword_width + int(6 * scale), 2),
        )

        # Draw head
        head_radius = int(8 * scale)
        pygame.draw.circle(
            screen, SKIN_COLOR, (center_x, center_y - int(12 * scale)), head_radius
        )

        # Draw hair
        hair_width = int(12 * scale)
        hair_height = int(6 * scale)
        pygame.draw.ellipse(
            screen,
            HAIR_COLOR,
            (
                center_x - hair_width // 2,
                center_y - int(18 * scale),
                hair_width,
                hair_height,
            ),
        )

        # Draw face details
        eye_radius = int(2 * scale)
        eye_y = center_y - int(13 * scale)
        # Left eye
        pygame.draw.circle(
            screen, (255, 255, 255), (center_x - int(3 * scale), eye_y), eye_radius
        )
        pygame.draw.circle(
            screen, (0, 0, 0), (center_x - int(3 * scale), eye_y), int(1 * scale)
        )
        # Right eye
        pygame.draw.circle(
            screen, (255, 255, 255), (center_x + int(3 * scale), eye_y), eye_radius
        )
        pygame.draw.circle(
            screen, (0, 0, 0), (center_x + int(3 * scale), eye_y), int(1 * scale)
        )

        # Draw smile
        smile_width = int(6 * scale)
        pygame.draw.arc(
            screen,
            (0, 0, 0),
            (
                center_x - smile_width // 2,
                center_y - int(12 * scale),
                smile_width,
                int(6 * scale),
            ),
            3.14,
            2 * 3.14,
            1,
        )

        # Draw health bar on top
        self.draw_health_bar(screen)
