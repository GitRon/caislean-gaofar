"""Tests for Banshee monster class"""

from caislean_gaofar.entities.monsters.banshee import Banshee
from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class TestBanshee:
    """Tests for Banshee monster"""

    def test_banshee_initialization(self):
        """Test Banshee can be initialized"""
        # Arrange & Act
        banshee = Banshee(5, 3)

        # Assert
        assert banshee.grid_x == 5
        assert banshee.grid_y == 3
        assert isinstance(banshee, BaseMonster)

    def test_banshee_has_required_attributes(self):
        """Test Banshee has all required class attributes"""
        # Assert
        assert hasattr(Banshee, "HEALTH")
        assert hasattr(Banshee, "ATTACK_DAMAGE")
        assert hasattr(Banshee, "SPEED")
        assert hasattr(Banshee, "CHASE_RANGE")
        assert hasattr(Banshee, "ATTACK_RANGE")
        assert hasattr(Banshee, "DESCRIPTION")
        assert hasattr(Banshee, "MONSTER_TYPE")

    def test_banshee_stats_are_positive(self):
        """Test Banshee stats are positive values"""
        # Arrange & Act
        banshee = Banshee(5, 5)

        # Assert
        assert banshee.max_health > 0
        assert banshee.attack_damage > 0
        assert banshee.speed > 0
        assert banshee.chase_range > 0
        assert banshee.attack_range > 0

    def test_banshee_has_description(self):
        """Test Banshee has a non-empty description"""
        # Arrange & Act
        banshee = Banshee(5, 5)

        # Assert
        assert isinstance(banshee.description, str)
        assert len(banshee.description) > 0

    def test_banshee_has_monster_type(self):
        """Test Banshee has a non-empty monster_type"""
        # Arrange & Act
        banshee = Banshee(5, 5)

        # Assert
        assert isinstance(banshee.monster_type, str)
        assert len(banshee.monster_type) > 0

    def test_banshee_initializes_alive(self):
        """Test Banshee initializes as alive"""
        # Arrange & Act
        banshee = Banshee(5, 5)

        # Assert
        assert banshee.is_alive is True
        assert banshee.health == banshee.max_health

    def test_banshee_stats(self):
        """Test Banshee has expected stats"""
        # Arrange & Act
        banshee = Banshee(5, 5)

        # Assert
        assert banshee.HEALTH == 60
        assert banshee.ATTACK_DAMAGE == 12
        assert banshee.SPEED == 1
        assert banshee.CHASE_RANGE == 6
        assert banshee.ATTACK_RANGE == 2
        assert banshee.monster_type == "banshee"
