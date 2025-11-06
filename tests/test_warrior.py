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

    @patch("pygame.draw.arc")
    @patch("pygame.draw.ellipse")
    @patch("pygame.draw.circle")
    @patch("pygame.draw.rect")
    def test_draw_warrior(
        self,
        mock_draw_rect,
        mock_draw_circle,
        mock_draw_ellipse,
        mock_draw_arc,
        mock_screen,
    ):
        """Test drawing warrior as detailed human character"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        warrior.draw(mock_screen)

        # Assert
        # Verify all drawing methods are called for the detailed human character
        assert mock_draw_rect.called  # Body, arms, legs, boots, sword
        assert mock_draw_circle.called  # Head and eyes
        assert mock_draw_ellipse.called  # Hair
        assert mock_draw_arc.called  # Smile

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

    def test_use_health_potion_success(self):
        """Test using health potion successfully restores health"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.health = 50
        # Add health potion to inventory
        potion = Item(
            "Health Potion", ItemType.CONSUMABLE, "Restores 30 HP", health_bonus=30
        )
        warrior.inventory.add_item(potion)
        initial_potions = warrior.count_health_potions()

        # Act
        result = warrior.use_health_potion()

        # Assert
        assert result is True
        assert warrior.health == 80  # 50 + 30
        assert warrior.count_health_potions() == initial_potions - 1

    def test_use_health_potion_caps_at_max_health(self):
        """Test using health potion doesn't exceed max health"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.health = 90
        # Add health potion to inventory
        potion = Item(
            "Health Potion", ItemType.CONSUMABLE, "Restores 30 HP", health_bonus=30
        )
        warrior.inventory.add_item(potion)
        initial_potions = warrior.count_health_potions()

        # Act
        result = warrior.use_health_potion()

        # Assert
        assert result is True
        assert warrior.health == warrior.max_health
        assert warrior.count_health_potions() == initial_potions - 1

    def test_use_health_potion_no_potions_left(self):
        """Test using health potion fails when none available"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.health = 50
        # No potions in inventory

        # Act
        result = warrior.use_health_potion()

        # Assert
        assert result is False
        assert warrior.health == 50
        assert warrior.count_health_potions() == 0

    def test_use_health_potion_at_full_health(self):
        """Test using health potion fails when at full health"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.health = warrior.max_health
        # Add health potion to inventory
        potion = Item(
            "Health Potion", ItemType.CONSUMABLE, "Restores 30 HP", health_bonus=30
        )
        warrior.inventory.add_item(potion)
        initial_potions = warrior.count_health_potions()

        # Act
        result = warrior.use_health_potion()

        # Assert
        assert result is False
        assert warrior.health == warrior.max_health
        assert warrior.count_health_potions() == initial_potions

    def test_count_health_potions_empty(self):
        """Test counting health potions when none are in inventory"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        count = warrior.count_health_potions()

        # Assert
        assert count == 0

    def test_count_health_potions_multiple(self):
        """Test counting multiple health potions"""
        # Arrange
        warrior = Warrior(5, 5)
        potion1 = Item(
            "Health Potion", ItemType.CONSUMABLE, "Restores HP", health_bonus=30
        )
        potion2 = Item(
            "Health Potion", ItemType.CONSUMABLE, "Restores HP", health_bonus=30
        )
        potion3 = Item(
            "Health Potion", ItemType.CONSUMABLE, "Restores HP", health_bonus=30
        )
        warrior.inventory.add_item(potion1)
        warrior.inventory.add_item(potion2)
        warrior.inventory.add_item(potion3)

        # Act
        count = warrior.count_health_potions()

        # Assert
        assert count == 3

    def test_count_gold_empty(self):
        """Test counting gold when none is in inventory"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        gold = warrior.count_gold()

        # Assert
        assert gold == 0

    def test_count_gold_single_item(self):
        """Test counting gold from a single gold item"""
        # Arrange
        warrior = Warrior(5, 5)
        gold_item = Item("Gold Coins", ItemType.MISC, "Currency", gold_value=100)
        warrior.inventory.add_item(gold_item)

        # Act
        gold = warrior.count_gold()

        # Assert
        assert gold == 100

    def test_count_gold_multiple_items(self):
        """Test counting gold from multiple gold items"""
        # Arrange
        warrior = Warrior(5, 5)
        gold1 = Item("Gold Coins", ItemType.MISC, "Currency", gold_value=50)
        gold2 = Item("Gold Pouch", ItemType.MISC, "Currency", gold_value=30)
        warrior.inventory.add_item(gold1)
        warrior.inventory.add_item(gold2)

        # Act
        gold = warrior.count_gold()

        # Assert
        assert gold == 80

    def test_count_gold_ignores_non_gold_items(self):
        """Test that count_gold ignores items without gold_value"""
        # Arrange
        warrior = Warrior(5, 5)
        gold_item = Item("Gold Coins", ItemType.MISC, "Currency", gold_value=50)
        misc_item = Item("Key", ItemType.MISC, "Opens doors")
        warrior.inventory.add_item(gold_item)
        warrior.inventory.add_item(misc_item)

        # Act
        gold = warrior.count_gold()

        # Assert
        assert gold == 50
