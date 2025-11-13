"""Tests for CatSi monster class"""

from caislean_gaofar.entities.monsters.cat_si import CatSi
from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class TestCatSi:
    """Tests for CatSi monster"""

    def test_cat_si_initialization(self):
        """Test CatSi can be initialized"""
        # Arrange & Act
        cat_si = CatSi(5, 3)

        # Assert
        assert cat_si.grid_x == 5
        assert cat_si.grid_y == 3
        assert isinstance(cat_si, BaseMonster)

    def test_cat_si_has_required_attributes(self):
        """Test CatSi has all required class attributes"""
        # Assert
        assert hasattr(CatSi, "HEALTH")
        assert hasattr(CatSi, "ATTACK_DAMAGE")
        assert hasattr(CatSi, "SPEED")
        assert hasattr(CatSi, "CHASE_RANGE")
        assert hasattr(CatSi, "ATTACK_RANGE")
        assert hasattr(CatSi, "DESCRIPTION")
        assert hasattr(CatSi, "MONSTER_TYPE")

    def test_cat_si_stats_are_positive(self):
        """Test CatSi stats are positive values"""
        # Arrange & Act
        cat_si = CatSi(5, 5)

        # Assert
        assert cat_si.max_health > 0
        assert cat_si.attack_damage > 0
        assert cat_si.speed > 0
        assert cat_si.chase_range > 0
        assert cat_si.attack_range > 0

    def test_cat_si_has_description(self):
        """Test CatSi has a non-empty description"""
        # Arrange & Act
        cat_si = CatSi(5, 5)

        # Assert
        assert isinstance(cat_si.description, str)
        assert len(cat_si.description) > 0

    def test_cat_si_has_monster_type(self):
        """Test CatSi has a non-empty monster_type"""
        # Arrange & Act
        cat_si = CatSi(5, 5)

        # Assert
        assert isinstance(cat_si.monster_type, str)
        assert len(cat_si.monster_type) > 0
        assert cat_si.monster_type == "cat_si"

    def test_cat_si_initializes_alive(self):
        """Test CatSi initializes as alive"""
        # Arrange & Act
        cat_si = CatSi(5, 5)

        # Assert
        assert cat_si.is_alive is True
        assert cat_si.health == cat_si.max_health
