"""Tests for Pooka monster class"""

import pygame
import pytest

from caislean_gaofar.entities.monsters.pooka import Pooka
from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class TestPooka:
    """Tests for Pooka monster"""

    @pytest.fixture(autouse=True)
    def setup_pygame(self):
        """Initialize pygame before each test."""
        pygame.init()
        pygame.display.set_mode((800, 600))
        yield
        pygame.quit()

    def test_pooka_initialization(self):
        """Test Pooka can be initialized"""
        # Arrange & Act
        pooka = Pooka(5, 3)

        # Assert
        assert pooka.grid_x == 5
        assert pooka.grid_y == 3
        assert isinstance(pooka, BaseMonster)

    def test_pooka_has_required_attributes(self):
        """Test Pooka has all required class attributes"""
        # Assert
        assert hasattr(Pooka, "HEALTH")
        assert hasattr(Pooka, "ATTACK_DAMAGE")
        assert hasattr(Pooka, "SPEED")
        assert hasattr(Pooka, "CHASE_RANGE")
        assert hasattr(Pooka, "ATTACK_RANGE")
        assert hasattr(Pooka, "DESCRIPTION")
        assert hasattr(Pooka, "MONSTER_TYPE")

    def test_pooka_stats_are_positive(self):
        """Test Pooka stats are positive values"""
        # Arrange & Act
        pooka = Pooka(5, 5)

        # Assert
        assert pooka.max_health > 0
        assert pooka.attack_damage > 0
        assert pooka.speed > 0
        assert pooka.chase_range > 0
        assert pooka.attack_range > 0

    def test_pooka_has_description(self):
        """Test Pooka has a non-empty description"""
        # Arrange & Act
        pooka = Pooka(5, 5)

        # Assert
        assert isinstance(pooka.description, str)
        assert len(pooka.description) > 0

    def test_pooka_has_monster_type(self):
        """Test Pooka has a non-empty monster_type"""
        # Arrange & Act
        pooka = Pooka(5, 5)

        # Assert
        assert isinstance(pooka.monster_type, str)
        assert len(pooka.monster_type) > 0
        assert pooka.monster_type == "pooka"

    def test_pooka_initializes_alive(self):
        """Test Pooka initializes as alive"""
        # Arrange & Act
        pooka = Pooka(5, 5)

        # Assert
        assert pooka.is_alive is True
        assert pooka.health == pooka.max_health

    def test_pooka_draw_body(self):
        """Test Pooka draw_body renders without error"""
        # Arrange
        pooka = Pooka(5, 5)
        screen = pygame.display.get_surface()

        # Act & Assert - should not raise exception
        pooka.draw_body(screen, 400, 300)

    def test_pooka_draw_details(self):
        """Test Pooka draw_details renders without error"""
        # Arrange
        pooka = Pooka(5, 5)
        screen = pygame.display.get_surface()

        # Act & Assert - should not raise exception
        pooka.draw_details(screen, 400, 300)
