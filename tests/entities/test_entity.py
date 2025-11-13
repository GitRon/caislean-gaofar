"""Tests for entity.py - Entity base class"""

import pytest
from unittest.mock import Mock, patch
import pygame
from caislean_gaofar.entities.entity import Entity
from caislean_gaofar.core import config


@pytest.fixture
def mock_screen():
    """Create a mock pygame surface"""
    return Mock(spec=pygame.Surface)


class TestEntity:
    """Tests for Entity class"""

    def test_entity_initialization(self):
        """Test Entity initialization with all parameters"""
        # Arrange & Act
        entity = Entity(
            grid_x=5,
            grid_y=3,
            size=50,
            color=(255, 0, 0),
            max_health=100,
            speed=1,
            attack_damage=10,
            attack_cooldown=2,
        )

        # Assert
        assert entity.grid_x == 5
        assert entity.grid_y == 3
        assert entity.size == 50
        assert entity.color == (255, 0, 0)
        assert entity.max_health == 100
        assert entity.health == 100
        assert entity.speed == 1
        assert entity.attack_damage == 10
        assert entity.attack_cooldown == 2
        assert entity.turns_since_last_attack == 2
        assert entity.is_alive is True

    def test_entity_x_property(self):
        """Test x property converts grid to pixel coordinates"""
        # Arrange
        entity = Entity(5, 3, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        x = entity.x

        # Assert
        assert x == 5 * config.TILE_SIZE

    def test_entity_y_property(self):
        """Test y property converts grid to pixel coordinates"""
        # Arrange
        entity = Entity(5, 3, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        y = entity.y

        # Assert
        assert y == 3 * config.TILE_SIZE

    def test_get_rect(self):
        """Test get_rect returns correct pygame.Rect"""
        # Arrange
        entity = Entity(5, 3, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        rect = entity.get_rect()

        # Assert
        assert isinstance(rect, pygame.Rect)
        assert rect.x == 5 * config.TILE_SIZE
        assert rect.y == 3 * config.TILE_SIZE
        assert rect.width == 50
        assert rect.height == 50

    def test_get_center(self):
        """Test get_center returns center position"""
        # Arrange
        entity = Entity(5, 3, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        center_x, center_y = entity.get_center()

        # Assert
        assert center_x == 5 * config.TILE_SIZE + 25
        assert center_y == 3 * config.TILE_SIZE + 25

    def test_grid_distance_to_same_position(self):
        """Test grid distance to same position"""
        # Arrange
        entity1 = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        entity2 = Entity(5, 5, 50, (0, 255, 0), 100, 1, 10, 2)

        # Act
        distance = entity1.grid_distance_to(entity2)

        # Assert
        assert distance == 0

    def test_grid_distance_to_different_position(self):
        """Test grid distance to different position"""
        # Arrange
        entity1 = Entity(1, 1, 50, (255, 0, 0), 100, 1, 10, 2)
        entity2 = Entity(4, 5, 50, (0, 255, 0), 100, 1, 10, 2)

        # Act
        distance = entity1.grid_distance_to(entity2)

        # Assert
        assert distance == 7  # |1-4| + |1-5| = 3 + 4

    def test_can_attack_when_cooldown_ready(self):
        """Test can_attack returns True when cooldown is ready"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        entity.turns_since_last_attack = 2

        # Act
        result = entity.can_attack()

        # Assert
        assert result is True

    def test_can_attack_when_cooldown_not_ready(self):
        """Test can_attack returns False when cooldown not ready"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        entity.turns_since_last_attack = 1

        # Act
        result = entity.can_attack()

        # Assert
        assert result is False

    def test_can_attack_when_cooldown_zero_turns(self):
        """Test can_attack when turns since last attack is zero"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        entity.turns_since_last_attack = 0

        # Act
        result = entity.can_attack()

        # Assert
        assert result is False

    def test_attack_successful(self):
        """Test successful attack on target"""
        # Arrange
        attacker = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        target = Entity(6, 5, 50, (0, 255, 0), 100, 1, 10, 2)
        attacker.turns_since_last_attack = 2

        # Act
        result = attacker.attack(target)

        # Assert
        assert result is True
        assert target.health == 90
        assert attacker.turns_since_last_attack == 0

    def test_attack_when_cooldown_not_ready(self):
        """Test attack fails when cooldown not ready"""
        # Arrange
        attacker = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        target = Entity(6, 5, 50, (0, 255, 0), 100, 1, 10, 2)
        attacker.turns_since_last_attack = 1

        # Act
        result = attacker.attack(target)

        # Assert
        assert result is False
        assert target.health == 100
        assert attacker.turns_since_last_attack == 1

    def test_take_damage_normal(self):
        """Test taking normal damage"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        entity.take_damage(30)

        # Assert
        assert entity.health == 70
        assert entity.is_alive is True

    def test_take_damage_to_zero_health(self):
        """Test taking damage that reduces health to exactly zero"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        entity.take_damage(100)

        # Assert
        assert entity.health == 0
        assert entity.is_alive is False

    def test_take_damage_exceeding_health(self):
        """Test taking damage exceeding current health"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        entity.take_damage(150)

        # Assert
        assert entity.health == 0
        assert entity.is_alive is False

    def test_take_damage_when_already_low_health(self):
        """Test taking damage when already at low health"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        entity.health = 10

        # Act
        entity.take_damage(5)

        # Assert
        assert entity.health == 5
        assert entity.is_alive is True

    def test_move_valid_position(self):
        """Test moving to valid position"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        result = entity.move(1, 0)

        # Assert
        assert result is True
        assert entity.grid_x == 6
        assert entity.grid_y == 5

    def test_move_to_invalid_position_negative_x(self):
        """Test moving to invalid position (negative x)"""
        # Arrange
        entity = Entity(0, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        result = entity.move(-1, 0)

        # Assert
        assert result is False
        assert entity.grid_x == 0
        assert entity.grid_y == 5

    def test_move_to_invalid_position_negative_y(self):
        """Test moving to invalid position (negative y)"""
        # Arrange
        entity = Entity(5, 0, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        result = entity.move(0, -1)

        # Assert
        assert result is False
        assert entity.grid_x == 5
        assert entity.grid_y == 0

    def test_move_to_invalid_position_beyond_width(self):
        """Test moving beyond grid width"""
        # Arrange
        entity = Entity(config.GRID_WIDTH - 1, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        result = entity.move(1, 0)

        # Assert
        assert result is False
        assert entity.grid_x == config.GRID_WIDTH - 1
        assert entity.grid_y == 5

    def test_move_to_invalid_position_beyond_height(self):
        """Test moving beyond grid height"""
        # Arrange
        entity = Entity(5, config.GRID_HEIGHT - 1, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        result = entity.move(0, 1)

        # Assert
        assert result is False
        assert entity.grid_x == 5
        assert entity.grid_y == config.GRID_HEIGHT - 1

    def test_move_multiple_tiles(self):
        """Test moving multiple tiles at once"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        result = entity.move(2, 3)

        # Assert
        assert result is True
        assert entity.grid_x == 7
        assert entity.grid_y == 8

    def test_move_negative_delta(self):
        """Test moving with negative delta"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        result = entity.move(-2, -1)

        # Assert
        assert result is True
        assert entity.grid_x == 3
        assert entity.grid_y == 4

    @patch("pygame.draw.rect")
    def test_draw_calls_pygame_draw(self, mock_draw_rect, mock_screen):
        """Test draw method calls pygame.draw.rect"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        entity.draw(mock_screen)

        # Assert
        assert mock_draw_rect.called

    @patch("pygame.draw.rect")
    def test_draw_health_bar(self, mock_draw_rect, mock_screen):
        """Test draw_health_bar method"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        entity.health = 50

        # Act
        entity.draw_health_bar(mock_screen)

        # Assert
        assert mock_draw_rect.called
        assert mock_draw_rect.call_count >= 3  # background, health, border

    def test_on_turn_start_increments_attack_cooldown(self):
        """Test on_turn_start increments turns_since_last_attack"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        entity.turns_since_last_attack = 0

        # Act
        entity.on_turn_start()

        # Assert
        assert entity.turns_since_last_attack == 1

    def test_on_turn_start_multiple_calls(self):
        """Test on_turn_start with multiple calls"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        entity.turns_since_last_attack = 0

        # Act
        entity.on_turn_start()
        entity.on_turn_start()
        entity.on_turn_start()

        # Assert
        assert entity.turns_since_last_attack == 3

    def test_update_method_exists(self):
        """Test update method exists and can be called"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act & Assert (should not raise exception)
        entity.update()

    def test_move_with_world_map_passable(self):
        """Test moving with world_map parameter to passable terrain"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        mock_world_map = Mock()
        mock_world_map.is_passable.return_value = True

        # Act
        result = entity.move(1, 0, mock_world_map)

        # Assert
        assert result is True
        assert entity.grid_x == 6
        assert entity.grid_y == 5
        mock_world_map.is_passable.assert_called_once_with(6, 5)

    def test_move_with_world_map_blocked(self):
        """Test moving with world_map parameter to blocked terrain"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        mock_world_map = Mock()
        mock_world_map.is_passable.return_value = False

        # Act
        result = entity.move(1, 0, mock_world_map)

        # Assert
        assert result is False
        assert entity.grid_x == 5
        assert entity.grid_y == 5
        mock_world_map.is_passable.assert_called_once_with(6, 5)

    def test_take_damage_with_defense(self):
        """Test taking damage with defense reduces damage"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        entity.take_damage(20, defense=5)

        # Assert - Should take 20 - 5 = 15 damage
        assert entity.health == 85
        assert entity.is_alive is True

    def test_take_damage_with_high_defense(self):
        """Test taking damage with high defense still deals minimum 1 damage"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        entity.take_damage(10, defense=50)

        # Assert - Should take at least 1 damage
        assert entity.health == 99
        assert entity.is_alive is True

    def test_take_damage_with_defense_equals_damage(self):
        """Test taking damage when defense equals damage still deals 1 damage"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        entity.take_damage(10, defense=10)

        # Assert - Should take at least 1 damage
        assert entity.health == 99
        assert entity.is_alive is True

    def test_take_damage_with_zero_defense(self):
        """Test taking damage with zero defense (default behavior)"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act
        entity.take_damage(25, defense=0)

        # Assert - Should take full damage
        assert entity.health == 75
        assert entity.is_alive is True

    def test_take_damage_lethal_with_defense(self):
        """Test taking lethal damage with defense"""
        # Arrange
        entity = Entity(5, 5, 50, (255, 0, 0), 100, 1, 10, 2)

        # Act - 200 damage with 50 defense = 150 actual damage
        entity.take_damage(200, defense=50)

        # Assert
        assert entity.health == 0
        assert entity.is_alive is False
