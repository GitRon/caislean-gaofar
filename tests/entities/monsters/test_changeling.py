"""Tests for Changeling monster class"""

import pygame
import pytest

from caislean_gaofar.entities.monsters.changeling import Changeling
from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class TestChangeling:
    """Tests for Changeling monster"""

    @pytest.fixture(autouse=True)
    def setup_pygame(self):
        """Initialize pygame before each test."""
        pygame.init()
        pygame.display.set_mode((800, 600))
        yield
        pygame.quit()

    def test_changeling_initialization(self):
        """Test Changeling can be initialized"""
        # Arrange & Act
        changeling = Changeling(5, 3)

        # Assert
        assert changeling.grid_x == 5
        assert changeling.grid_y == 3
        assert isinstance(changeling, BaseMonster)

    def test_changeling_has_required_attributes(self):
        """Test Changeling has all required class attributes"""
        # Assert
        assert hasattr(Changeling, "HEALTH")
        assert hasattr(Changeling, "ATTACK_DAMAGE")
        assert hasattr(Changeling, "SPEED")
        assert hasattr(Changeling, "CHASE_RANGE")
        assert hasattr(Changeling, "ATTACK_RANGE")
        assert hasattr(Changeling, "DESCRIPTION")
        assert hasattr(Changeling, "MONSTER_TYPE")

    def test_changeling_stats_are_positive(self):
        """Test Changeling stats are positive values"""
        # Arrange & Act
        changeling = Changeling(5, 5)

        # Assert
        assert changeling.max_health > 0
        assert changeling.attack_damage > 0
        assert changeling.speed > 0
        assert changeling.chase_range > 0
        assert changeling.attack_range > 0

    def test_changeling_has_description(self):
        """Test Changeling has a non-empty description"""
        # Arrange & Act
        changeling = Changeling(5, 5)

        # Assert
        assert isinstance(changeling.description, str)
        assert len(changeling.description) > 0

    def test_changeling_has_monster_type(self):
        """Test Changeling has a non-empty monster_type"""
        # Arrange & Act
        changeling = Changeling(5, 5)

        # Assert
        assert isinstance(changeling.monster_type, str)
        assert len(changeling.monster_type) > 0
        assert changeling.monster_type == "changeling"

    def test_changeling_initializes_alive(self):
        """Test Changeling initializes as alive"""
        # Arrange & Act
        changeling = Changeling(5, 5)

        # Assert
        assert changeling.is_alive is True
        assert changeling.health == changeling.max_health

    def test_changeling_draw_body(self):
        """Test Changeling draw_body renders without error"""
        # Arrange
        changeling = Changeling(5, 5)
        screen = pygame.display.get_surface()

        # Act & Assert - should not raise exception
        changeling.draw_body(screen, 400, 300)

    def test_changeling_draw_details(self):
        """Test Changeling draw_details renders without error"""
        # Arrange
        changeling = Changeling(5, 5)
        screen = pygame.display.get_surface()

        # Act & Assert - should not raise exception
        changeling.draw_details(screen, 400, 300)
