"""Tests for warrior.py - Warrior class"""

import pytest
from unittest.mock import Mock, patch
import pygame
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.entities.entity import Entity
from caislean_gaofar.objects.item import Item, ItemType
from caislean_gaofar.core import config


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
        assert result["success"] is True
        assert result["damage"] == config.WARRIOR_ATTACK_DAMAGE
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
        assert result["success"] is True
        assert result["damage"] == config.WARRIOR_ATTACK_DAMAGE + 10
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
        assert result["success"] is False
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
        assert result["success"] is False

    def test_execute_turn_move_action(self):
        """Test execute_turn with move action"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.queue_movement(1, 0)

        # Act
        result = warrior.execute_turn()

        # Assert
        assert result["success"] is True
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
        assert result["success"] is True
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
        assert result["success"] is True
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
        assert result["success"] is True
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
        assert result["success"] is False
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
        assert result["success"] is False
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
        assert result["success"] is False
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
        assert warrior.inventory.backpack_slots == [None] * 10

    def test_execute_turn_unknown_action_type(self):
        """Test execute_turn with unknown action type returns False"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.pending_action = ("unknown",)

        # Act
        result = warrior.execute_turn()

        # Assert
        assert result["success"] is False

    def test_use_health_potion_success(self):
        """Test using health potion successfully restores health"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.health = 50
        # Add health potion to inventory
        potion = Item("Health Potion", ItemType.CONSUMABLE, "Restores 30 HP")
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
        potion = Item("Health Potion", ItemType.CONSUMABLE, "Restores 30 HP")
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
        potion = Item("Health Potion", ItemType.CONSUMABLE, "Restores 30 HP")
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
        potion1 = Item("Health Potion", ItemType.CONSUMABLE, "Restores HP")
        potion2 = Item("Health Potion", ItemType.CONSUMABLE, "Restores HP")
        potion3 = Item("Health Potion", ItemType.CONSUMABLE, "Restores HP")
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
        town_portal = Item("Town Portal", ItemType.CONSUMABLE, "Opens a portal to town")
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
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town"
        )
        town_portal2 = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town"
        )
        town_portal3 = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town"
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
        health_potion = Item("Health Potion", ItemType.CONSUMABLE, "Restores health")
        town_portal = Item("Town Portal", ItemType.CONSUMABLE, "Opens a portal to town")
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
        town_portal = Item("Town Portal", ItemType.CONSUMABLE, "Opens a portal to town")
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
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town"
        )
        town_portal2 = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town"
        )
        town_portal3 = Item(
            "Town Portal", ItemType.CONSUMABLE, "Opens a portal to town"
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
        health_potion = Item("Health Potion", ItemType.CONSUMABLE, "Restores health")
        town_portal = Item("Town Portal", ItemType.CONSUMABLE, "Opens a portal to town")
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
        health_potion = Item("Health Potion", ItemType.CONSUMABLE, "Restores health")
        town_portal = Item("Town Portal", ItemType.CONSUMABLE, "Opens a portal to town")
        warrior.inventory.add_item(town_portal)
        warrior.inventory.add_item(health_potion)

        # Act
        result = warrior.use_health_potion()

        # Assert
        assert result is True
        assert warrior.count_town_portals() == 1  # Portal should remain
        assert warrior.count_health_potions() == 0  # Potion should be consumed


class TestWarriorLevelUpHPBonus:
    """Tests for HP bonus on level up"""

    def test_gain_experience_increases_max_hp_on_level_up(self):
        """Test that leveling up increases max HP"""
        # Arrange
        warrior = Warrior(5, 5)
        initial_max_hp = warrior.max_health

        # Act - Gain enough XP to level up to level 2
        warrior.gain_experience(100)

        # Assert
        assert warrior.experience.current_level == 2
        assert warrior.max_health == initial_max_hp + config.WARRIOR_HP_PER_LEVEL

    def test_gain_experience_restores_full_hp_on_level_up(self):
        """Test that leveling up restores full HP"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.health = 50  # Damage the warrior

        # Act - Gain enough XP to level up
        warrior.gain_experience(100)

        # Assert
        assert warrior.health == warrior.max_health

    def test_gain_experience_multiple_levels_applies_correct_hp_bonus(self):
        """Test that gaining multiple levels applies correct HP bonus"""
        # Arrange
        warrior = Warrior(5, 5)
        initial_max_hp = warrior.max_health

        # Act - Gain enough XP to jump from level 1 to level 5
        warrior.gain_experience(1000)

        # Assert
        assert warrior.experience.current_level == 5
        # Should gain HP for 4 level ups (2, 3, 4, 5)
        expected_hp = initial_max_hp + (config.WARRIOR_HP_PER_LEVEL * 4)
        assert warrior.max_health == expected_hp
        assert warrior.health == warrior.max_health

    def test_gain_experience_no_level_up_no_hp_bonus(self):
        """Test that gaining XP without leveling up doesn't change HP"""
        # Arrange
        warrior = Warrior(5, 5)
        initial_max_hp = warrior.max_health
        initial_hp = warrior.health

        # Act - Gain some XP but not enough to level up
        warrior.gain_experience(50)

        # Assert
        assert warrior.experience.current_level == 1
        assert warrior.max_health == initial_max_hp
        assert warrior.health == initial_hp

    def test_gain_experience_at_max_level_no_hp_bonus(self):
        """Test that gaining XP at max level doesn't increase HP"""
        # Arrange
        warrior = Warrior(5, 5)
        # Level up to max level
        warrior.gain_experience(1000)
        max_level_hp = warrior.max_health

        # Act - Gain more XP at max level
        warrior.gain_experience(500)

        # Assert
        assert warrior.experience.current_level == 5
        assert warrior.max_health == max_level_hp  # No change

    def test_hp_bonus_applies_correctly_per_level(self):
        """Test that each level up applies exactly WARRIOR_HP_PER_LEVEL bonus"""
        # Arrange
        warrior = Warrior(5, 5)
        initial_max_hp = warrior.max_health

        # Act & Assert - Level up one at a time
        # Level 1 -> 2
        warrior.gain_experience(100)
        assert warrior.max_health == initial_max_hp + config.WARRIOR_HP_PER_LEVEL

        # Level 2 -> 3
        level_2_hp = warrior.max_health
        warrior.gain_experience(150)  # 250 total
        assert warrior.max_health == level_2_hp + config.WARRIOR_HP_PER_LEVEL

        # Level 3 -> 4
        level_3_hp = warrior.max_health
        warrior.gain_experience(250)  # 500 total
        assert warrior.max_health == level_3_hp + config.WARRIOR_HP_PER_LEVEL

        # Level 4 -> 5
        level_4_hp = warrior.max_health
        warrior.gain_experience(500)  # 1000 total
        assert warrior.max_health == level_4_hp + config.WARRIOR_HP_PER_LEVEL


class TestWarriorSkillBonuses:
    """Tests for warrior skill bonuses"""

    def test_berserker_rage_passive_activates_below_50_percent_hp(self):
        """Test that Berserker Rage passive gives +25% attack below 50% HP"""
        # Arrange
        warrior = Warrior(5, 5)
        base_damage = warrior.get_effective_attack_damage()

        # Learn Berserker Rage skill
        warrior.skills.learn_skill("berserker_rage")

        # Act - Damage warrior below 50% HP
        warrior.health = warrior.max_health * 0.4  # 40% HP

        # Assert - Should have +25% attack
        boosted_damage = warrior.get_effective_attack_damage()
        assert boosted_damage == int(base_damage * 1.25)

    def test_berserker_rage_passive_not_active_above_50_percent_hp(self):
        """Test that Berserker Rage passive doesn't activate above 50% HP"""
        # Arrange
        warrior = Warrior(5, 5)
        base_damage = warrior.get_effective_attack_damage()

        # Learn Berserker Rage skill
        warrior.skills.learn_skill("berserker_rage")

        # Act - Keep HP above 50%
        warrior.health = warrior.max_health * 0.6  # 60% HP

        # Assert - Should have normal damage
        damage = warrior.get_effective_attack_damage()
        assert damage == base_damage

    def test_battle_hardened_passive_gives_crit_chance_above_75_percent_hp(self):
        """Test that Battle Hardened passive gives +10% crit above 75% HP"""
        # Arrange
        warrior = Warrior(5, 5)

        # Learn Battle Hardened skill
        warrior.skills.learn_skill("battle_hardened")

        # Act - Keep HP above 75%
        warrior.health = warrior.max_health * 0.8  # 80% HP

        # Assert - Should have 10% crit chance
        crit_chance = warrior.get_crit_chance()
        assert crit_chance == 0.10

    def test_battle_hardened_passive_no_crit_below_75_percent_hp(self):
        """Test that Battle Hardened passive doesn't activate below 75% HP"""
        # Arrange
        warrior = Warrior(5, 5)

        # Learn Battle Hardened skill
        warrior.skills.learn_skill("battle_hardened")

        # Act - Damage to below 75%
        warrior.health = warrior.max_health * 0.5  # 50% HP

        # Assert - Should have 0% crit chance
        crit_chance = warrior.get_crit_chance()
        assert crit_chance == 0.0

    def test_iron_skin_passive_gives_damage_reduction(self):
        """Test that Iron Skin passive gives 10% damage reduction"""
        # Arrange
        warrior = Warrior(5, 5)

        # Learn Iron Skin skill
        warrior.skills.learn_skill("iron_skin")

        # Act
        reduction = warrior.get_damage_reduction()

        # Assert - Should have 10% damage reduction
        assert reduction == 0.10

    def test_last_stand_passive_triggers_at_low_hp(self):
        """Test that Last Stand passive activates at <= 20% HP"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.skills.learn_skill("last_stand")

        # Act - Take damage to 20% HP
        warrior.health = int(warrior.max_health * 0.2)
        warrior.take_damage(5)  # This should trigger Last Stand

        # Assert - Should have emergency shield (30% max HP)
        expected_hp = int(warrior.max_health * 0.2) - 5 + int(warrior.max_health * 0.3)
        assert warrior.health == expected_hp
        assert warrior.skills.last_stand_used is True

    def test_last_stand_passive_only_triggers_once(self):
        """Test that Last Stand passive only triggers once per battle"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.skills.learn_skill("last_stand")

        # Act - Trigger Last Stand first time
        warrior.health = int(warrior.max_health * 0.2)
        warrior.take_damage(5)

        # Damage again to low HP
        warrior.health = 10
        warrior.take_damage(5)

        # Assert - Last Stand should not trigger again
        assert warrior.health == 5  # Just took 5 damage, no shield

    def test_last_stand_passive_does_not_trigger_above_threshold(self):
        """Test that Last Stand doesn't trigger when health stays above 20%"""
        # Arrange
        warrior = Warrior(5, 5)
        warrior.skills.learn_skill("last_stand")

        # Act - Take damage but stay above 20% HP
        warrior.health = warrior.max_health  # Full health
        initial_health = warrior.health
        warrior.take_damage(10)  # Small damage

        # Assert - Last Stand should NOT trigger (health still above 20%)
        assert warrior.health == initial_health - 10
        assert warrior.skills.last_stand_used is False

    def test_vampiric_strikes_passive_heals_on_damage(self):
        """Test that Vampiric Strikes passive heals for 15% of damage dealt"""
        # Arrange
        warrior = Warrior(5, 5)

        target = Entity(10, 10, 32, (255, 0, 0), 100, 1, 10, 1)

        # Learn Vampiric Strikes skill
        warrior.skills.learn_skill("vampiric_strikes")

        # Damage warrior first
        warrior.health = 50

        # Act - Attack target
        result = warrior.attack(target)

        # Assert - Should heal for 15% of damage
        expected_heal = int(result["damage"] * 0.15)
        assert result["healed"] == expected_heal
        assert warrior.health == 50 + expected_heal


class TestWarriorActiveSkills:
    """Tests for warrior active skills"""

    def test_attack_with_skill_on_cooldown_uses_basic_attack(self):
        """Test that trying to use skill on cooldown falls back to basic attack"""
        # Arrange
        warrior = Warrior(5, 5)
        from unittest.mock import patch

        target = Entity(10, 10, 32, (255, 0, 0), 100, 1, 10, 1)

        # Learn and set Power Strike as active
        warrior.skills.learn_skill("power_strike")
        warrior.skills.set_active_skill("power_strike")

        # Act - Attack with skill, but mock it as on cooldown
        with patch.object(
            warrior.skills.learned_skills["power_strike"], "can_use", return_value=False
        ):
            result = warrior.attack(target, use_skill=True)

        # Assert - Should use basic attack (no skill)
        assert result["success"] is True
        assert result["skill_used"] is None


class TestWarriorCriticalHits:
    """Tests for critical hit mechanics"""

    def test_critical_hit_deals_150_percent_damage(self):
        """Test that critical hits deal 1.5x damage"""
        # Arrange
        warrior = Warrior(5, 5)
        from unittest.mock import patch

        target = Entity(10, 10, 32, (255, 0, 0), 100, 1, 10, 1)

        # Give warrior crit chance
        warrior.skills.learn_skill("battle_hardened")
        warrior.health = warrior.max_health  # Full HP for 10% crit

        base_damage = warrior.get_effective_attack_damage()

        # Make sure warrior can attack
        warrior.turns_since_last_attack = warrior.attack_cooldown

        # Act - Mock random to always crit
        with patch("random.random", return_value=0.05):  # Below 10% threshold
            result = warrior.attack(target)

        # Assert - Should deal 1.5x damage
        assert result["success"] is True
        assert result["crit"] is True
        assert result["damage"] == int(base_damage * 1.5)

    def test_no_critical_hit_deals_normal_damage(self):
        """Test that non-crits deal normal damage"""
        # Arrange
        warrior = Warrior(5, 5)
        from unittest.mock import patch

        target = Entity(10, 10, 32, (255, 0, 0), 100, 1, 10, 1)

        # Give warrior crit chance
        warrior.skills.learn_skill("battle_hardened")
        warrior.health = warrior.max_health  # Full HP for 10% crit

        base_damage = warrior.get_effective_attack_damage()

        # Make sure warrior can attack
        warrior.turns_since_last_attack = warrior.attack_cooldown

        # Act - Mock random to not crit
        with patch("random.random", return_value=0.15):  # Above 10% threshold
            result = warrior.attack(target)

        # Assert - Should deal normal damage
        assert result["success"] is True
        assert result["crit"] is False
        assert result["damage"] == base_damage


class TestWarriorActiveSkillDamageMultipliers:
    """Tests for active skill damage multipliers in warrior attack"""

    def test_power_strike_damage_multiplier(self):
        """Test that Power Strike applies 1.5x damage multiplier"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(10, 10, 32, (255, 0, 0), 100, 1, 10, 1)

        # Learn and set active skill
        warrior.skills.learn_skill("power_strike")
        warrior.skills.set_active_skill("power_strike")

        # Make warrior able to attack
        warrior.turns_since_last_attack = warrior.attack_cooldown

        base_damage = warrior.get_effective_attack_damage()

        # Mock can_use to return True to bypass cooldown
        with patch.object(
            warrior.skills.get_active_skill(), "can_use", return_value=True
        ):
            # Act
            result = warrior.attack(target, use_skill=True)

        # Assert - Should apply 1.5x multiplier
        assert result["success"] is True
        assert result["skill_used"] == "Power Strike"
        assert result["damage"] == int(base_damage * 1.5)

    def test_shield_bash_damage_multiplier(self):
        """Test that Shield Bash applies 0.75x damage multiplier"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(10, 10, 32, (255, 0, 0), 100, 1, 10, 1)

        # Learn and set active skill
        warrior.skills.learn_skill("shield_bash")
        warrior.skills.set_active_skill("shield_bash")

        # Make warrior able to attack
        warrior.turns_since_last_attack = warrior.attack_cooldown

        base_damage = warrior.get_effective_attack_damage()

        # Mock can_use to return True to bypass cooldown
        with patch.object(
            warrior.skills.get_active_skill(), "can_use", return_value=True
        ):
            # Act
            result = warrior.attack(target, use_skill=True)

        # Assert - Should apply 0.75x multiplier
        assert result["success"] is True
        assert result["skill_used"] == "Shield Bash"
        assert result["damage"] == int(base_damage * 0.75)

    def test_whirlwind_damage_multiplier(self):
        """Test that Whirlwind applies 1.0x damage multiplier"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(10, 10, 32, (255, 0, 0), 100, 1, 10, 1)

        # Learn and set active skill
        warrior.skills.learn_skill("whirlwind")
        warrior.skills.set_active_skill("whirlwind")

        # Make warrior able to attack
        warrior.turns_since_last_attack = warrior.attack_cooldown

        base_damage = warrior.get_effective_attack_damage()

        # Mock can_use to return True to bypass cooldown
        with patch.object(
            warrior.skills.get_active_skill(), "can_use", return_value=True
        ):
            # Act
            result = warrior.attack(target, use_skill=True)

        # Assert - Should apply 1.0x multiplier (normal damage)
        assert result["success"] is True
        assert result["skill_used"] == "Whirlwind"
        assert result["damage"] == int(base_damage * 1.0)

    def test_cleave_damage_multiplier(self):
        """Test that Cleave applies 2.0x damage multiplier"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(10, 10, 32, (255, 0, 0), 100, 1, 10, 1)

        # Learn and set active skill (need to be level 4 for Cleave)
        warrior.gain_experience(500)  # Level up to 4
        warrior.skills.learn_skill("cleave")
        warrior.skills.set_active_skill("cleave")

        # Make warrior able to attack
        warrior.turns_since_last_attack = warrior.attack_cooldown

        base_damage = warrior.get_effective_attack_damage()

        # Mock can_use to return True to bypass cooldown
        with patch.object(
            warrior.skills.get_active_skill(), "can_use", return_value=True
        ):
            # Act
            result = warrior.attack(target, use_skill=True)

        # Assert - Should apply 2.0x multiplier
        assert result["success"] is True
        assert result["skill_used"] == "Cleave"
        assert result["damage"] == int(base_damage * 2.0)

    def test_earthsplitter_damage_multiplier(self):
        """Test that Earthsplitter applies 2.5x damage multiplier"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(10, 10, 32, (255, 0, 0), 100, 1, 10, 1)

        # Learn and set active skill (need to be level 5 for Earthsplitter)
        warrior.gain_experience(1000)  # Level up to 5
        warrior.skills.learn_skill("earthsplitter")
        warrior.skills.set_active_skill("earthsplitter")

        # Make warrior able to attack
        warrior.turns_since_last_attack = warrior.attack_cooldown

        base_damage = warrior.get_effective_attack_damage()

        # Mock can_use to return True to bypass cooldown
        with patch.object(
            warrior.skills.get_active_skill(), "can_use", return_value=True
        ):
            # Act
            result = warrior.attack(target, use_skill=True)

        # Assert - Should apply 2.5x multiplier
        assert result["success"] is True
        assert result["skill_used"] == "Earthsplitter"
        assert result["damage"] == int(base_damage * 2.5)

    def test_skill_on_cooldown_uses_basic_attack(self):
        """Test that when skill is on cooldown, basic attack is used instead"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(10, 10, 32, (255, 0, 0), 100, 1, 10, 1)

        # Learn and set active skill
        warrior.skills.learn_skill("power_strike")
        warrior.skills.set_active_skill("power_strike")

        # Make warrior able to attack
        warrior.turns_since_last_attack = warrior.attack_cooldown

        base_damage = warrior.get_effective_attack_damage()

        # Mock can_use to return False (skill on cooldown)
        with patch.object(
            warrior.skills.get_active_skill(), "can_use", return_value=False
        ):
            # Act
            result = warrior.attack(target, use_skill=True)

        # Assert - Should use basic attack (no skill, normal damage)
        assert result["success"] is True
        assert result.get("skill_used") is None
        assert result["damage"] == base_damage

    def test_unknown_skill_name_uses_default_multiplier(self):
        """Test that an unknown skill name uses 1.0x damage multiplier"""
        # Arrange
        warrior = Warrior(5, 5)
        target = Entity(10, 10, 32, (255, 0, 0), 100, 1, 10, 1)

        # Learn a skill and set it as active
        warrior.skills.learn_skill("power_strike")
        warrior.skills.set_active_skill("power_strike")

        # Make warrior able to attack
        warrior.turns_since_last_attack = warrior.attack_cooldown

        base_damage = warrior.get_effective_attack_damage()

        # Mock the active skill to have an unknown name
        mock_skill = Mock()
        mock_skill.name = "UnknownSkill"
        mock_skill.can_use = Mock(return_value=True)
        mock_skill.use = Mock()

        # Act - Mock get_active_skill to return our mock skill
        with patch.object(warrior.skills, "get_active_skill", return_value=mock_skill):
            result = warrior.attack(target, use_skill=True)

        # Assert - Should use 1.0x multiplier (default)
        assert result["success"] is True
        assert result["skill_used"] == "UnknownSkill"
        assert result["damage"] == int(base_damage * 1.0)


class TestWarriorDefense:
    """Tests for warrior defense mechanics"""

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
