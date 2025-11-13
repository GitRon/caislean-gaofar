"""Warrior class - player controlled character."""

import pygame
from caislean_gaofar.entities.entity import Entity
from caislean_gaofar.systems.inventory import Inventory
from caislean_gaofar.objects.item import ItemType
from caislean_gaofar.systems.experience import ExperienceSystem
from caislean_gaofar.systems.skills import SkillManager
from caislean_gaofar.core import config


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
        self.experience = ExperienceSystem()  # Experience and leveling system
        self.skills = SkillManager()  # Skill management

    def get_effective_attack_damage(self) -> int:
        """Get total attack damage including inventory and skill bonuses."""
        base_damage = self.base_attack_damage + self.inventory.get_total_attack_bonus()

        # Apply Berserker Rage passive (Tier 4): +25% attack when below 50% health
        if self.skills.has_passive_skill("berserker_rage"):
            if self.health < self.max_health * 0.5:
                base_damage = int(base_damage * 1.25)

        return base_damage

    def get_crit_chance(self) -> float:
        """
        Get critical hit chance.

        Returns:
            Crit chance from 0.0 to 1.0
        """
        crit_chance = 0.0

        # Battle Hardened passive (Tier 1): +10% crit when health > 75%
        if self.skills.has_passive_skill("battle_hardened"):
            if self.health > self.max_health * 0.75:
                crit_chance += 0.10

        return crit_chance

    def get_damage_reduction(self) -> float:
        """
        Get damage reduction percentage.

        Returns:
            Damage reduction from 0.0 to 1.0
        """
        reduction = 0.0

        # Iron Skin passive (Tier 2): 10% damage reduction
        if self.skills.has_passive_skill("iron_skin"):
            reduction += 0.10

        return min(reduction, 0.75)  # Cap at 75% reduction

    def gain_experience(self, xp_amount: int) -> bool:
        """
        Gain experience points and apply level up bonuses.

        Args:
            xp_amount: Amount of XP to gain

        Returns:
            True if leveled up, False otherwise
        """
        old_level = self.experience.current_level
        leveled_up = self.experience.add_xp(xp_amount)

        # Apply HP bonus for each level gained
        if leveled_up:
            new_level = self.experience.current_level
            levels_gained = new_level - old_level

            # Increase max health and restore full health
            hp_bonus = config.WARRIOR_HP_PER_LEVEL * levels_gained
            self.max_health += hp_bonus
            self.health = self.max_health  # Restore to full health on level up

        return leveled_up

    def get_effective_defense(self) -> int:
        """Get total defense including inventory bonuses."""
        return self.inventory.get_total_defense_bonus()

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
            ):
                # Use the potion - heals 30 HP
                heal_amount = 30
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

    def take_damage(self, damage: int):
        """
        Take damage with skill-based modifications.

        Args:
            damage: Incoming damage amount
        """
        # Apply damage reduction from passives
        reduction = self.get_damage_reduction()
        actual_damage = int(damage * (1.0 - reduction))

        # Get defense from equipment
        defense = self.get_effective_defense()

        # Call parent take_damage with defense
        super().take_damage(actual_damage, defense)

        # Check for Last Stand passive (Tier 5)
        if (
            self.skills.has_passive_skill("last_stand")
            and not self.skills.last_stand_used
        ):
            if self.health > 0 and self.health <= self.max_health * 0.2:
                # Grant emergency shield (30% max HP)
                shield_amount = int(self.max_health * 0.3)
                self.health = min(self.max_health, self.health + shield_amount)
                self.skills.last_stand_used = True

    def attack(self, target: "Entity", use_skill: bool = False) -> dict:
        """
        Attempt to attack a target with effective damage.

        Args:
            target: Target entity
            use_skill: If True, use active skill instead of basic attack

        Returns:
            Dictionary with attack results:
            - success: bool - if attack occurred
            - damage: int - damage dealt
            - crit: bool - if it was a critical hit
            - skill_used: str or None - name of skill used
            - healed: int - amount healed (vampiric strikes)
        """
        result = {
            "success": False,
            "damage": 0,
            "crit": False,
            "skill_used": None,
            "healed": 0,
        }

        if not self.can_attack():
            return result

        # Determine if using a skill
        active_skill = None
        damage_multiplier = 1.0

        if use_skill and self.skills.active_skill:
            active_skill = self.skills.get_active_skill()
            if active_skill and active_skill.can_use():
                result["skill_used"] = active_skill.name
                active_skill.use()

                # Apply skill damage multipliers
                if active_skill.name == "Power Strike":
                    damage_multiplier = 1.5
                elif active_skill.name == "Shield Bash":
                    damage_multiplier = 0.75
                    # TODO: Apply stun effect to target
                elif active_skill.name == "Whirlwind":
                    damage_multiplier = 1.0
                    # TODO: Hit all adjacent enemies
                elif active_skill.name == "Cleave":
                    damage_multiplier = 2.0
                    # TODO: Extended range
                elif active_skill.name == "Earthsplitter":
                    damage_multiplier = 2.5
                    # TODO: AOE shockwave
            else:
                # Skill on cooldown, use basic attack
                use_skill = False

        # Calculate base damage
        base_damage = self.get_effective_attack_damage()
        damage = int(base_damage * damage_multiplier)

        # Check for critical hit
        import random

        crit_chance = self.get_crit_chance()
        if random.random() < crit_chance:
            damage = int(damage * 1.5)  # Crits deal 150% damage
            result["crit"] = True

        # Deal damage
        target.take_damage(damage)
        result["damage"] = damage
        result["success"] = True

        # Vampiric Strikes passive (Tier 3): Heal for 15% of damage dealt
        if self.skills.has_passive_skill("vampiric_strikes"):
            heal_amount = int(damage * 0.15)
            self.health = min(self.max_health, self.health + heal_amount)
            result["healed"] = heal_amount

        self.turns_since_last_attack = 0
        return result

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

    def execute_turn(
        self, target: "Entity" = None, world_map=None, use_skill: bool = False
    ) -> dict:
        """
        Execute the queued action for this turn.

        Args:
            target: Target entity for attack actions
            world_map: Optional WorldMap object for movement validation
            use_skill: If True, use active skill for attack

        Returns:
            Dictionary with execution results (same as attack method for attacks,
            or {'success': bool} for other actions)
        """
        if self.pending_action is None:
            return {"success": False}

        action_type = self.pending_action[0]

        if action_type == "move":
            _, dx, dy = self.pending_action
            success = self.move(dx, dy, world_map)
            self.pending_action = None
            return {"success": success}
        elif action_type == "attack":
            # Warrior attacks in melee range (1 tile)
            if target and self.grid_distance_to(target) <= 1:
                result = self.attack(target, use_skill)
                self.pending_action = None
                return result
            self.pending_action = None
            return {"success": False}

        return {"success": False}

    def draw(
        self,
        screen: pygame.Surface,
        camera_offset_x: int = 0,
        camera_offset_y: int = 0,
    ):
        """
        Draw the warrior as a human player character.

        Args:
            screen: The pygame screen surface
            camera_offset_x: Camera offset in grid coordinates (default 0)
            camera_offset_y: Camera offset in grid coordinates (default 0)
        """
        # Define colors for the human character
        SKIN_COLOR = (255, 220, 177)  # Flesh tone
        ARMOR_COLOR = (70, 130, 180)  # Steel blue armor
        HAIR_COLOR = (101, 67, 33)  # Brown hair
        BOOT_COLOR = (60, 60, 60)  # Dark gray boots
        SWORD_COLOR = (192, 192, 192)  # Silver sword
        SWORD_HANDLE = (139, 69, 19)  # Brown handle

        # Calculate screen coordinates with camera offset
        screen_x = self.get_screen_x(camera_offset_x)
        screen_y = self.get_screen_y(camera_offset_y)

        center_x = screen_x + self.size // 2
        center_y = screen_y + self.size // 2

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
        self.draw_health_bar(screen, camera_offset_x, camera_offset_y)
