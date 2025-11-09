"""Tests for skills.py - Skills system"""

import pytest
from unittest.mock import patch
from skills import Skill, SkillType, SkillManager, WARRIOR_SKILLS


class TestSkill:
    """Tests for Skill class"""

    def test_skill_initialization(self):
        """Test Skill initialization"""
        # Arrange & Act
        skill = Skill(
            name="Test Skill",
            description="Test description",
            tier=1,
            skill_type=SkillType.ACTIVE,
            cooldown=10,
            icon_color=(255, 0, 0),
        )

        # Assert
        assert skill.name == "Test Skill"
        assert skill.description == "Test description"
        assert skill.tier == 1
        assert skill.skill_type == SkillType.ACTIVE
        assert skill.cooldown == 10
        assert skill.icon_color == (255, 0, 0)
        assert skill.last_used_time == 0

    @patch("pygame.time.get_ticks")
    def test_can_use_active_skill_ready(self, mock_get_ticks):
        """Test can_use for active skill that is ready"""
        # Arrange
        mock_get_ticks.return_value = 10000
        skill = Skill(
            name="Test",
            description="Test",
            tier=1,
            skill_type=SkillType.ACTIVE,
            cooldown=5,
        )

        # Act
        can_use = skill.can_use()

        # Assert
        assert can_use is True

    @patch("pygame.time.get_ticks")
    def test_can_use_active_skill_on_cooldown(self, mock_get_ticks):
        """Test can_use for active skill on cooldown"""
        # Arrange
        skill = Skill(
            name="Test",
            description="Test",
            tier=1,
            skill_type=SkillType.ACTIVE,
            cooldown=5,
        )
        mock_get_ticks.return_value = 10000
        skill.use()
        mock_get_ticks.return_value = 12000  # 2 seconds later

        # Act
        can_use = skill.can_use()

        # Assert
        assert can_use is False  # Still on cooldown (need 5 seconds)

    def test_can_use_passive_skill(self):
        """Test can_use for passive skill (always True)"""
        # Arrange
        skill = Skill(
            name="Test",
            description="Test",
            tier=1,
            skill_type=SkillType.PASSIVE,
        )

        # Act
        can_use = skill.can_use()

        # Assert
        assert can_use is True

    @patch("pygame.time.get_ticks")
    def test_use_skill(self, mock_get_ticks):
        """Test using a skill"""
        # Arrange
        mock_get_ticks.return_value = 10000
        skill = Skill(
            name="Test",
            description="Test",
            tier=1,
            skill_type=SkillType.ACTIVE,
            cooldown=5,
        )

        # Act
        skill.use()

        # Assert
        assert skill.last_used_time == 10000

    @patch("pygame.time.get_ticks")
    def test_get_remaining_cooldown(self, mock_get_ticks):
        """Test getting remaining cooldown"""
        # Arrange
        skill = Skill(
            name="Test",
            description="Test",
            tier=1,
            skill_type=SkillType.ACTIVE,
            cooldown=10,
        )
        mock_get_ticks.return_value = 10000
        skill.use()
        mock_get_ticks.return_value = 13000  # 3 seconds later

        # Act
        remaining = skill.get_remaining_cooldown()

        # Assert
        assert remaining == 7.0  # 10 - 3 = 7 seconds

    def test_get_remaining_cooldown_passive(self):
        """Test remaining cooldown for passive skill"""
        # Arrange
        skill = Skill(
            name="Test",
            description="Test",
            tier=1,
            skill_type=SkillType.PASSIVE,
        )

        # Act
        remaining = skill.get_remaining_cooldown()

        # Assert
        assert remaining == 0


class TestSkillManager:
    """Tests for SkillManager class"""

    def test_initialization(self):
        """Test SkillManager initialization"""
        # Arrange & Act
        manager = SkillManager()

        # Assert
        assert manager.learned_skills == {}
        assert manager.active_skill is None
        assert manager.last_stand_used is False

    def test_learn_skill(self):
        """Test learning a skill"""
        # Arrange
        manager = SkillManager()

        # Act
        result = manager.learn_skill("power_strike")

        # Assert
        assert result is True
        assert "power_strike" in manager.learned_skills
        assert manager.learned_skills["power_strike"].name == "Power Strike"

    def test_learn_skill_already_known(self):
        """Test learning a skill that's already known"""
        # Arrange
        manager = SkillManager()
        manager.learn_skill("power_strike")

        # Act
        result = manager.learn_skill("power_strike")

        # Assert
        assert result is False

    def test_learn_skill_invalid(self):
        """Test learning an invalid skill"""
        # Arrange
        manager = SkillManager()

        # Act
        result = manager.learn_skill("invalid_skill")

        # Assert
        assert result is False

    def test_set_active_skill(self):
        """Test setting active skill"""
        # Arrange
        manager = SkillManager()
        manager.learn_skill("power_strike")

        # Act
        result = manager.set_active_skill("power_strike")

        # Assert
        assert result is True
        assert manager.active_skill == "power_strike"

    def test_set_active_skill_none(self):
        """Test clearing active skill"""
        # Arrange
        manager = SkillManager()
        manager.learn_skill("power_strike")
        manager.set_active_skill("power_strike")

        # Act
        result = manager.set_active_skill(None)

        # Assert
        assert result is True
        assert manager.active_skill is None

    def test_set_active_skill_not_learned(self):
        """Test setting active skill that's not learned"""
        # Arrange
        manager = SkillManager()

        # Act
        result = manager.set_active_skill("power_strike")

        # Assert
        assert result is False

    def test_set_active_skill_passive(self):
        """Test setting a passive skill as active (should fail)"""
        # Arrange
        manager = SkillManager()
        manager.learn_skill("battle_hardened")  # Passive skill

        # Act
        result = manager.set_active_skill("battle_hardened")

        # Assert
        assert result is False

    def test_get_active_skill(self):
        """Test getting active skill"""
        # Arrange
        manager = SkillManager()
        manager.learn_skill("power_strike")
        manager.set_active_skill("power_strike")

        # Act
        skill = manager.get_active_skill()

        # Assert
        assert skill is not None
        assert skill.name == "Power Strike"

    def test_get_active_skill_none_set(self):
        """Test getting active skill when none is set"""
        # Arrange
        manager = SkillManager()

        # Act
        skill = manager.get_active_skill()

        # Assert
        assert skill is None

    @patch("pygame.time.get_ticks")
    def test_can_use_active_skill(self, mock_get_ticks):
        """Test checking if active skill can be used"""
        # Arrange
        mock_get_ticks.return_value = 10000
        manager = SkillManager()
        manager.learn_skill("power_strike")
        manager.set_active_skill("power_strike")

        # Act
        can_use = manager.can_use_active_skill()

        # Assert
        assert can_use is True

    def test_can_use_active_skill_none_set(self):
        """Test can_use when no active skill is set"""
        # Arrange
        manager = SkillManager()

        # Act
        can_use = manager.can_use_active_skill()

        # Assert
        assert can_use is False

    @patch("pygame.time.get_ticks")
    def test_use_active_skill(self, mock_get_ticks):
        """Test using active skill"""
        # Arrange
        mock_get_ticks.return_value = 10000
        manager = SkillManager()
        manager.learn_skill("power_strike")
        manager.set_active_skill("power_strike")

        # Act
        manager.use_active_skill()

        # Assert
        skill = manager.get_active_skill()
        assert skill.last_used_time == 10000

    def test_use_active_skill_none_set(self):
        """Test using active skill when none is set"""
        # Arrange
        manager = SkillManager()

        # Act - should not raise error
        manager.use_active_skill()

        # Assert - just verify no exception was raised
        assert manager.active_skill is None

    def test_has_passive_skill(self):
        """Test checking for passive skill"""
        # Arrange
        manager = SkillManager()
        manager.learn_skill("battle_hardened")

        # Act & Assert
        assert manager.has_passive_skill("battle_hardened") is True
        assert manager.has_passive_skill("iron_skin") is False

    def test_get_learned_skills_by_tier(self):
        """Test getting learned skills by tier"""
        # Arrange
        manager = SkillManager()
        manager.learn_skill("power_strike")  # Tier 1
        manager.learn_skill("battle_hardened")  # Tier 1
        manager.learn_skill("shield_bash")  # Tier 2

        # Act
        tier1_skills = manager.get_learned_skills_by_tier(1)
        tier2_skills = manager.get_learned_skills_by_tier(2)
        tier3_skills = manager.get_learned_skills_by_tier(3)

        # Assert
        assert len(tier1_skills) == 2
        assert len(tier2_skills) == 1
        assert len(tier3_skills) == 0

    def test_get_available_skills_for_tier(self):
        """Test getting all available skills for a tier"""
        # Arrange
        manager = SkillManager()

        # Act
        tier1_skills = manager.get_available_skills_for_tier(1)

        # Assert
        assert len(tier1_skills) == 2  # power_strike and battle_hardened

    def test_reset_battle_state(self):
        """Test resetting battle-specific state"""
        # Arrange
        manager = SkillManager()
        manager.last_stand_used = True

        # Act
        manager.reset_battle_state()

        # Assert
        assert manager.last_stand_used is False


class TestWarriorSkills:
    """Tests for WARRIOR_SKILLS definitions"""

    def test_warrior_skills_exist(self):
        """Test that all warrior skills are defined"""
        # Assert - Check each skill explicitly
        assert "power_strike" in WARRIOR_SKILLS
        assert "battle_hardened" in WARRIOR_SKILLS
        assert "shield_bash" in WARRIOR_SKILLS
        assert "iron_skin" in WARRIOR_SKILLS
        assert "whirlwind" in WARRIOR_SKILLS
        assert "vampiric_strikes" in WARRIOR_SKILLS
        assert "cleave" in WARRIOR_SKILLS
        assert "berserker_rage" in WARRIOR_SKILLS
        assert "earthsplitter" in WARRIOR_SKILLS
        assert "last_stand" in WARRIOR_SKILLS

    def test_tier_distribution(self):
        """Test that skills are properly distributed across tiers"""
        # Arrange
        tier_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        # Act
        tier_counts = {
            tier: sum(1 for s in WARRIOR_SKILLS.values() if s.tier == tier)
            for tier in range(1, 6)
        }

        # Assert - Each tier should have 2 skills (1 active, 1 passive)
        assert tier_counts[1] == 2, f"Tier 1 should have 2 skills, has {tier_counts[1]}"
        assert tier_counts[2] == 2, f"Tier 2 should have 2 skills, has {tier_counts[2]}"
        assert tier_counts[3] == 2, f"Tier 3 should have 2 skills, has {tier_counts[3]}"
        assert tier_counts[4] == 2, f"Tier 4 should have 2 skills, has {tier_counts[4]}"
        assert tier_counts[5] == 2, f"Tier 5 should have 2 skills, has {tier_counts[5]}"

    def test_skill_types(self):
        """Test that each tier has one active and one passive"""
        # Helper to count skills by type for a tier
        def count_skills(tier, skill_type):
            return sum(
                1
                for s in WARRIOR_SKILLS.values()
                if s.tier == tier and s.skill_type == skill_type
            )

        # Assert tier 1
        assert count_skills(1, SkillType.ACTIVE) == 1, "Tier 1 should have 1 active skill"
        assert count_skills(1, SkillType.PASSIVE) == 1, "Tier 1 should have 1 passive skill"

        # Assert tier 2
        assert count_skills(2, SkillType.ACTIVE) == 1, "Tier 2 should have 1 active skill"
        assert count_skills(2, SkillType.PASSIVE) == 1, "Tier 2 should have 1 passive skill"

        # Assert tier 3
        assert count_skills(3, SkillType.ACTIVE) == 1, "Tier 3 should have 1 active skill"
        assert count_skills(3, SkillType.PASSIVE) == 1, "Tier 3 should have 1 passive skill"

        # Assert tier 4
        assert count_skills(4, SkillType.ACTIVE) == 1, "Tier 4 should have 1 active skill"
        assert count_skills(4, SkillType.PASSIVE) == 1, "Tier 4 should have 1 passive skill"

        # Assert tier 5
        assert count_skills(5, SkillType.ACTIVE) == 1, "Tier 5 should have 1 active skill"
        assert count_skills(5, SkillType.PASSIVE) == 1, "Tier 5 should have 1 passive skill"

    def test_active_skills_have_cooldowns(self):
        """Test that all active skills have cooldowns"""
        # Get all active skills
        active_skills = {
            skill_id: skill
            for skill_id, skill in WARRIOR_SKILLS.items()
            if skill.skill_type == SkillType.ACTIVE
        }

        # Assert each active skill has a cooldown
        assert active_skills["power_strike"].cooldown > 0
        assert active_skills["shield_bash"].cooldown > 0
        assert active_skills["whirlwind"].cooldown > 0
        assert active_skills["cleave"].cooldown > 0
        assert active_skills["earthsplitter"].cooldown > 0
