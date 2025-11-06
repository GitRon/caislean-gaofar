"""Tests for combat.py - CombatSystem class"""

import pytest
from unittest.mock import Mock, patch
import pygame
from combat import CombatSystem
from entity import Entity
from warrior import Warrior


@pytest.fixture
def mock_screen():
    """Create a mock pygame surface"""
    screen = Mock(spec=pygame.Surface)
    screen.blit = Mock()
    return screen


@pytest.fixture
def mock_font():
    """Create a mock pygame font"""
    font = Mock()
    text_surface = Mock()
    font.render.return_value = text_surface
    return font


class TestCombatSystem:
    """Tests for CombatSystem class"""

    def test_is_in_attack_range_warrior_in_range(self):
        """Test warrior is in attack range when 1 tile away"""
        # Arrange
        warrior = Warrior(5, 5)
        monster = Entity(6, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        result = CombatSystem.is_in_attack_range(warrior, monster)

        # Assert
        assert result is True

    def test_is_in_attack_range_warrior_same_position(self):
        """Test warrior in attack range at same position"""
        # Arrange
        warrior = Warrior(5, 5)
        monster = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        result = CombatSystem.is_in_attack_range(warrior, monster)

        # Assert
        assert result is True

    def test_is_in_attack_range_warrior_out_of_range(self):
        """Test warrior out of attack range when 2 tiles away"""
        # Arrange
        warrior = Warrior(5, 5)
        monster = Entity(7, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        result = CombatSystem.is_in_attack_range(warrior, monster)

        # Assert
        assert result is False

    def test_is_in_attack_range_monster_with_attack_range_in_range(self):
        """Test monster with attack_range attribute in range"""
        # Arrange
        warrior = Warrior(5, 5)
        monster = Entity(8, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        monster.attack_range = 5

        # Act
        result = CombatSystem.is_in_attack_range(monster, warrior)

        # Assert
        assert result is True

    def test_is_in_attack_range_monster_with_attack_range_out_of_range(self):
        """Test monster with attack_range attribute out of range"""
        # Arrange
        warrior = Warrior(5, 5)
        monster = Entity(8, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        monster.attack_range = 2

        # Act
        result = CombatSystem.is_in_attack_range(monster, warrior)

        # Assert
        assert result is False

    def test_is_in_attack_range_monster_exactly_at_attack_range(self):
        """Test monster exactly at attack_range boundary"""
        # Arrange
        warrior = Warrior(5, 5)
        monster = Entity(8, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        monster.attack_range = 3

        # Act
        result = CombatSystem.is_in_attack_range(monster, warrior)

        # Assert
        assert result is True

    def test_draw_combat_ui_basic(self, mock_screen):
        """Test drawing combat UI with basic entities (compatibility check)"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.health = 80
        monster = Entity(6, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        monster.health = 50

        # Act - should not crash (UI moved to HUD)
        CombatSystem.draw_combat_ui(mock_screen, warrior, monster)

        # Assert - method exists and completes without error
        assert True

    def test_draw_combat_ui_with_monster_type(self, mock_screen):
        """Test drawing combat UI with monster type (compatibility check)"""
        # Arrange
        warrior = Warrior(5, 5)
        monster = Entity(6, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        monster.monster_type = "banshee"

        # Act - should not crash (UI moved to HUD)
        CombatSystem.draw_combat_ui(mock_screen, warrior, monster)

        # Assert - method exists and completes without error
        assert True

    def test_draw_combat_ui_with_monster_description(self, mock_screen):
        """Test drawing combat UI with monster description (compatibility check)"""
        # Arrange
        warrior = Warrior(5, 5)
        monster = Entity(6, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        monster.monster_type = "banshee"
        monster.description = "A wailing spirit"

        # Act - should not crash (UI moved to HUD)
        CombatSystem.draw_combat_ui(mock_screen, warrior, monster)

        # Assert - method exists and completes without error
        assert True

    @patch("pygame.draw.line")
    def test_draw_attack_range_indicator_in_range(self, mock_draw_line, mock_screen):
        """Test drawing attack range indicator when in range"""
        # Arrange
        warrior = Warrior(5, 5)
        monster = Entity(6, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        CombatSystem.draw_attack_range_indicator(mock_screen, warrior, monster)

        # Assert
        assert mock_draw_line.called

    @patch("pygame.draw.line")
    def test_draw_attack_range_indicator_out_of_range(
        self, mock_draw_line, mock_screen
    ):
        """Test drawing attack range indicator when out of range"""
        # Arrange
        warrior = Warrior(5, 5)
        monster = Entity(10, 10, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        CombatSystem.draw_attack_range_indicator(mock_screen, warrior, monster)

        # Assert
        assert not mock_draw_line.called
