"""Tests for warrior.py - Warrior class"""

import pytest
from unittest.mock import Mock, patch
import pygame
from warrior import Warrior
from entity import Entity
from item import Item, ItemType
import config


@pytest.fixture
def mock_screen():
    """Create a mock pygame surface"""
    return Mock(spec=pygame.Surface)


class TestWarrior:
    """Tests for Warrior class"""

    def test_warrior_initialization(self):
        """Test Warrior initialization"""
        # Arrange & Act
        warrior = Warrior(5, 3)

        # Assert
        assert warrior.grid_x == 5
        assert warrior.grid_y == 3
        assert warrior.size == config.WARRIOR_SIZE
        assert warrior.color == config.BLUE
        assert warrior.max_health == config.WARRIOR_MAX_HEALTH
        assert warrior.health == config.WARRIOR_MAX_HEALTH
        assert warrior.speed == config.WARRIOR_SPEED
        assert warrior.attack_damage == config.WARRIOR_ATTACK_DAMAGE
        assert warrior.attack_cooldown == config.WARRIOR_ATTACK_COOLDOWN
        assert warrior.base_attack_damage == config.WARRIOR_ATTACK_DAMAGE
        assert warrior.inventory is not None
        assert warrior.pending_action is None

    def test_get_effective_attack_damage_no_bonuses(self):
        """Test effective attack damage with no inventory bonuses"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        damage = warrior.get_effective_attack_damage()

        # Assert
        assert damage == config.WARRIOR_ATTACK_DAMAGE

    def test_get_effective_attack_damage_with_weapon(self):
        """Test effective attack damage with weapon bonus"""
        # Arrange
        warrior = Warrior(5, 5)
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        warrior.inventory.add_item(weapon)

        # Act
        damage = warrior.get_effective_attack_damage()

        # Assert
        assert damage == config.WARRIOR_ATTACK_DAMAGE + 10

    def test_get_effective_attack_damage_with_weapon_and_armor(self):
        """Test effective attack damage with both weapon and armor bonuses"""
        # Arrange
        warrior = Warrior(5, 5)
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        armor = Item("Shield", ItemType.ARMOR, attack_bonus=5)
        warrior.inventory.add_item(weapon)
        warrior.inventory.add_item(armor)

        # Act
        damage = warrior.get_effective_attack_damage()

        # Assert
        assert damage == config.WARRIOR_ATTACK_DAMAGE + 15

    def test_attack_successful_with_cooldown_ready(self):
        """Test successful attack with cooldown ready"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(6, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        warrior.turns_since_last_attack = warrior.attack_cooldown

        # Act
        result = warrior.attack(target)

        # Assert
        assert result is True
        assert target.health == 100 - config.WARRIOR_ATTACK_DAMAGE
        assert warrior.turns_since_last_attack == 0

    def test_attack_with_weapon_bonus(self):
        """Test attack applies weapon bonus damage"""
        # Arrange
        warrior = Warrior(5, 5)
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        warrior.inventory.add_item(weapon)
        target = Entity(6, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        warrior.turns_since_last_attack = warrior.attack_cooldown

        # Act
        result = warrior.attack(target)

        # Assert
        assert result is True
        assert target.health == 100 - (config.WARRIOR_ATTACK_DAMAGE + 10)

    def test_attack_fails_when_cooldown_not_ready(self):
        """Test attack fails when cooldown not ready"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(6, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        warrior.turns_since_last_attack = 0

        # Act
        result = warrior.attack(target)

        # Assert
        assert result is False
        assert target.health == 100

    def test_queue_movement(self):
        """Test queueing movement action"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        warrior.queue_movement(1, 0)

        # Assert
        assert warrior.pending_action == ("move", 1, 0)

    def test_queue_movement_replaces_previous(self):
        """Test queueing movement replaces previous action"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.queue_movement(1, 0)

        # Act
        warrior.queue_movement(0, 1)

        # Assert
        assert warrior.pending_action == ("move", 0, 1)

    def test_queue_attack(self):
        """Test queueing attack action"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        warrior.queue_attack()

        # Assert
        assert warrior.pending_action == ("attack",)

    def test_queue_attack_replaces_previous(self):
        """Test queueing attack replaces previous action"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.queue_movement(1, 0)

        # Act
        warrior.queue_attack()

        # Assert
        assert warrior.pending_action == ("attack",)

    def test_execute_turn_no_action(self):
        """Test execute_turn with no pending action"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        result = warrior.execute_turn()

        # Assert
        assert result is False

    def test_execute_turn_move_action(self):
        """Test execute_turn with move action"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.queue_movement(1, 0)

        # Act
        result = warrior.execute_turn()

        # Assert
        assert result is True
        assert warrior.grid_x == 6
        assert warrior.grid_y == 5
        assert warrior.pending_action is None

    def test_execute_turn_move_action_negative_delta(self):
        """Test execute_turn with negative movement"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.queue_movement(-1, -1)

        # Act
        result = warrior.execute_turn()

        # Assert
        assert result is True
        assert warrior.grid_x == 4
        assert warrior.grid_y == 4
        assert warrior.pending_action is None

    def test_execute_turn_attack_in_range(self):
        """Test execute_turn with attack action when target in range"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(6, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        warrior.queue_attack()
        warrior.turns_since_last_attack = warrior.attack_cooldown

        # Act
        result = warrior.execute_turn(target)

        # Assert
        assert result is True
        assert target.health < 100
        assert warrior.pending_action is None

    def test_execute_turn_attack_exactly_one_tile_away(self):
        """Test execute_turn with attack when exactly 1 tile away"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(5, 6, 50, (255, 0, 0), 100, 1, 10, 2)
        warrior.queue_attack()
        warrior.turns_since_last_attack = warrior.attack_cooldown

        # Act
        result = warrior.execute_turn(target)

        # Assert
        assert result is True
        assert target.health < 100
        assert warrior.pending_action is None

    def test_execute_turn_attack_out_of_range(self):
        """Test execute_turn with attack action when target out of range"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(8, 8, 50, (255, 0, 0), 100, 1, 10, 2)
        warrior.queue_attack()
        warrior.turns_since_last_attack = warrior.attack_cooldown

        # Act
        result = warrior.execute_turn(target)

        # Assert
        assert result is False
        assert target.health == 100
        assert warrior.pending_action is None

    def test_execute_turn_attack_no_target(self):
        """Test execute_turn with attack action but no target"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.queue_attack()

        # Act
        result = warrior.execute_turn()

        # Assert
        assert result is False
        assert warrior.pending_action is None

    def test_execute_turn_attack_cooldown_not_ready(self):
        """Test execute_turn with attack when cooldown not ready"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(6, 5, 50, (255, 0, 0), 100, 1, 10, 2)
        warrior.queue_attack()
        warrior.turns_since_last_attack = 0

        # Act
        result = warrior.execute_turn(target)

        # Assert
        assert result is False
        assert target.health == 100
        assert warrior.pending_action is None

    @patch("pygame.draw.line")
    @patch("pygame.draw.rect")
    def test_draw_warrior(self, mock_draw_rect, mock_draw_line, mock_screen):
        """Test drawing warrior with cross pattern"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        warrior.draw(mock_screen)

        # Assert
        assert mock_draw_rect.called
        assert mock_draw_line.called
        assert mock_draw_line.call_count == 2  # vertical and horizontal lines

    def test_warrior_inherits_from_entity(self):
        """Test Warrior inherits from Entity"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act & Assert
        assert isinstance(warrior, Entity)

    def test_warrior_has_inventory(self):
        """Test Warrior has inventory instance"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act & Assert
        assert hasattr(warrior, "inventory")
        assert warrior.inventory.weapon_slot is None
        assert warrior.inventory.armor_slot is None
        assert warrior.inventory.backpack_slots == [None, None, None, None, None]

    def test_execute_turn_unknown_action_type(self):
        """Test execute_turn with unknown action type returns False"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.pending_action = ("unknown",)

        # Act
        result = warrior.execute_turn()

        # Assert
        assert result is False
