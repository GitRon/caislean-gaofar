"""Tests for Dullahan monster class"""

from monsters.dullahan import Dullahan
from monsters.base_monster import BaseMonster


class TestDullahan:
    """Tests for Dullahan monster"""

    def test_dullahan_initialization(self):
        """Test Dullahan can be initialized"""
        # Arrange & Act
        dullahan = Dullahan(5, 3)

        # Assert
        assert dullahan.grid_x == 5
        assert dullahan.grid_y == 3
        assert isinstance(dullahan, BaseMonster)

    def test_dullahan_has_required_attributes(self):
        """Test Dullahan has all required class attributes"""
        # Assert
        assert hasattr(Dullahan, "HEALTH")
        assert hasattr(Dullahan, "ATTACK_DAMAGE")
        assert hasattr(Dullahan, "SPEED")
        assert hasattr(Dullahan, "CHASE_RANGE")
        assert hasattr(Dullahan, "ATTACK_RANGE")
        assert hasattr(Dullahan, "DESCRIPTION")
        assert hasattr(Dullahan, "MONSTER_TYPE")

    def test_dullahan_stats_are_positive(self):
        """Test Dullahan stats are positive values"""
        # Arrange & Act
        dullahan = Dullahan(5, 5)

        # Assert
        assert dullahan.max_health > 0
        assert dullahan.attack_damage > 0
        assert dullahan.speed > 0
        assert dullahan.chase_range > 0
        assert dullahan.attack_range > 0

    def test_dullahan_has_description(self):
        """Test Dullahan has a non-empty description"""
        # Arrange & Act
        dullahan = Dullahan(5, 5)

        # Assert
        assert isinstance(dullahan.description, str)
        assert len(dullahan.description) > 0

    def test_dullahan_has_monster_type(self):
        """Test Dullahan has a non-empty monster_type"""
        # Arrange & Act
        dullahan = Dullahan(5, 5)

        # Assert
        assert isinstance(dullahan.monster_type, str)
        assert len(dullahan.monster_type) > 0
        assert dullahan.monster_type == "dullahan"

    def test_dullahan_initializes_alive(self):
        """Test Dullahan initializes as alive"""
        # Arrange & Act
        dullahan = Dullahan(5, 5)

        # Assert
        assert dullahan.is_alive is True
        assert dullahan.health == dullahan.max_health
