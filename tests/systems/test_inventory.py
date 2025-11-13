"""Tests for inventory.py - Inventory class"""

from caislean_gaofar.systems.inventory import Inventory
from caislean_gaofar.objects.item import Item, ItemType


class TestInventory:
    """Tests for Inventory class"""

    def test_inventory_initialization(self):
        """Test Inventory initialization with empty slots"""
        # Arrange & Act
        inventory = Inventory()

        # Assert
        assert inventory.weapon_slot is None
        assert inventory.armor_slot is None
        assert inventory.backpack_slots == [None] * 13

    def test_add_item_weapon_to_empty_weapon_slot(self):
        """Test adding weapon to empty weapon slot"""
        # Arrange
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON)

        # Act
        result = inventory.add_item(weapon)

        # Assert
        assert result is True
        assert inventory.weapon_slot == weapon

    def test_add_item_armor_to_empty_armor_slot(self):
        """Test adding armor to empty armor slot"""
        # Arrange
        inventory = Inventory()
        armor = Item("Shield", ItemType.ARMOR)

        # Act
        result = inventory.add_item(armor)

        # Assert
        assert result is True
        assert inventory.armor_slot == armor

    def test_add_item_weapon_when_weapon_slot_full(self):
        """Test adding weapon when weapon slot is full goes to backpack"""
        # Arrange
        inventory = Inventory()
        weapon1 = Item("Sword", ItemType.WEAPON)
        weapon2 = Item("Axe", ItemType.WEAPON)
        inventory.add_item(weapon1)

        # Act
        result = inventory.add_item(weapon2)

        # Assert
        assert result is True
        assert inventory.weapon_slot == weapon1
        assert inventory.backpack_slots[0] == weapon2

    def test_add_item_armor_when_armor_slot_full(self):
        """Test adding armor when armor slot is full goes to backpack"""
        # Arrange
        inventory = Inventory()
        armor1 = Item("Shield", ItemType.ARMOR)
        armor2 = Item("Helmet", ItemType.ARMOR)
        inventory.add_item(armor1)

        # Act
        result = inventory.add_item(armor2)

        # Assert
        assert result is True
        assert inventory.armor_slot == armor1
        assert inventory.backpack_slots[0] == armor2

    def test_add_item_consumable_to_backpack(self):
        """Test adding consumable directly to backpack"""
        # Arrange
        inventory = Inventory()
        consumable = Item("Potion", ItemType.CONSUMABLE)

        # Act
        result = inventory.add_item(consumable)

        # Assert
        assert result is True
        assert inventory.backpack_slots[0] == consumable

    def test_add_item_misc_to_backpack(self):
        """Test adding misc item directly to backpack"""
        # Arrange
        inventory = Inventory()
        misc = Item("Key", ItemType.MISC)

        # Act
        result = inventory.add_item(misc)

        # Assert
        assert result is True
        assert inventory.backpack_slots[0] == misc

    def test_add_item_fills_backpack_slots_sequentially(self):
        """Test adding items fills backpack slots in order"""
        # Arrange
        inventory = Inventory()
        item1 = Item("Item1", ItemType.MISC)
        item2 = Item("Item2", ItemType.MISC)
        item3 = Item("Item3", ItemType.MISC)

        # Act
        inventory.add_item(item1)
        inventory.add_item(item2)
        inventory.add_item(item3)

        # Assert
        assert inventory.backpack_slots[0] == item1
        assert inventory.backpack_slots[1] == item2
        assert inventory.backpack_slots[2] == item3

    def test_add_item_when_inventory_full(self):
        """Test adding item when inventory is completely full"""
        # Arrange
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON)
        inventory.armor_slot = Item("Shield", ItemType.ARMOR)
        inventory.backpack_slots = [
            Item("Item1", ItemType.MISC),
            Item("Item2", ItemType.MISC),
            Item("Item3", ItemType.MISC),
            Item("Item4", ItemType.MISC),
            Item("Item5", ItemType.MISC),
        ]
        new_item = Item("Item6", ItemType.MISC)

        # Act
        result = inventory.add_item(new_item)

        # Assert
        assert result is False

    def test_remove_item_from_weapon_slot(self):
        """Test removing item from weapon slot"""
        # Arrange
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON)
        inventory.weapon_slot = weapon

        # Act
        removed_item = inventory.remove_item_from_slot("weapon")

        # Assert
        assert removed_item == weapon
        assert inventory.weapon_slot is None

    def test_remove_item_from_empty_weapon_slot(self):
        """Test removing item from empty weapon slot"""
        # Arrange
        inventory = Inventory()

        # Act
        removed_item = inventory.remove_item_from_slot("weapon")

        # Assert
        assert removed_item is None

    def test_remove_item_from_armor_slot(self):
        """Test removing item from armor slot"""
        # Arrange
        inventory = Inventory()
        armor = Item("Shield", ItemType.ARMOR)
        inventory.armor_slot = armor

        # Act
        removed_item = inventory.remove_item_from_slot("armor")

        # Assert
        assert removed_item == armor
        assert inventory.armor_slot is None

    def test_remove_item_from_empty_armor_slot(self):
        """Test removing item from empty armor slot"""
        # Arrange
        inventory = Inventory()

        # Act
        removed_item = inventory.remove_item_from_slot("armor")

        # Assert
        assert removed_item is None

    def test_remove_item_from_backpack_slot_0(self):
        """Test removing item from backpack slot 0"""
        # Arrange
        inventory = Inventory()
        item = Item("Item", ItemType.MISC)
        inventory.backpack_slots[0] = item

        # Act
        removed_item = inventory.remove_item_from_slot("backpack", 0)

        # Assert
        assert removed_item == item
        assert inventory.backpack_slots[0] is None

    def test_remove_item_from_backpack_slot_1(self):
        """Test removing item from backpack slot 1"""
        # Arrange
        inventory = Inventory()
        item = Item("Item", ItemType.MISC)
        inventory.backpack_slots[1] = item

        # Act
        removed_item = inventory.remove_item_from_slot("backpack", 1)

        # Assert
        assert removed_item == item
        assert inventory.backpack_slots[1] is None

    def test_remove_item_from_backpack_slot_2(self):
        """Test removing item from backpack slot 2"""
        # Arrange
        inventory = Inventory()
        item = Item("Item", ItemType.MISC)
        inventory.backpack_slots[2] = item

        # Act
        removed_item = inventory.remove_item_from_slot("backpack", 2)

        # Assert
        assert removed_item == item
        assert inventory.backpack_slots[2] is None

    def test_remove_item_from_backpack_slot_3(self):
        """Test removing item from backpack slot 3"""
        # Arrange
        inventory = Inventory()
        item = Item("Item", ItemType.MISC)
        inventory.backpack_slots[3] = item

        # Act
        removed_item = inventory.remove_item_from_slot("backpack", 3)

        # Assert
        assert removed_item == item
        assert inventory.backpack_slots[3] is None

    def test_remove_item_from_backpack_slot_4(self):
        """Test removing item from backpack slot 4"""
        # Arrange
        inventory = Inventory()
        item = Item("Item", ItemType.MISC)
        inventory.backpack_slots[4] = item

        # Act
        removed_item = inventory.remove_item_from_slot("backpack", 4)

        # Assert
        assert removed_item == item
        assert inventory.backpack_slots[4] is None

    def test_remove_item_from_empty_backpack_slot(self):
        """Test removing item from empty backpack slot"""
        # Arrange
        inventory = Inventory()

        # Act
        removed_item = inventory.remove_item_from_slot("backpack", 0)

        # Assert
        assert removed_item is None

    def test_remove_item_from_backpack_invalid_index_negative(self):
        """Test removing item with negative backpack index"""
        # Arrange
        inventory = Inventory()

        # Act
        removed_item = inventory.remove_item_from_slot("backpack", -1)

        # Assert
        assert removed_item is None

    def test_remove_item_from_backpack_invalid_index_too_large(self):
        """Test removing item with too large backpack index"""
        # Arrange
        inventory = Inventory()

        # Act
        removed_item = inventory.remove_item_from_slot("backpack", 13)

        # Assert
        assert removed_item is None

    def test_remove_item_invalid_slot_type(self):
        """Test removing item with invalid slot type"""
        # Arrange
        inventory = Inventory()

        # Act
        removed_item = inventory.remove_item_from_slot("invalid")

        # Assert
        assert removed_item is None

    def test_equip_from_backpack_weapon(self):
        """Test equipping weapon from backpack to empty weapon slot"""
        # Arrange
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON)
        inventory.backpack_slots[0] = weapon

        # Act
        result = inventory.equip_from_backpack(0)

        # Assert
        assert result is True
        assert inventory.weapon_slot == weapon
        assert inventory.backpack_slots[0] is None

    def test_equip_from_backpack_weapon_swap(self):
        """Test equipping weapon from backpack swaps with current weapon"""
        # Arrange
        inventory = Inventory()
        old_weapon = Item("Sword", ItemType.WEAPON)
        new_weapon = Item("Axe", ItemType.WEAPON)
        inventory.weapon_slot = old_weapon
        inventory.backpack_slots[0] = new_weapon

        # Act
        result = inventory.equip_from_backpack(0)

        # Assert
        assert result is True
        assert inventory.weapon_slot == new_weapon
        assert inventory.backpack_slots[0] == old_weapon

    def test_equip_from_backpack_armor(self):
        """Test equipping armor from backpack to empty armor slot"""
        # Arrange
        inventory = Inventory()
        armor = Item("Shield", ItemType.ARMOR)
        inventory.backpack_slots[1] = armor

        # Act
        result = inventory.equip_from_backpack(1)

        # Assert
        assert result is True
        assert inventory.armor_slot == armor
        assert inventory.backpack_slots[1] is None

    def test_equip_from_backpack_armor_swap(self):
        """Test equipping armor from backpack swaps with current armor"""
        # Arrange
        inventory = Inventory()
        old_armor = Item("Shield", ItemType.ARMOR)
        new_armor = Item("Helmet", ItemType.ARMOR)
        inventory.armor_slot = old_armor
        inventory.backpack_slots[2] = new_armor

        # Act
        result = inventory.equip_from_backpack(2)

        # Assert
        assert result is True
        assert inventory.armor_slot == new_armor
        assert inventory.backpack_slots[2] == old_armor

    def test_equip_from_backpack_consumable_fails(self):
        """Test equipping consumable from backpack fails"""
        # Arrange
        inventory = Inventory()
        consumable = Item("Potion", ItemType.CONSUMABLE)
        inventory.backpack_slots[0] = consumable

        # Act
        result = inventory.equip_from_backpack(0)

        # Assert
        assert result is False
        assert inventory.backpack_slots[0] == consumable

    def test_equip_from_backpack_misc_fails(self):
        """Test equipping misc item from backpack fails"""
        # Arrange
        inventory = Inventory()
        misc = Item("Key", ItemType.MISC)
        inventory.backpack_slots[0] = misc

        # Act
        result = inventory.equip_from_backpack(0)

        # Assert
        assert result is False
        assert inventory.backpack_slots[0] == misc

    def test_equip_from_backpack_empty_slot_fails(self):
        """Test equipping from empty backpack slot fails"""
        # Arrange
        inventory = Inventory()

        # Act
        result = inventory.equip_from_backpack(0)

        # Assert
        assert result is False

    def test_equip_from_backpack_invalid_index_negative(self):
        """Test equipping with negative index fails"""
        # Arrange
        inventory = Inventory()

        # Act
        result = inventory.equip_from_backpack(-1)

        # Assert
        assert result is False

    def test_equip_from_backpack_invalid_index_too_large(self):
        """Test equipping with too large index fails"""
        # Arrange
        inventory = Inventory()

        # Act
        result = inventory.equip_from_backpack(13)

        # Assert
        assert result is False

    def test_get_total_attack_bonus_no_items(self):
        """Test total attack bonus with no items"""
        # Arrange
        inventory = Inventory()

        # Act
        bonus = inventory.get_total_attack_bonus()

        # Assert
        assert bonus == 0

    def test_get_total_attack_bonus_weapon_only(self):
        """Test total attack bonus with weapon only"""
        # Arrange
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        inventory.weapon_slot = weapon

        # Act
        bonus = inventory.get_total_attack_bonus()

        # Assert
        assert bonus == 10

    def test_get_total_attack_bonus_armor_only(self):
        """Test total attack bonus with armor only"""
        # Arrange
        inventory = Inventory()
        armor = Item("Shield", ItemType.ARMOR, attack_bonus=5)
        inventory.armor_slot = armor

        # Act
        bonus = inventory.get_total_attack_bonus()

        # Assert
        assert bonus == 5

    def test_get_total_attack_bonus_both_items(self):
        """Test total attack bonus with both weapon and armor"""
        # Arrange
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        armor = Item("Shield", ItemType.ARMOR, attack_bonus=5)
        inventory.weapon_slot = weapon
        inventory.armor_slot = armor

        # Act
        bonus = inventory.get_total_attack_bonus()

        # Assert
        assert bonus == 15

    def test_get_total_defense_bonus_no_items(self):
        """Test total defense bonus with no items"""
        # Arrange
        inventory = Inventory()

        # Act
        bonus = inventory.get_total_defense_bonus()

        # Assert
        assert bonus == 0

    def test_get_total_defense_bonus_weapon_only(self):
        """Test total defense bonus with weapon only"""
        # Arrange
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, defense_bonus=2)
        inventory.weapon_slot = weapon

        # Act
        bonus = inventory.get_total_defense_bonus()

        # Assert
        assert bonus == 2

    def test_get_total_defense_bonus_armor_only(self):
        """Test total defense bonus with armor only"""
        # Arrange
        inventory = Inventory()
        armor = Item("Shield", ItemType.ARMOR, defense_bonus=10)
        inventory.armor_slot = armor

        # Act
        bonus = inventory.get_total_defense_bonus()

        # Assert
        assert bonus == 10

    def test_get_total_defense_bonus_both_items(self):
        """Test total defense bonus with both weapon and armor"""
        # Arrange
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON, defense_bonus=2)
        armor = Item("Shield", ItemType.ARMOR, defense_bonus=10)
        inventory.weapon_slot = weapon
        inventory.armor_slot = armor

        # Act
        bonus = inventory.get_total_defense_bonus()

        # Assert
        assert bonus == 12

    def test_has_space_empty_inventory(self):
        """Test has_space returns True for empty inventory"""
        # Arrange
        inventory = Inventory()

        # Act & Assert
        assert inventory.has_space() is True

    def test_has_space_full_inventory(self):  # noqa: PBR008
        """Test has_space returns False for full inventory"""
        # Arrange
        inventory = Inventory()
        inventory.weapon_slot = Item("Sword", ItemType.WEAPON)
        inventory.armor_slot = Item("Shield", ItemType.ARMOR)
        for i in range(13):
            inventory.backpack_slots[i] = Item(f"Item{i}", ItemType.MISC)

        # Act & Assert
        assert inventory.has_space() is False

    def test_contains_item_weapon_slot(self):
        """Test contains_item returns True for weapon in weapon slot"""
        # Arrange
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON)
        inventory.weapon_slot = weapon

        # Act & Assert
        assert inventory.contains_item(weapon) is True

    def test_contains_item_armor_slot(self):
        """Test contains_item returns True for armor in armor slot"""
        # Arrange
        inventory = Inventory()
        armor = Item("Shield", ItemType.ARMOR)
        inventory.armor_slot = armor

        # Act & Assert
        assert inventory.contains_item(armor) is True

    def test_contains_item_backpack(self):
        """Test contains_item returns True for item in backpack"""
        # Arrange
        inventory = Inventory()
        item = Item("Potion", ItemType.CONSUMABLE)
        inventory.backpack_slots[0] = item

        # Act & Assert
        assert inventory.contains_item(item) is True

    def test_contains_item_not_found(self):
        """Test contains_item returns False for item not in inventory"""
        # Arrange
        inventory = Inventory()
        item = Item("Potion", ItemType.CONSUMABLE)

        # Act & Assert
        assert inventory.contains_item(item) is False

    def test_remove_item_weapon_slot(self):
        """Test remove_item removes weapon from weapon slot"""
        # Arrange
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON)
        inventory.weapon_slot = weapon

        # Act
        result = inventory.remove_item(weapon)

        # Assert
        assert result is True
        assert inventory.weapon_slot is None

    def test_remove_item_armor_slot(self):
        """Test remove_item removes armor from armor slot"""
        # Arrange
        inventory = Inventory()
        armor = Item("Shield", ItemType.ARMOR)
        inventory.armor_slot = armor

        # Act
        result = inventory.remove_item(armor)

        # Assert
        assert result is True
        assert inventory.armor_slot is None

    def test_remove_item_backpack(self):
        """Test remove_item removes item from backpack"""
        # Arrange
        inventory = Inventory()
        item = Item("Potion", ItemType.CONSUMABLE)
        inventory.backpack_slots[2] = item

        # Act
        result = inventory.remove_item(item)

        # Assert
        assert result is True
        assert inventory.backpack_slots[2] is None

    def test_remove_item_not_found(self):
        """Test remove_item returns False for item not in inventory"""
        # Arrange
        inventory = Inventory()
        item = Item("Potion", ItemType.CONSUMABLE)

        # Act
        result = inventory.remove_item(item)

        # Assert
        assert result is False

    def test_get_all_items_empty(self):
        """Test get_all_items returns empty list for empty inventory"""
        # Arrange
        inventory = Inventory()

        # Act
        items = inventory.get_all_items()

        # Assert
        assert items == []

    def test_get_all_items_weapon_only(self):
        """Test get_all_items returns weapon only"""
        # Arrange
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON)
        inventory.weapon_slot = weapon

        # Act
        items = inventory.get_all_items()

        # Assert
        assert len(items) == 1
        assert items[0] == weapon

    def test_get_all_items_armor_only(self):
        """Test get_all_items returns armor only"""
        # Arrange
        inventory = Inventory()
        armor = Item("Shield", ItemType.ARMOR)
        inventory.armor_slot = armor

        # Act
        items = inventory.get_all_items()

        # Assert
        assert len(items) == 1
        assert items[0] == armor

    def test_get_all_items_backpack_only(self):
        """Test get_all_items returns backpack items only"""
        # Arrange
        inventory = Inventory()
        item1 = Item("Potion1", ItemType.CONSUMABLE)
        item2 = Item("Potion2", ItemType.CONSUMABLE)
        inventory.backpack_slots[0] = item1
        inventory.backpack_slots[1] = item2

        # Act
        items = inventory.get_all_items()

        # Assert
        assert len(items) == 2
        assert item1 in items
        assert item2 in items

    def test_get_all_items_all_slots(self):
        """Test get_all_items returns all items from all slots"""
        # Arrange
        inventory = Inventory()
        weapon = Item("Sword", ItemType.WEAPON)
        armor = Item("Shield", ItemType.ARMOR)
        item1 = Item("Potion1", ItemType.CONSUMABLE)
        item2 = Item("Potion2", ItemType.CONSUMABLE)
        inventory.weapon_slot = weapon
        inventory.armor_slot = armor
        inventory.backpack_slots[0] = item1
        inventory.backpack_slots[1] = item2

        # Act
        items = inventory.get_all_items()

        # Assert
        assert len(items) == 4
        assert weapon in items
        assert armor in items
        assert item1 in items
        assert item2 in items
