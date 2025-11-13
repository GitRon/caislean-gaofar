"""Tests for experience.py - Experience system"""

from caislean_gaofar.systems.experience import ExperienceSystem


class TestExperienceSystem:
    """Tests for ExperienceSystem class"""

    def test_initialization(self):
        """Test ExperienceSystem initialization"""
        # Arrange & Act
        exp_system = ExperienceSystem()

        # Assert
        assert exp_system.current_xp == 0
        assert exp_system.current_level == 1
        assert exp_system.skill_points == 0
        assert exp_system.spent_skill_points == 0

    def test_add_xp_no_level_up(self):
        """Test adding XP without leveling up"""
        # Arrange
        exp_system = ExperienceSystem()

        # Act
        leveled_up = exp_system.add_xp(50)

        # Assert
        assert leveled_up is False
        assert exp_system.current_xp == 50
        assert exp_system.current_level == 1
        assert exp_system.skill_points == 0

    def test_add_xp_single_level_up(self):
        """Test adding XP that causes one level up"""
        # Arrange
        exp_system = ExperienceSystem()

        # Act
        leveled_up = exp_system.add_xp(100)

        # Assert
        assert leveled_up is True
        assert exp_system.current_xp == 100
        assert exp_system.current_level == 2
        assert exp_system.skill_points == 1

    def test_add_xp_multiple_level_ups(self):
        """Test adding XP that causes multiple level ups"""
        # Arrange
        exp_system = ExperienceSystem()

        # Act
        leveled_up = exp_system.add_xp(500)

        # Assert
        assert leveled_up is True
        assert exp_system.current_xp == 500
        assert exp_system.current_level == 4
        assert exp_system.skill_points == 3  # Level 2, 3, 4

    def test_add_xp_reach_max_level(self):
        """Test adding XP to reach max level"""
        # Arrange
        exp_system = ExperienceSystem()

        # Act
        leveled_up = exp_system.add_xp(1000)

        # Assert
        assert leveled_up is True
        assert exp_system.current_xp == 1000
        assert exp_system.current_level == 5  # Max level
        assert exp_system.skill_points == 4  # Levels 2, 3, 4, 5

    def test_add_xp_beyond_max_level(self):
        """Test adding XP when already at max level"""
        # Arrange
        exp_system = ExperienceSystem()
        exp_system.add_xp(1000)  # Reach max level

        # Act
        leveled_up = exp_system.add_xp(500)  # Try to gain more XP

        # Assert
        assert leveled_up is False
        assert exp_system.current_level == 5  # Still max level
        # XP doesn't accumulate beyond max level
        assert exp_system.current_xp == 1000

    def test_get_xp_for_next_level(self):
        """Test getting XP required for next level"""
        # Arrange
        exp_system = ExperienceSystem()

        # Act & Assert
        assert exp_system.get_xp_for_next_level() == 100  # Level 1 -> 2

        exp_system.add_xp(100)
        assert exp_system.get_xp_for_next_level() == 250  # Level 2 -> 3

        exp_system.add_xp(150)
        assert exp_system.get_xp_for_next_level() == 500  # Level 3 -> 4

    def test_get_xp_for_next_level_at_max(self):
        """Test getting XP for next level when at max level"""
        # Arrange
        exp_system = ExperienceSystem()
        exp_system.add_xp(1000)  # Max level

        # Act
        next_level_xp = exp_system.get_xp_for_next_level()

        # Assert
        assert next_level_xp == 0

    def test_get_xp_progress(self):
        """Test XP progress calculation"""
        # Arrange
        exp_system = ExperienceSystem()

        # Act & Assert
        assert exp_system.get_xp_progress() == 0.0  # 0/100

        exp_system.add_xp(50)
        assert exp_system.get_xp_progress() == 0.5  # 50/100

        exp_system.add_xp(50)  # Now at level 2 with 100 XP
        assert exp_system.get_xp_progress() == 0.0  # 0/150 in current level

        exp_system.add_xp(75)  # 175 total, 75 in level 2
        assert exp_system.get_xp_progress() == 0.5  # 75/150

    def test_get_xp_progress_at_max_level(self):
        """Test XP progress at max level"""
        # Arrange
        exp_system = ExperienceSystem()
        exp_system.add_xp(1000)  # Max level

        # Act
        progress = exp_system.get_xp_progress()

        # Assert
        assert progress == 1.0

    def test_spend_skill_point(self):
        """Test spending skill points"""
        # Arrange
        exp_system = ExperienceSystem()
        exp_system.add_xp(250)  # Level 3, 2 skill points

        # Act & Assert
        assert exp_system.get_available_skill_points() == 2
        assert exp_system.spend_skill_point() is True
        assert exp_system.get_available_skill_points() == 1
        assert exp_system.spent_skill_points == 1

    def test_spend_skill_point_none_available(self):
        """Test spending skill point when none available"""
        # Arrange
        exp_system = ExperienceSystem()

        # Act
        result = exp_system.spend_skill_point()

        # Assert
        assert result is False
        assert exp_system.spent_skill_points == 0

    def test_is_max_level(self):
        """Test max level check"""
        # Arrange
        exp_system = ExperienceSystem()

        # Act & Assert
        assert exp_system.is_max_level() is False

        exp_system.add_xp(1000)
        assert exp_system.is_max_level() is True

    def test_get_current_level(self):
        """Test getting current level"""
        # Arrange
        exp_system = ExperienceSystem()

        # Act & Assert
        assert exp_system.get_current_level() == 1

        exp_system.add_xp(250)
        assert exp_system.get_current_level() == 3

    def test_get_current_xp(self):
        """Test getting current XP"""
        # Arrange
        exp_system = ExperienceSystem()

        # Act & Assert
        assert exp_system.get_current_xp() == 0

        exp_system.add_xp(175)
        assert exp_system.get_current_xp() == 175
