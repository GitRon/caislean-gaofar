"""Skills system for warrior abilities and progression."""

import pygame
from typing import Optional, Callable
from enum import Enum


class SkillType(Enum):
    """Types of skills."""

    ACTIVE = "active"
    PASSIVE = "passive"


class Skill:
    """Represents a warrior skill."""

    def __init__(
        self,
        name: str,
        description: str,
        tier: int,
        skill_type: SkillType,
        cooldown: float = 0,
        icon_color: tuple = (255, 255, 255),
    ):
        """
        Initialize a skill.

        Args:
            name: Skill name
            description: Skill description
            tier: Level requirement (1-5)
            skill_type: Type of skill (active or passive)
            cooldown: Cooldown in seconds (for active skills)
            icon_color: Color for skill icon
        """
        self.name = name
        self.description = description
        self.tier = tier
        self.skill_type = skill_type
        self.cooldown = cooldown
        self.icon_color = icon_color
        self.last_used_time = 0  # Time when skill was last used

    def can_use(self) -> bool:
        """Check if skill is ready to use (cooldown expired)."""
        if self.skill_type == SkillType.PASSIVE:
            return True
        current_time = pygame.time.get_ticks()
        return (current_time - self.last_used_time) >= (self.cooldown * 1000)

    def use(self):
        """Mark skill as used (start cooldown)."""
        self.last_used_time = pygame.time.get_ticks()

    def get_remaining_cooldown(self) -> float:
        """Get remaining cooldown in seconds."""
        if self.skill_type == SkillType.PASSIVE:
            return 0
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_used_time) / 1000
        remaining = self.cooldown - elapsed
        return max(0, remaining)


# Define all warrior skills for tiers 1-5
WARRIOR_SKILLS = {
    # Tier 1 - Level 2 skills
    "power_strike": Skill(
        name="Power Strike",
        description="Deliver a mighty blow that deals 150% weapon damage",
        tier=1,
        skill_type=SkillType.ACTIVE,
        cooldown=6,
        icon_color=(255, 100, 100),
    ),
    "battle_hardened": Skill(
        name="Battle Hardened",
        description="+10% critical hit chance when health exceeds 75%",
        tier=1,
        skill_type=SkillType.PASSIVE,
        icon_color=(100, 255, 100),
    ),
    # Tier 2 - Level 3 skills
    "shield_bash": Skill(
        name="Shield Bash",
        description="Bash enemy stunning them for 1 turn, dealing 75% damage",
        tier=2,
        skill_type=SkillType.ACTIVE,
        cooldown=10,
        icon_color=(150, 150, 255),
    ),
    "iron_skin": Skill(
        name="Iron Skin",
        description="Reduce all incoming damage by 10%",
        tier=2,
        skill_type=SkillType.PASSIVE,
        icon_color=(180, 180, 180),
    ),
    # Tier 3 - Level 4 skills
    "whirlwind": Skill(
        name="Whirlwind",
        description="Spin attack hitting all adjacent enemies for 100% damage",
        tier=3,
        skill_type=SkillType.ACTIVE,
        cooldown=15,
        icon_color=(255, 200, 50),
    ),
    "vampiric_strikes": Skill(
        name="Vampiric Strikes",
        description="Heal for 15% of damage dealt",
        tier=3,
        skill_type=SkillType.PASSIVE,
        icon_color=(200, 50, 200),
    ),
    # Tier 4 - Level 5 skills
    "cleave": Skill(
        name="Cleave",
        description="Powerful strike dealing 200% damage with extended range",
        tier=4,
        skill_type=SkillType.ACTIVE,
        cooldown=20,
        icon_color=(255, 150, 0),
    ),
    "berserker_rage": Skill(
        name="Berserker Rage",
        description="+25% attack damage when below 50% health",
        tier=4,
        skill_type=SkillType.PASSIVE,
        icon_color=(200, 0, 0),
    ),
    # Tier 5 - Max level skills
    "earthsplitter": Skill(
        name="Earthsplitter",
        description="Smash the ground creating a shockwave, hitting all enemies in range for 250% damage",
        tier=5,
        skill_type=SkillType.ACTIVE,
        cooldown=25,
        icon_color=(139, 69, 19),
    ),
    "last_stand": Skill(
        name="Last Stand",
        description="When reduced below 20% health, gain a shield for 30% max HP (once per battle)",
        tier=5,
        skill_type=SkillType.PASSIVE,
        icon_color=(255, 215, 0),
    ),
}


class SkillManager:
    """Manages learned and active skills for a warrior."""

    def __init__(self):
        """Initialize the skill manager."""
        self.learned_skills = {}  # skill_id -> Skill
        self.active_skill = None  # Currently selected active skill (replaces attack)
        self.last_stand_used = False  # Track if Last Stand was triggered this battle

    def learn_skill(self, skill_id: str) -> bool:
        """
        Learn a new skill.

        Args:
            skill_id: ID of skill to learn

        Returns:
            True if learned successfully, False if already known or invalid
        """
        if skill_id in self.learned_skills:
            return False
        if skill_id not in WARRIOR_SKILLS:
            return False

        self.learned_skills[skill_id] = WARRIOR_SKILLS[skill_id]
        return True

    def set_active_skill(self, skill_id: Optional[str]) -> bool:
        """
        Set the active skill (replaces basic attack).

        Args:
            skill_id: ID of skill to set as active, or None for basic attack

        Returns:
            True if successful, False if skill not learned or not active type
        """
        if skill_id is None:
            self.active_skill = None
            return True

        if skill_id not in self.learned_skills:
            return False

        skill = self.learned_skills[skill_id]
        if skill.skill_type != SkillType.ACTIVE:
            return False

        self.active_skill = skill_id
        return True

    def get_active_skill(self) -> Optional[Skill]:
        """Get the currently active skill."""
        if self.active_skill is None:
            return None
        return self.learned_skills.get(self.active_skill)

    def can_use_active_skill(self) -> bool:
        """Check if active skill can be used (is off cooldown)."""
        if self.active_skill is None:
            return False
        skill = self.get_active_skill()
        return skill.can_use() if skill else False

    def use_active_skill(self):
        """Use the active skill (start cooldown)."""
        skill = self.get_active_skill()
        if skill:
            skill.use()

    def has_passive_skill(self, skill_id: str) -> bool:
        """Check if a passive skill is learned."""
        return skill_id in self.learned_skills

    def get_learned_skills_by_tier(self, tier: int) -> list:
        """Get all learned skills for a specific tier."""
        return [
            (skill_id, skill)
            for skill_id, skill in self.learned_skills.items()
            if skill.tier == tier
        ]

    def get_available_skills_for_tier(self, tier: int) -> list:
        """Get all available skills for a tier (learned and unlearned)."""
        return [
            (skill_id, skill)
            for skill_id, skill in WARRIOR_SKILLS.items()
            if skill.tier == tier
        ]

    def reset_battle_state(self):
        """Reset battle-specific skill states (e.g., Last Stand)."""
        self.last_stand_used = False
