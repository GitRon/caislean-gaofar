"""Tests for monsters/base_monster.py - BaseMonster class"""

import pytest
from unittest.mock import Mock, patch
import pygame
from caislean_gaofar.entities.monsters.base_monster import BaseMonster
from caislean_gaofar.entities.entity import Entity
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.core import config


@pytest.fixture
def mock_screen():
    """Create a mock pygame surface"""
    screen = Mock()
    screen.blit = Mock()
    return screen


class MonsterSubclass(BaseMonster):
    """Test subclass for testing BaseMonster functionality"""

    HEALTH = 80
    ATTACK_DAMAGE = 12
    SPEED = 2
    CHASE_RANGE = 6
    ATTACK_RANGE = 2
    DESCRIPTION = "Test monster"
    MONSTER_TYPE = "test_monster"


class TestBaseMonster:
    """Tests for BaseMonster class"""

    def test_base_monster_initialization_with_defaults(self):
        """Test BaseMonster initialization with default values"""
        # Arrange & Act
        monster = BaseMonster(5, 3)

        # Assert
        assert monster.grid_x == 5
        assert monster.grid_y == 3
        assert monster.size == config.MONSTER_SIZE
        assert monster.color == config.RED
        assert monster.max_health == BaseMonster.HEALTH
        assert monster.health == BaseMonster.HEALTH
        assert monster.speed == BaseMonster.SPEED
        assert monster.attack_damage == BaseMonster.ATTACK_DAMAGE
        assert monster.attack_cooldown == config.MONSTER_ATTACK_COOLDOWN
        assert monster.monster_type == BaseMonster.MONSTER_TYPE
        assert monster.chase_range == BaseMonster.CHASE_RANGE
        assert monster.attack_range == BaseMonster.ATTACK_RANGE
        assert monster.description == BaseMonster.DESCRIPTION
        assert monster.frame_count == 0

    def test_base_monster_initialization_with_subclass(self):
        """Test BaseMonster initialization with subclass values"""
        # Arrange & Act
        monster = MonsterSubclass(7, 4)

        # Assert
        assert monster.grid_x == 7
        assert monster.grid_y == 4
        assert monster.max_health == 80
        assert monster.health == 80
        assert monster.speed == 2
        assert monster.attack_damage == 12
        assert monster.monster_type == "test_monster"
        assert monster.chase_range == 6
        assert monster.attack_range == 2
        assert monster.description == "Test monster"

    def test_execute_turn_target_in_attack_range(self):
        """Test execute_turn when target is in attack range"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        target = Warrior(6, 5)
        monster.turns_since_last_attack = monster.attack_cooldown

        # Act
        monster.execute_turn(target)

        # Assert
        assert target.health < target.max_health

    def test_execute_turn_target_in_chase_but_not_attack_range(self):
        """Test execute_turn when target is in chase range but not attack range"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        target = Warrior(9, 5)
        initial_monster_x = monster.grid_x
        initial_monster_y = monster.grid_y

        # Act
        monster.execute_turn(target)

        # Assert - monster should have moved
        assert (
            monster.grid_x != initial_monster_x or monster.grid_y != initial_monster_y
        )

    def test_execute_turn_target_out_of_chase_range(self):
        """Test execute_turn when target is out of chase range"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        target = Warrior(15, 5)
        initial_monster_x = monster.grid_x
        initial_monster_y = monster.grid_y

        # Act
        monster.execute_turn(target)

        # Assert - monster should not move
        assert monster.grid_x == initial_monster_x
        assert monster.grid_y == initial_monster_y

    def test_execute_turn_monster_dead(self):
        """Test execute_turn when monster is dead"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        target = Warrior(6, 5)
        monster.is_alive = False
        initial_health = target.health

        # Act
        monster.execute_turn(target)

        # Assert - target should not be attacked
        assert target.health == initial_health

    def test_execute_turn_target_dead(self):
        """Test execute_turn when target is dead"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        target = Warrior(6, 5)
        target.is_alive = False
        initial_monster_x = monster.grid_x

        # Act
        monster.execute_turn(target)

        # Assert - monster should not move
        assert monster.grid_x == initial_monster_x

    def test_execute_turn_target_at_exact_chase_range(self):
        """Test execute_turn when target is exactly at chase range"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        target = Warrior(11, 5)  # Distance = 6, exactly at chase range
        initial_monster_x = monster.grid_x

        # Act
        monster.execute_turn(target)

        # Assert - monster should move
        assert monster.grid_x != initial_monster_x

    def test_execute_turn_target_at_exact_attack_range(self):
        """Test execute_turn when target is exactly at attack range"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        target = Warrior(7, 5)  # Distance = 2, exactly at attack range
        monster.turns_since_last_attack = monster.attack_cooldown

        # Act
        monster.execute_turn(target)

        # Assert - should attack, not move
        assert target.health < target.max_health

    def test_move_towards_target_horizontal_right(self):
        """Test moving towards target to the right"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        target = Warrior(10, 5)

        # Act
        monster._move_towards_target(target)

        # Assert
        assert monster.grid_x == 6
        assert monster.grid_y == 5

    def test_move_towards_target_horizontal_left(self):
        """Test moving towards target to the left"""
        # Arrange
        monster = MonsterSubclass(10, 5)
        target = Warrior(5, 5)

        # Act
        monster._move_towards_target(target)

        # Assert
        assert monster.grid_x == 9
        assert monster.grid_y == 5

    def test_move_towards_target_vertical_down(self):
        """Test moving towards target downward"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        target = Warrior(5, 10)

        # Act
        monster._move_towards_target(target)

        # Assert
        assert monster.grid_x == 5
        assert monster.grid_y == 6

    def test_move_towards_target_vertical_up(self):
        """Test moving towards target upward"""
        # Arrange
        monster = MonsterSubclass(5, 10)
        target = Warrior(5, 5)

        # Act
        monster._move_towards_target(target)

        # Assert
        assert monster.grid_x == 5
        assert monster.grid_y == 9

    def test_move_towards_target_diagonal_prioritize_horizontal(self):
        """Test moving towards diagonal target prioritizing horizontal"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        target = Warrior(10, 6)  # More horizontal distance

        # Act
        monster._move_towards_target(target)

        # Assert
        assert monster.grid_x == 6  # Should move horizontally first

    def test_move_towards_target_diagonal_prioritize_vertical(self):
        """Test moving towards diagonal target prioritizing vertical"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        target = Warrior(6, 10)  # More vertical distance

        # Act
        monster._move_towards_target(target)

        # Assert
        assert monster.grid_y == 6  # Should move vertically first

    def test_move_towards_target_blocked_horizontal(self):
        """Test moving towards target when horizontal path blocked"""
        # Arrange
        monster = MonsterSubclass(config.GRID_WIDTH - 1, 5)
        target = Warrior(config.GRID_WIDTH + 5, 10)

        # Act
        monster._move_towards_target(target)

        # Assert - should try vertical movement instead
        assert monster.grid_y == 6

    def test_move_towards_target_blocked_vertical(self):
        """Test moving towards target when vertical path blocked"""
        # Arrange
        monster = MonsterSubclass(5, config.GRID_HEIGHT - 1)
        target = Warrior(10, config.GRID_HEIGHT + 5)

        # Act
        monster._move_towards_target(target)

        # Assert - should try horizontal movement instead
        assert monster.grid_x == 6

    def test_move_towards_target_same_position(self):
        """Test moving towards target at same position"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        target = Warrior(5, 5)

        # Act
        monster._move_towards_target(target)

        # Assert - should not move
        assert monster.grid_x == 5
        assert monster.grid_y == 5

    def test_frame_count_starts_at_zero(self):
        """Test frame count starts at zero"""
        # Arrange & Act
        monster = MonsterSubclass(5, 5)

        # Assert
        assert monster.frame_count == 0

    def test_monster_inherits_from_entity(self):
        """Test BaseMonster inherits from Entity"""
        # Arrange
        monster = BaseMonster(5, 5)

        # Act & Assert
        assert isinstance(monster, Entity)

    @patch("pygame.draw.circle")
    def test_draw_without_custom_renderer(self, mock_draw_circle):
        """Test drawing without custom renderer uses fallback"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        screen = pygame.display.set_mode((800, 600))

        # Act
        monster.draw(screen)

        # Assert - fallback draw_body should draw eyes
        assert mock_draw_circle.called
        assert monster.frame_count == 1

    def test_draw_with_custom_renderer(self):
        """Test drawing with custom draw_body override"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        screen = pygame.display.set_mode((800, 600))

        # Mock the draw_body method
        monster.draw_body = Mock()
        monster.draw_details = Mock()

        # Act
        monster.draw(screen)

        # Assert - draw_body and draw_details should be called
        assert monster.draw_body.called
        assert monster.draw_details.called
        assert monster.frame_count == 1

    def test_draw_increments_frame_count(self):
        """Test draw increments frame count"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        screen = pygame.display.set_mode((800, 600))
        initial_count = monster.frame_count

        # Act
        monster.draw(screen)
        monster.draw(screen)

        # Assert
        assert monster.frame_count == initial_count + 2

    def test_draw_fallback_renders_eyes(self):
        """Test fallback draw_body renders eyes"""
        # Arrange
        monster = MonsterSubclass(5, 5)
        screen = pygame.display.set_mode((800, 600))

        # Act & Assert - should not raise exception
        monster.draw(screen)
