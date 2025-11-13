"""Tests for Leprechaun monster class"""

from caislean_gaofar.entities.monsters.leprechaun import Leprechaun
from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class TestLeprechaun:
    """Tests for Leprechaun monster"""

    def test_leprechaun_initialization(self):
        """Test Leprechaun can be initialized"""
        # Arrange & Act
        leprechaun = Leprechaun(5, 3)

        # Assert
        assert leprechaun.grid_x == 5
        assert leprechaun.grid_y == 3
        assert isinstance(leprechaun, BaseMonster)

    def test_leprechaun_has_required_attributes(self):
        """Test Leprechaun has all required class attributes"""
        # Assert
        assert hasattr(Leprechaun, "HEALTH")
        assert hasattr(Leprechaun, "ATTACK_DAMAGE")
        assert hasattr(Leprechaun, "SPEED")
        assert hasattr(Leprechaun, "CHASE_RANGE")
        assert hasattr(Leprechaun, "ATTACK_RANGE")
        assert hasattr(Leprechaun, "DESCRIPTION")
        assert hasattr(Leprechaun, "MONSTER_TYPE")

    def test_leprechaun_stats_are_positive(self):
        """Test Leprechaun stats are positive values"""
        # Arrange & Act
        leprechaun = Leprechaun(5, 5)

        # Assert
        assert leprechaun.max_health > 0
        assert leprechaun.attack_damage > 0
        assert leprechaun.speed > 0
        assert leprechaun.chase_range > 0
        assert leprechaun.attack_range > 0

    def test_leprechaun_has_description(self):
        """Test Leprechaun has a non-empty description"""
        # Arrange & Act
        leprechaun = Leprechaun(5, 5)

        # Assert
        assert isinstance(leprechaun.description, str)
        assert len(leprechaun.description) > 0

    def test_leprechaun_has_monster_type(self):
        """Test Leprechaun has a non-empty monster_type"""
        # Arrange & Act
        leprechaun = Leprechaun(5, 5)

        # Assert
        assert isinstance(leprechaun.monster_type, str)
        assert len(leprechaun.monster_type) > 0
        assert leprechaun.monster_type == "leprechaun"

    def test_leprechaun_initializes_alive(self):
        """Test Leprechaun initializes as alive"""
        # Arrange & Act
        leprechaun = Leprechaun(5, 5)

        # Assert
        assert leprechaun.is_alive is True
        assert leprechaun.health == leprechaun.max_health
