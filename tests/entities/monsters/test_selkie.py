"""Tests for Selkie monster class"""

import pygame
import pytest

from caislean_gaofar.entities.monsters.selkie import Selkie
from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class TestSelkie:
    """Tests for Selkie monster"""

    @pytest.fixture(autouse=True)
    def setup_pygame(self):
        """Initialize pygame before each test."""
        pygame.init()
        pygame.display.set_mode((800, 600))
        yield
        pygame.quit()

    def test_selkie_initialization(self):
        """Test Selkie can be initialized"""
        # Arrange & Act
        selkie = Selkie(5, 3)

        # Assert
        assert selkie.grid_x == 5
        assert selkie.grid_y == 3
        assert isinstance(selkie, BaseMonster)

    def test_selkie_has_required_attributes(self):
        """Test Selkie has all required class attributes"""
        # Assert
        assert hasattr(Selkie, "HEALTH")
        assert hasattr(Selkie, "ATTACK_DAMAGE")
        assert hasattr(Selkie, "SPEED")
        assert hasattr(Selkie, "CHASE_RANGE")
        assert hasattr(Selkie, "ATTACK_RANGE")
        assert hasattr(Selkie, "DESCRIPTION")
        assert hasattr(Selkie, "MONSTER_TYPE")

    def test_selkie_stats_are_positive(self):
        """Test Selkie stats are positive values"""
        # Arrange & Act
        selkie = Selkie(5, 5)

        # Assert
        assert selkie.max_health > 0
        assert selkie.attack_damage > 0
        assert selkie.speed > 0
        assert selkie.chase_range > 0
        assert selkie.attack_range > 0

    def test_selkie_has_description(self):
        """Test Selkie has a non-empty description"""
        # Arrange & Act
        selkie = Selkie(5, 5)

        # Assert
        assert isinstance(selkie.description, str)
        assert len(selkie.description) > 0

    def test_selkie_has_monster_type(self):
        """Test Selkie has a non-empty monster_type"""
        # Arrange & Act
        selkie = Selkie(5, 5)

        # Assert
        assert isinstance(selkie.monster_type, str)
        assert len(selkie.monster_type) > 0
        assert selkie.monster_type == "selkie"

    def test_selkie_initializes_alive(self):
        """Test Selkie initializes as alive"""
        # Arrange & Act
        selkie = Selkie(5, 5)

        # Assert
        assert selkie.is_alive is True
        assert selkie.health == selkie.max_health

    def test_selkie_draw_body(self):
        """Test Selkie draw_body renders without error"""
        # Arrange
        selkie = Selkie(5, 5)
        screen = pygame.display.get_surface()

        # Act & Assert - should not raise exception
        selkie.draw_body(screen, 400, 300)

    def test_selkie_draw_details(self):
        """Test Selkie draw_details renders without error"""
        # Arrange
        selkie = Selkie(5, 5)
        screen = pygame.display.get_surface()

        # Act & Assert - should not raise exception
        selkie.draw_details(screen, 400, 300)
