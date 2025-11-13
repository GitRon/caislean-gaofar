"""Tests for Clurichaun monster class"""

import pygame
import pytest

from caislean_gaofar.entities.monsters.clurichaun import Clurichaun
from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class TestClurichaun:
    """Tests for Clurichaun monster"""

    @pytest.fixture(autouse=True)
    def setup_pygame(self):
        """Initialize pygame before each test."""
        pygame.init()
        pygame.display.set_mode((800, 600))
        yield
        pygame.quit()

    def test_clurichaun_initialization(self):
        """Test Clurichaun can be initialized"""
        # Arrange & Act
        clurichaun = Clurichaun(5, 3)

        # Assert
        assert clurichaun.grid_x == 5
        assert clurichaun.grid_y == 3
        assert isinstance(clurichaun, BaseMonster)

    def test_clurichaun_has_required_attributes(self):
        """Test Clurichaun has all required class attributes"""
        # Assert
        assert hasattr(Clurichaun, "HEALTH")
        assert hasattr(Clurichaun, "ATTACK_DAMAGE")
        assert hasattr(Clurichaun, "SPEED")
        assert hasattr(Clurichaun, "CHASE_RANGE")
        assert hasattr(Clurichaun, "ATTACK_RANGE")
        assert hasattr(Clurichaun, "DESCRIPTION")
        assert hasattr(Clurichaun, "MONSTER_TYPE")

    def test_clurichaun_stats_are_positive(self):
        """Test Clurichaun stats are positive values"""
        # Arrange & Act
        clurichaun = Clurichaun(5, 5)

        # Assert
        assert clurichaun.max_health > 0
        assert clurichaun.attack_damage > 0
        assert clurichaun.speed > 0
        assert clurichaun.chase_range > 0
        assert clurichaun.attack_range > 0

    def test_clurichaun_has_description(self):
        """Test Clurichaun has a non-empty description"""
        # Arrange & Act
        clurichaun = Clurichaun(5, 5)

        # Assert
        assert isinstance(clurichaun.description, str)
        assert len(clurichaun.description) > 0

    def test_clurichaun_has_monster_type(self):
        """Test Clurichaun has a non-empty monster_type"""
        # Arrange & Act
        clurichaun = Clurichaun(5, 5)

        # Assert
        assert isinstance(clurichaun.monster_type, str)
        assert len(clurichaun.monster_type) > 0
        assert clurichaun.monster_type == "clurichaun"

    def test_clurichaun_initializes_alive(self):
        """Test Clurichaun initializes as alive"""
        # Arrange & Act
        clurichaun = Clurichaun(5, 5)

        # Assert
        assert clurichaun.is_alive is True
        assert clurichaun.health == clurichaun.max_health

    def test_clurichaun_draw_body(self):
        """Test Clurichaun draw_body renders without error"""
        # Arrange
        clurichaun = Clurichaun(5, 5)
        screen = pygame.display.get_surface()

        # Act & Assert - should not raise exception
        clurichaun.draw_body(screen, 400, 300)

    def test_clurichaun_draw_details(self):
        """Test Clurichaun draw_details renders without error"""
        # Arrange
        clurichaun = Clurichaun(5, 5)
        screen = pygame.display.get_surface()

        # Act & Assert - should not raise exception
        clurichaun.draw_details(screen, 400, 300)
