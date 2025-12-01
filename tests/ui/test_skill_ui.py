"""Tests for skill_ui.py - SkillUI class"""

import pytest
from typing import Generator
from unittest.mock import patch
import pygame
from caislean_gaofar.ui.skill_ui import SkillUI
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.core import config


@pytest.fixture(autouse=True)
def setup_pygame() -> Generator[None, None, None]:
    """Setup pygame before each test and cleanup after"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def skill_ui() -> SkillUI:
    """Create a SkillUI instance"""
    return SkillUI()


@pytest.fixture
def warrior() -> Warrior:
    """Create a warrior instance"""
    return Warrior(5, 5)


@pytest.fixture
def screen() -> pygame.Surface:
    """Create a real pygame screen"""
    return pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))


class TestSkillUI:
    """Tests for SkillUI class"""

    def test_skill_ui_initialization(self, skill_ui):
        """Test SkillUI initialization"""
        # Assert
        assert skill_ui.panel_width == 500
        assert skill_ui.panel_height == 520
        assert skill_ui.panel_x == (config.SCREEN_WIDTH - 500) // 2
        assert skill_ui.panel_y == (config.SCREEN_HEIGHT - 520) // 2
        assert skill_ui.selected_skill_id is None
        assert skill_ui.hovered_skill_id is None

    def test_skill_ui_colors(self, skill_ui):
        """Test SkillUI color definitions"""
        # Assert
        assert skill_ui.bg_color == (30, 30, 40)
        assert skill_ui.border_color == (218, 165, 32)
        assert skill_ui.text_color == (255, 248, 220)
        assert skill_ui.locked_color == (100, 100, 100)
        assert skill_ui.learned_color == (50, 200, 50)
        assert skill_ui.available_color == (255, 215, 0)

    def test_draw_basic(self, skill_ui, warrior, screen):
        """Test basic drawing of skill UI"""
        # Act
        skill_ui.draw(screen, warrior)

        # Assert - No errors should occur
        assert skill_ui is not None

    def test_draw_with_skill_points(self, skill_ui, warrior, screen):
        """Test drawing skill UI with available skill points"""
        # Arrange - Give warrior some skill points
        warrior.gain_experience(100)

        # Act
        skill_ui.draw(screen, warrior)

        # Assert - No errors should occur
        assert skill_ui is not None

    def test_draw_with_learned_skills(self, skill_ui, warrior, screen):
        """Test drawing skill UI with learned skills"""
        # Arrange - Learn a skill
        warrior.skills.learn_skill("power_strike")

        # Act
        skill_ui.draw(screen, warrior)

        # Assert - No errors should occur
        assert skill_ui is not None

    @patch("pygame.mouse.get_pos")
    def test_draw_with_hover(self, mock_get_pos, skill_ui, warrior, screen):
        """Test drawing skill UI with mouse hovering over skill"""
        # Arrange - Position mouse over first skill
        skill_x = skill_ui.panel_x + 150
        tier_y = skill_ui.panel_y + 90
        mock_get_pos.return_value = (skill_x + 10, tier_y + 10)

        # Act
        skill_ui.draw(screen, warrior)

        # Assert
        assert skill_ui.hovered_skill_id is not None

    def test_draw_with_active_skill(self, skill_ui, warrior, screen):
        """Test drawing skill UI with active skill set"""
        # Arrange - Learn and set active skill
        warrior.skills.learn_skill("power_strike")
        warrior.skills.set_active_skill("power_strike")

        # Act
        skill_ui.draw(screen, warrior)

        # Assert - No errors should occur
        assert skill_ui is not None

    def test_draw_all_tiers(self, skill_ui, warrior, screen):
        """Test drawing all 5 skill tiers"""
        # Arrange - Level up to access all tiers
        warrior.gain_experience(1000)

        # Act
        skill_ui.draw(screen, warrior)

        # Assert - No errors should occur
        assert skill_ui is not None

    def test_handle_click_learn_skill(self, skill_ui, warrior):
        """Test learning a skill via left-click"""
        # Arrange - Give skill point and level up
        warrior.gain_experience(100)
        assert warrior.experience.get_available_skill_points() > 0

        # Calculate position of first skill (Tier 1)
        skill_x = skill_ui.panel_x + 150
        tier_y = skill_ui.panel_y + 90
        click_pos = (skill_x + 10, tier_y + 10)

        # Act
        result = skill_ui.handle_click(click_pos, warrior, right_click=False)

        # Assert
        assert result is True
        assert len(warrior.skills.learned_skills) > 0

    def test_handle_click_set_active_skill(self, skill_ui, warrior):
        """Test setting active skill via right-click"""
        # Arrange - Learn an active skill first
        warrior.skills.learn_skill("power_strike")

        # Calculate position of power_strike skill (Tier 1)
        skill_x = skill_ui.panel_x + 150
        tier_y = skill_ui.panel_y + 90
        click_pos = (skill_x + 10, tier_y + 10)

        # Act
        result = skill_ui.handle_click(click_pos, warrior, right_click=True)

        # Assert
        assert result is True
        assert warrior.skills.active_skill == "power_strike"

    def test_handle_click_cannot_learn_locked_skill(self, skill_ui, warrior):
        """Test that locked skills cannot be learned"""
        # Arrange - Warrior at level 1, try to learn tier 5 skill
        assert warrior.experience.current_level == 1

        # Give skill point
        warrior.gain_experience(100)

        # Calculate position of tier 5 skill
        skill_x = skill_ui.panel_x + 150
        tier_y = skill_ui.panel_y + 90 + 4 * (60 + 10)  # Tier 5
        click_pos = (skill_x + 10, tier_y + 10)

        # Act
        result = skill_ui.handle_click(click_pos, warrior, right_click=False)

        # Assert
        assert result is False

    def test_handle_click_cannot_learn_without_skill_points(self, skill_ui, warrior):
        """Test that skills cannot be learned without skill points"""
        # Arrange - Level up but set skill points to 0
        warrior.gain_experience(100)
        # Directly set skill points to 0
        warrior.experience.skill_points = 0

        # Calculate position of first skill
        skill_x = skill_ui.panel_x + 150
        tier_y = skill_ui.panel_y + 90
        click_pos = (skill_x + 10, tier_y + 10)

        # Act
        result = skill_ui.handle_click(click_pos, warrior, right_click=False)

        # Assert
        assert result is False

    def test_handle_click_cannot_set_passive_as_active(self, skill_ui, warrior):
        """Test that passive skills cannot be set as active"""
        # Arrange - Learn a passive skill
        warrior.skills.learn_skill("battle_hardened")

        # Find battle_hardened skill position
        skill_x = skill_ui.panel_x + 150 + 160  # Second skill in tier
        tier_y = skill_ui.panel_y + 90
        click_pos = (skill_x + 10, tier_y + 10)

        # Act
        result = skill_ui.handle_click(click_pos, warrior, right_click=True)

        # Assert
        assert result is False

    def test_handle_click_miss(self, skill_ui, warrior):
        """Test clicking outside skill areas returns False"""
        # Arrange - Click far from any skill
        click_pos = (10, 10)

        # Act
        result = skill_ui.handle_click(click_pos, warrior, right_click=False)

        # Assert
        assert result is False

    def test_handle_click_already_learned_skill(self, skill_ui, warrior):
        """Test clicking on already learned skill returns False"""
        # Arrange - Learn a skill
        warrior.gain_experience(100)
        warrior.skills.learn_skill("power_strike")

        # Calculate position of power_strike
        skill_x = skill_ui.panel_x + 150
        tier_y = skill_ui.panel_y + 90
        click_pos = (skill_x + 10, tier_y + 10)

        # Act
        result = skill_ui.handle_click(click_pos, warrior, right_click=False)

        # Assert
        assert result is False

    def test_handle_click_unlearned_skill_right_click(self, skill_ui, warrior):
        """Test right-clicking unlearned skill returns False"""
        # Arrange - Don't learn any skills
        skill_x = skill_ui.panel_x + 150
        tier_y = skill_ui.panel_y + 90
        click_pos = (skill_x + 10, tier_y + 10)

        # Act
        result = skill_ui.handle_click(click_pos, warrior, right_click=True)

        # Assert
        assert result is False

    @patch("pygame.mouse.get_pos")
    def test_draw_skill_details_for_active_skill(
        self, mock_get_pos, skill_ui, warrior, screen
    ):
        """Test drawing skill details for active skill with cooldown"""
        # Arrange - Position mouse over power_strike (active skill)
        skill_x = skill_ui.panel_x + 150
        tier_y = skill_ui.panel_y + 90
        mock_get_pos.return_value = (skill_x + 10, tier_y + 10)

        # Act
        skill_ui.draw(screen, warrior)

        # Assert
        assert skill_ui.hovered_skill_id is not None

    def test_draw_skill_tree_locked_skills(self, skill_ui, warrior, screen):
        """Test that low-level warrior sees locked skills"""
        # Arrange - Level 1 warrior should see locked skills
        assert warrior.experience.current_level == 1

        # Act
        skill_ui.draw(screen, warrior)

        # Assert - No errors should occur
        assert skill_ui is not None

    def test_draw_skill_tree_all_unlocked(self, skill_ui, warrior, screen):
        """Test that high-level warrior sees all unlocked skills"""
        # Arrange - Level up to max
        warrior.gain_experience(1000)

        # Act
        skill_ui.draw(screen, warrior)

        # Assert - No errors should occur
        assert skill_ui is not None

    def test_draw_with_passive_skills(self, skill_ui, warrior, screen):
        """Test drawing with passive skills"""
        # Arrange - Learn passive skill
        warrior.skills.learn_skill("iron_skin")

        # Act
        skill_ui.draw(screen, warrior)

        # Assert - No errors should occur
        assert skill_ui is not None

    def test_draw_with_multiple_skills_learned(self, skill_ui, warrior, screen):
        """Test drawing with multiple skills learned"""
        # Arrange - Learn multiple skills
        warrior.gain_experience(500)
        warrior.skills.learn_skill("power_strike")
        warrior.skills.learn_skill("battle_hardened")
        warrior.skills.learn_skill("shield_bash")

        # Act
        skill_ui.draw(screen, warrior)

        # Assert - No errors should occur
        assert skill_ui is not None

    @patch("pygame.mouse.get_pos")
    def test_draw_hover_on_different_tiers(
        self, mock_get_pos, skill_ui, warrior, screen
    ):
        """Test hovering over skills in different tiers"""
        # Arrange - Level up to unlock tier 2
        warrior.gain_experience(200)

        # Position mouse over tier 2 skill
        skill_x = skill_ui.panel_x + 150
        tier_y = skill_ui.panel_y + 90 + (60 + 10)  # Tier 2
        mock_get_pos.return_value = (skill_x + 10, tier_y + 10)

        # Act
        skill_ui.draw(screen, warrior)

        # Assert
        assert skill_ui.hovered_skill_id is not None

    def test_handle_click_tier_1(self, skill_ui, warrior):
        """Test clicking tier 1 skill"""
        # Arrange
        warrior.gain_experience(1000)
        skill_x = skill_ui.panel_x + 150
        tier_y = skill_ui.panel_y + 90
        click_pos = (skill_x + 10, tier_y + 10)

        # Act
        result = skill_ui.handle_click(click_pos, warrior, right_click=False)

        # Assert
        assert result is True

    def test_handle_click_tier_2(self, skill_ui, warrior):
        """Test clicking tier 2 skill"""
        # Arrange
        warrior.gain_experience(1000)
        skill_x = skill_ui.panel_x + 150
        tier_y = skill_ui.panel_y + 90 + 70
        click_pos = (skill_x + 10, tier_y + 10)

        # Act
        result = skill_ui.handle_click(click_pos, warrior, right_click=False)

        # Assert
        assert result is True

    def test_handle_click_tier_3(self, skill_ui, warrior):
        """Test clicking tier 3 skill"""
        # Arrange
        warrior.gain_experience(1000)
        skill_x = skill_ui.panel_x + 150
        tier_y = skill_ui.panel_y + 90 + 140
        click_pos = (skill_x + 10, tier_y + 10)

        # Act
        result = skill_ui.handle_click(click_pos, warrior, right_click=False)

        # Assert
        assert result is True

    def test_draw_skill_without_skill_points(self, skill_ui, warrior, screen):
        """Test drawing skills when no skill points available (border color)"""
        # Arrange - Level up but set skill points to 0
        warrior.gain_experience(100)
        warrior.experience.skill_points = 0

        # Act
        skill_ui.draw(screen, warrior)

        # Assert - No errors should occur (tests line 139)
        assert warrior.experience.get_available_skill_points() == 0

    @patch("pygame.mouse.get_pos")
    def test_draw_skill_details_for_passive_skill(
        self, mock_get_pos, skill_ui, warrior, screen
    ):
        """Test drawing skill details for passive skill (no cooldown)"""
        # Arrange - Position mouse over battle_hardened (passive skill)
        skill_x = skill_ui.panel_x + 150 + 160  # Second skill in tier 1
        tier_y = skill_ui.panel_y + 90
        mock_get_pos.return_value = (skill_x + 10, tier_y + 10)

        # Act
        skill_ui.draw(screen, warrior)

        # Assert - Should show skill details without cooldown (tests line 228->exit)
        assert skill_ui.hovered_skill_id is not None

    def test_draw_skill_details_word_wrap(self, skill_ui, screen):
        """Test skill details with word wrapping for long descriptions"""
        from caislean_gaofar.systems.skills import Skill, SkillType

        # Arrange - Create a skill with very long description to force wrapping
        long_description = (
            "This is a very long skill description that contains many words and will "
            "definitely need to be wrapped across multiple lines when displayed in the "
            "skill panel because it exceeds the available width for text rendering"
        )
        test_skill = Skill(
            name="Test Skill",
            description=long_description,
            tier=1,
            skill_type=SkillType.PASSIVE,
            icon_color=(255, 0, 0),
        )

        # Act - Call _draw_skill_details directly to test word wrapping
        skill_ui._draw_skill_details(screen, test_skill)

        # Assert - Should handle word wrapping without errors (tests lines 218-219)
        assert test_skill.description == long_description

    def test_draw_skill_details_empty_description(self, skill_ui, screen):
        """Test skill details with empty description"""
        from caislean_gaofar.systems.skills import Skill, SkillType

        # Arrange - Create a skill with empty description
        test_skill = Skill(
            name="Empty Skill",
            description="",
            tier=1,
            skill_type=SkillType.PASSIVE,
            icon_color=(255, 0, 0),
        )

        # Act - Call _draw_skill_details directly
        skill_ui._draw_skill_details(screen, test_skill)

        # Assert - Should handle empty description without errors (tests branch 220->223)
        assert test_skill.description == ""
