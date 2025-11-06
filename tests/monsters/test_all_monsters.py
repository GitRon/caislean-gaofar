"""Tests for all specific monster classes"""

import pytest
from monsters.banshee import Banshee
from monsters.cat_si import CatSi
from monsters.changeling import Changeling
from monsters.clurichaun import Clurichaun
from monsters.dullahan import Dullahan
from monsters.fear_gorta import FearGorta
from monsters.leprechaun import Leprechaun
from monsters.merrow import Merrow
from monsters.pooka import Pooka
from monsters.selkie import Selkie
from monsters.base_monster import BaseMonster


# List of all monster classes to test
ALL_MONSTER_CLASSES = [
    Banshee,
    CatSi,
    Changeling,
    Clurichaun,
    Dullahan,
    FearGorta,
    Leprechaun,
    Merrow,
    Pooka,
    Selkie,
]


@pytest.mark.parametrize("monster_class", ALL_MONSTER_CLASSES)
class TestAllMonsters:
    """Parametrized tests that run for all monster classes"""

    def test_monster_initialization(self, monster_class):
        """Test monster can be initialized"""
        # Arrange & Act
        monster = monster_class(5, 3)

        # Assert
        assert monster.grid_x == 5
        assert monster.grid_y == 3
        assert isinstance(monster, BaseMonster)

    def test_monster_has_required_attributes(self, monster_class):
        """Test monster has all required class attributes"""
        # Assert
        assert hasattr(monster_class, "HEALTH")
        assert hasattr(monster_class, "ATTACK_DAMAGE")
        assert hasattr(monster_class, "SPEED")
        assert hasattr(monster_class, "CHASE_RANGE")
        assert hasattr(monster_class, "ATTACK_RANGE")
        assert hasattr(monster_class, "DESCRIPTION")
        assert hasattr(monster_class, "MONSTER_TYPE")

    def test_monster_stats_are_positive(self, monster_class):
        """Test monster stats are positive values"""
        # Arrange & Act
        monster = monster_class(5, 5)

        # Assert
        assert monster.max_health > 0
        assert monster.attack_damage > 0
        assert monster.speed > 0
        assert monster.chase_range > 0
        assert monster.attack_range > 0

    def test_monster_has_description(self, monster_class):
        """Test monster has a non-empty description"""
        # Arrange & Act
        monster = monster_class(5, 5)

        # Assert
        assert isinstance(monster.description, str)
        assert len(monster.description) > 0

    def test_monster_has_monster_type(self, monster_class):
        """Test monster has a non-empty monster_type"""
        # Arrange & Act
        monster = monster_class(5, 5)

        # Assert
        assert isinstance(monster.monster_type, str)
        assert len(monster.monster_type) > 0

    def test_monster_initializes_alive(self, monster_class):
        """Test monster initializes as alive"""
        # Arrange & Act
        monster = monster_class(5, 5)

        # Assert
        assert monster.is_alive is True
        assert monster.health == monster.max_health


class TestBanshee:
    """Specific tests for Banshee"""

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


class TestCatSi:
    """Specific tests for Cat Si"""

    def test_cat_si_initialization(self):
        """Test Cat Si can be initialized"""
        # Arrange & Act
        cat_si = CatSi(5, 5)

        # Assert
        assert cat_si.monster_type == "cat_si"


class TestChangeling:
    """Specific tests for Changeling"""

    def test_changeling_initialization(self):
        """Test Changeling can be initialized"""
        # Arrange & Act
        changeling = Changeling(5, 5)

        # Assert
        assert changeling.monster_type == "changeling"


class TestClurichaun:
    """Specific tests for Clurichaun"""

    def test_clurichaun_initialization(self):
        """Test Clurichaun can be initialized"""
        # Arrange & Act
        clurichaun = Clurichaun(5, 5)

        # Assert
        assert clurichaun.monster_type == "clurichaun"


class TestDullahan:
    """Specific tests for Dullahan"""

    def test_dullahan_initialization(self):
        """Test Dullahan can be initialized"""
        # Arrange & Act
        dullahan = Dullahan(5, 5)

        # Assert
        assert dullahan.monster_type == "dullahan"


class TestFearGorta:
    """Specific tests for Fear Gorta"""

    def test_fear_gorta_initialization(self):
        """Test Fear Gorta can be initialized"""
        # Arrange & Act
        fear_gorta = FearGorta(5, 5)

        # Assert
        assert fear_gorta.monster_type == "fear_gorta"


class TestLeprechaun:
    """Specific tests for Leprechaun"""

    def test_leprechaun_initialization(self):
        """Test Leprechaun can be initialized"""
        # Arrange & Act
        leprechaun = Leprechaun(5, 5)

        # Assert
        assert leprechaun.monster_type == "leprechaun"


class TestMerrow:
    """Specific tests for Merrow"""

    def test_merrow_initialization(self):
        """Test Merrow can be initialized"""
        # Arrange & Act
        merrow = Merrow(5, 5)

        # Assert
        assert merrow.monster_type == "merrow"


class TestPooka:
    """Specific tests for Pooka"""

    def test_pooka_initialization(self):
        """Test Pooka can be initialized"""
        # Arrange & Act
        pooka = Pooka(5, 5)

        # Assert
        assert pooka.monster_type == "pooka"


class TestSelkie:
    """Specific tests for Selkie"""

    def test_selkie_initialization(self):
        """Test Selkie can be initialized"""
        # Arrange & Act
        selkie = Selkie(5, 5)

        # Assert
        assert selkie.monster_type == "selkie"
