"""Tests for FearGorta monster class"""

import pygame
import pytest

from monsters.fear_gorta import FearGorta
from monsters.base_monster import BaseMonster


class TestFearGorta:
    """Tests for FearGorta monster"""

    @pytest.fixture(autouse=True)
    def setup_pygame(self):
        """Initialize pygame before each test."""
        pygame.init()
        pygame.display.set_mode((800, 600))
        yield
        pygame.quit()

    def test_fear_gorta_initialization(self):
        """Test FearGorta can be initialized"""
        # Arrange & Act
        fear_gorta = FearGorta(5, 3)

        # Assert
        assert fear_gorta.grid_x == 5
        assert fear_gorta.grid_y == 3
        assert isinstance(fear_gorta, BaseMonster)

    def test_fear_gorta_has_required_attributes(self):
        """Test FearGorta has all required class attributes"""
        # Assert
        assert hasattr(FearGorta, "HEALTH")
        assert hasattr(FearGorta, "ATTACK_DAMAGE")
        assert hasattr(FearGorta, "SPEED")
        assert hasattr(FearGorta, "CHASE_RANGE")
        assert hasattr(FearGorta, "ATTACK_RANGE")
        assert hasattr(FearGorta, "DESCRIPTION")
        assert hasattr(FearGorta, "MONSTER_TYPE")

    def test_fear_gorta_stats_are_positive(self):
        """Test FearGorta stats are positive values"""
        # Arrange & Act
        fear_gorta = FearGorta(5, 5)

        # Assert
        assert fear_gorta.max_health > 0
        assert fear_gorta.attack_damage > 0
        assert fear_gorta.speed > 0
        assert fear_gorta.chase_range > 0
        assert fear_gorta.attack_range > 0

    def test_fear_gorta_has_description(self):
        """Test FearGorta has a non-empty description"""
        # Arrange & Act
        fear_gorta = FearGorta(5, 5)

        # Assert
        assert isinstance(fear_gorta.description, str)
        assert len(fear_gorta.description) > 0

    def test_fear_gorta_has_monster_type(self):
        """Test FearGorta has a non-empty monster_type"""
        # Arrange & Act
        fear_gorta = FearGorta(5, 5)

        # Assert
        assert isinstance(fear_gorta.monster_type, str)
        assert len(fear_gorta.monster_type) > 0
        assert fear_gorta.monster_type == "fear_gorta"

    def test_fear_gorta_initializes_alive(self):
        """Test FearGorta initializes as alive"""
        # Arrange & Act
        fear_gorta = FearGorta(5, 5)

        # Assert
        assert fear_gorta.is_alive is True
        assert fear_gorta.health == fear_gorta.max_health

    def test_fear_gorta_draw_body(self):
        """Test FearGorta draw_body renders without error"""
        # Arrange
        fear_gorta = FearGorta(5, 5)
        screen = pygame.display.get_surface()

        # Act & Assert - should not raise exception
        fear_gorta.draw_body(screen, 400, 300)

    def test_fear_gorta_draw_details(self):
        """Test FearGorta draw_details renders without error"""
        # Arrange
        fear_gorta = FearGorta(5, 5)
        screen = pygame.display.get_surface()

        # Act & Assert - should not raise exception
        fear_gorta.draw_details(screen, 400, 300)
