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
        assert warrior.inventory.backpack_slots == [None] * 13

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
        """Test counting gold when none has been added"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        gold = warrior.count_gold()

        # Assert
        assert gold == 0

    def test_add_gold(self):
        """Test adding gold to warrior's currency"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        warrior.add_gold(100)
        gold = warrior.count_gold()

        # Assert
        assert gold == 100

    def test_add_gold_multiple_times(self):
        """Test adding gold multiple times accumulates"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        warrior.add_gold(50)
        warrior.add_gold(30)
        gold = warrior.count_gold()

        # Assert
        assert gold == 80

    def test_remove_gold_success(self):
        """Test removing gold when enough is available"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.add_gold(100)

        # Act
        success = warrior.remove_gold(50)

        # Assert
        assert success is True
        assert warrior.count_gold() == 50

    def test_remove_gold_failure(self):
        """Test removing gold when not enough is available"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.add_gold(30)

        # Act
        success = warrior.remove_gold(50)

        # Assert
        assert success is False
        assert warrior.count_gold() == 30

    def test_count_town_portals_empty(self):
        """Test counting town portals when inventory is empty"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        count = warrior.count_town_portals()

        # Assert
        assert count == 0

    def test_count_town_portals_single(self):
        """Test counting town portals with one portal"""
        # Arrange
        warrior = Warrior(5, 5)
        town_portal = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town", health_bonus=0
        )
        warrior.inventory.add_item(town_portal)

        # Act
        count = warrior.count_town_portals()

        # Assert
        assert count == 1

    def test_count_town_portals_multiple(self):
        """Test counting town portals with multiple portals"""
        # Arrange
        warrior = Warrior(5, 5)
        # Add 3 town portals
        town_portal1 = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town", health_bonus=0
        )
        town_portal2 = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town", health_bonus=0
        )
        town_portal3 = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town", health_bonus=0
        )
        warrior.inventory.add_item(town_portal1)
        warrior.inventory.add_item(town_portal2)
        warrior.inventory.add_item(town_portal3)

        # Act
        count = warrior.count_town_portals()

        # Assert
        assert count == 3

    def test_count_town_portals_mixed_with_potions(self):
        """Test counting town portals with health potions in inventory"""
        # Arrange
        warrior = Warrior(5, 5)
        health_potion = Item(
            "Health Potion", ItemType.CONSUMABLE, "Restores health", health_bonus=30
        )
        town_portal = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town", health_bonus=0
        )
        warrior.inventory.add_item(health_potion)
        warrior.inventory.add_item(town_portal)
        warrior.inventory.add_item(health_potion)

        # Act
        portal_count = warrior.count_town_portals()
        potion_count = warrior.count_health_potions()

        # Assert
        assert portal_count == 1
        assert potion_count == 2

    def test_use_town_portal_success(self):
        """Test using a town portal successfully"""
        # Arrange
        warrior = Warrior(5, 5)
        town_portal = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town", health_bonus=0
        )
        warrior.inventory.add_item(town_portal)

        # Act
        result = warrior.use_town_portal()

        # Assert
        assert result is True
        assert warrior.count_town_portals() == 0

    def test_use_town_portal_no_portals(self):
        """Test using a town portal when none available"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        result = warrior.use_town_portal()

        # Assert
        assert result is False

    def test_use_town_portal_uses_first_portal(self):
        """Test that using portal removes the first one"""
        # Arrange
        warrior = Warrior(5, 5)
        # Add 3 town portals
        town_portal1 = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town", health_bonus=0
        )
        town_portal2 = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town", health_bonus=0
        )
        town_portal3 = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town", health_bonus=0
        )
        warrior.inventory.add_item(town_portal1)
        warrior.inventory.add_item(town_portal2)
        warrior.inventory.add_item(town_portal3)

        # Act
        result = warrior.use_town_portal()

        # Assert
        assert result is True
        assert warrior.count_town_portals() == 2

    def test_count_health_potions_excludes_town_portals(self):
        """Test that health potion count excludes town portals"""
        # Arrange
        warrior = Warrior(5, 5)
        health_potion = Item(
            "Health Potion", ItemType.CONSUMABLE, "Restores health", health_bonus=30
        )
        town_portal = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town", health_bonus=0
        )
        warrior.inventory.add_item(health_potion)
        warrior.inventory.add_item(town_portal)

        # Act
        potion_count = warrior.count_health_potions()

        # Assert
        assert potion_count == 1

    def test_use_health_potion_ignores_town_portals(self):
        """Test that using health potion doesn't consume town portals"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.health = 50  # Damage warrior
        health_potion = Item(
            "Health Potion", ItemType.CONSUMABLE, "Restores health", health_bonus=30
        )
        town_portal = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town", health_bonus=0
        )
        warrior.inventory.add_item(town_portal)
        warrior.inventory.add_item(health_potion)

        # Act
        result = warrior.use_health_potion()

        # Assert
        assert result is True
        assert warrior.count_town_portals() == 1  # Portal should remain
        assert warrior.count_health_potions() == 0  # Potion should be consumed

    def test_get_effective_defense_no_equipment(self):
        """Test effective defense with no equipment"""
        # Arrange
        warrior = Warrior(5, 5)

        # Act
        defense = warrior.get_effective_defense()

        # Assert
        assert defense == 0

    def test_get_effective_defense_with_armor(self):
        """Test effective defense with armor equipped"""
        # Arrange
        warrior = Warrior(5, 5)
        armor = Item("Shield", ItemType.ARMOR, defense_bonus=10)
        warrior.inventory.add_item(armor)

        # Act
        defense = warrior.get_effective_defense()

        # Assert
        assert defense == 10

    def test_get_effective_defense_with_weapon_and_armor(self):
        """Test effective defense with both weapon and armor"""
        # Arrange
        warrior = Warrior(5, 5)
        weapon = Item("Sword", ItemType.WEAPON, defense_bonus=2)
        armor = Item("Shield", ItemType.ARMOR, defense_bonus=10)
        warrior.inventory.add_item(weapon)
        warrior.inventory.add_item(armor)

        # Act
        defense = warrior.get_effective_defense()

        # Assert
        assert defense == 12

    def test_take_damage_with_defense_bonus(self):
        """Test taking damage with defense bonus reduces damage"""
        # Arrange
        warrior = Warrior(5, 5)
        armor = Item("Shield", ItemType.ARMOR, defense_bonus=5)
        warrior.inventory.add_item(armor)
        initial_health = warrior.health

        # Act
        warrior.take_damage(10)

        # Assert - Should take 10 - 5 = 5 damage
        assert warrior.health == initial_health - 5

    def test_take_damage_with_high_defense_minimum_damage(self):
        """Test that defense can't reduce damage below 1"""
        # Arrange
        warrior = Warrior(5, 5)
        armor = Item("Super Shield", ItemType.ARMOR, defense_bonus=100)
        warrior.inventory.add_item(armor)
        initial_health = warrior.health

        # Act
        warrior.take_damage(10)

        # Assert - Should take at least 1 damage
        assert warrior.health == initial_health - 1
