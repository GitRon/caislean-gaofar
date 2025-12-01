"""Tests for Merrow monster class"""

import pygame
import pytest
from typing import Generator

from caislean_gaofar.entities.monsters.merrow import Merrow
from caislean_gaofar.entities.monsters.base_monster import BaseMonster


class TestMerrow:
    """Tests for Merrow monster"""

    @pytest.fixture(autouse=True)
    def setup_pygame(self) -> Generator[None, None, None]:
        """Initialize pygame before each test."""
        pygame.init()
        pygame.display.set_mode((800, 600))
        yield
        pygame.quit()

    def test_merrow_initialization(self):
        """Test Merrow can be initialized"""
        # Arrange & Act
        merrow = Merrow(5, 3)

        # Assert
        assert merrow.grid_x == 5
        assert merrow.grid_y == 3
        assert isinstance(merrow, BaseMonster)

    def test_merrow_has_required_attributes(self):
        """Test Merrow has all required class attributes"""
        # Assert
        assert hasattr(Merrow, "HEALTH")
        assert hasattr(Merrow, "ATTACK_DAMAGE")
        assert hasattr(Merrow, "SPEED")
        assert hasattr(Merrow, "CHASE_RANGE")
        assert hasattr(Merrow, "ATTACK_RANGE")
        assert hasattr(Merrow, "DESCRIPTION")
        assert hasattr(Merrow, "MONSTER_TYPE")

    def test_merrow_stats_are_positive(self):
        """Test Merrow stats are positive values"""
        # Arrange & Act
        merrow = Merrow(5, 5)

        # Assert
        assert merrow.max_health > 0
        assert merrow.attack_damage > 0
        assert merrow.speed > 0
        assert merrow.chase_range > 0
        assert merrow.attack_range > 0

    def test_merrow_has_description(self):
        """Test Merrow has a non-empty description"""
        # Arrange & Act
        merrow = Merrow(5, 5)

        # Assert
        assert isinstance(merrow.description, str)
        assert len(merrow.description) > 0

    def test_merrow_has_monster_type(self):
        """Test Merrow has a non-empty monster_type"""
        # Arrange & Act
        merrow = Merrow(5, 5)

        # Assert
        assert isinstance(merrow.monster_type, str)
        assert len(merrow.monster_type) > 0
        assert merrow.monster_type == "merrow"

    def test_merrow_initializes_alive(self):
        """Test Merrow initializes as alive"""
        # Arrange & Act
        merrow = Merrow(5, 5)

        # Assert
        assert merrow.is_alive is True
        assert merrow.health == merrow.max_health

    def test_merrow_draw_body(self):
        """Test Merrow draw_body renders without error"""
        # Arrange
        merrow = Merrow(5, 5)
        screen = pygame.display.get_surface()

        # Act & Assert - should not raise exception
        merrow.draw_body(screen, 400, 300)

    def test_merrow_draw_details(self):
        """Test Merrow draw_details renders without error"""
        # Arrange
        merrow = Merrow(5, 5)
        screen = pygame.display.get_surface()

        # Act & Assert - should not raise exception
        merrow.draw_details(screen, 400, 300)
