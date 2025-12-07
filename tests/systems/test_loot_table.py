"""Tests for loot_table.py - Loot table system for monster drops"""

from unittest.mock import patch
from caislean_gaofar.systems.loot_table import (
    LootTable,
    create_common_weapon,
    create_common_armor,
    create_consumable,
    create_misc_item,
    create_town_portal,
    get_loot_for_monster,
    LOOT_TABLES,
)
from caislean_gaofar.objects.item import Item, ItemType


class TestLootTable:
    """Tests for LootTable class"""

    def test_loottable_initialization(self):
        """Test LootTable initialization"""
        # Arrange
        item1 = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        item2 = Item("Shield", ItemType.ARMOR, defense_bonus=5)
        loot_entries = [(item1, 0.5), (item2, 0.3)]

        # Act
        loot_table = LootTable(loot_entries)

        # Assert
        assert loot_table.loot_entries == loot_entries
        assert len(loot_table.loot_entries) == 2

    @patch("caislean_gaofar.systems.loot_table.random.random")
    def test_loottable_roll_loot_first_item_drops(self, mock_random):
        """Test LootTable roll_loot when first item drops"""
        # Arrange
        item1 = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        item2 = Item("Shield", ItemType.ARMOR, defense_bonus=5)
        loot_table = LootTable([(item1, 0.5), (item2, 0.3)])
        mock_random.return_value = 0.3  # Less than 0.5, should drop first item

        # Act
        result = loot_table.roll_loot()

        # Assert
        assert result == item1

    @patch("caislean_gaofar.systems.loot_table.random.random")
    def test_loottable_roll_loot_second_item_drops(self, mock_random):
        """Test LootTable roll_loot when second item drops"""
        # Arrange
        item1 = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        item2 = Item("Shield", ItemType.ARMOR, defense_bonus=5)
        loot_table = LootTable([(item1, 0.5), (item2, 0.3)])
        # First call returns 0.6 (skip first), second call returns 0.2 (take second)
        mock_random.side_effect = [0.6, 0.2]

        # Act
        result = loot_table.roll_loot()

        # Assert
        assert result == item2

    @patch("caislean_gaofar.systems.loot_table.random.random")
    def test_loottable_roll_loot_no_items_drop(self, mock_random):
        """Test LootTable roll_loot when no items drop"""
        # Arrange
        item1 = Item("Sword", ItemType.WEAPON, attack_bonus=10)
        item2 = Item("Shield", ItemType.ARMOR, defense_bonus=5)
        loot_table = LootTable([(item1, 0.5), (item2, 0.3)])
        mock_random.return_value = 0.9  # Higher than both drop chances

        # Act
        result = loot_table.roll_loot()

        # Assert
        assert result is None


class TestCreateFunctions:
    """Tests for item creation helper functions"""

    def test_create_common_weapon(self):
        """Test create_common_weapon creates weapon with correct properties"""
        # Arrange & Act
        weapon = create_common_weapon("Iron Sword", 15)

        # Assert
        assert weapon.name == "Iron Sword"
        assert weapon.item_type == ItemType.WEAPON
        assert weapon.description == "Deals 15 extra damage"
        assert weapon.attack_bonus == 15
        assert weapon.defense_bonus == 0

    def test_create_common_armor(self):
        """Test create_common_armor"""
        # Arrange & Act
        armor = create_common_armor("Iron Plate", 10)

        # Assert
        assert armor.name == "Iron Plate"
        assert armor.item_type == ItemType.ARMOR
        assert armor.description == "+10 defense"
        assert armor.defense_bonus == 10
        assert armor.attack_bonus == 0

    def test_create_consumable(self):
        """Test create_consumable creates consumable with correct properties"""
        # Arrange & Act
        potion = create_consumable("Health Potion")

        # Assert
        assert potion.name == "Health Potion"
        assert potion.item_type == ItemType.CONSUMABLE
        assert potion.description == "Restores 30 health"
        assert potion.health_restore == 30
        assert potion.attack_bonus == 0
        assert potion.defense_bonus == 0

    def test_create_consumable_custom_health_restore(self):
        """Test create_consumable with custom health_restore value"""
        # Arrange & Act
        potion = create_consumable("Greater Health Potion", health_restore=50)

        # Assert
        assert potion.name == "Greater Health Potion"
        assert potion.item_type == ItemType.CONSUMABLE
        assert potion.description == "Restores 50 health"
        assert potion.health_restore == 50
        assert potion.attack_bonus == 0
        assert potion.defense_bonus == 0

    def test_create_misc_item(self):
        """Test create_misc_item creates misc item with correct properties"""
        # Arrange & Act
        misc = create_misc_item("Golden Key", "Opens special doors")

        # Assert
        assert misc.name == "Golden Key"
        assert misc.item_type == ItemType.MISC
        assert misc.description == "Opens special doors"
        assert misc.attack_bonus == 0
        assert misc.defense_bonus == 0

    def test_create_town_portal(self):
        """Test create_town_portal creates town portal with correct properties"""
        # Arrange & Act
        portal = create_town_portal()

        # Assert
        assert portal.name == "Town Portal"
        assert portal.item_type == ItemType.CONSUMABLE
        assert "portal" in portal.description.lower()
        assert "town" in portal.description.lower()
        assert portal.attack_bonus == 0
        assert portal.defense_bonus == 0


class TestGetLootForMonster:
    """Tests for get_loot_for_monster function"""

    @patch("caislean_gaofar.systems.loot_table.random.random")
    def test_get_loot_for_monster_valid_type_drops_loot(self, mock_random):
        """Test get_loot_for_monster with valid monster type that drops loot"""
        # Arrange
        mock_random.return_value = 0.1  # Low value to ensure a drop

        # Act
        result = get_loot_for_monster("banshee")

        # Assert
        assert result is not None
        assert isinstance(result, Item)

    @patch("caislean_gaofar.systems.loot_table.random.random")
    def test_get_loot_for_monster_valid_type_no_drop(self, mock_random):
        """Test get_loot_for_monster with valid monster type that doesn't drop"""
        # Arrange
        mock_random.return_value = 0.99  # High value to prevent drops

        # Act
        result = get_loot_for_monster("banshee")

        # Assert
        assert result is None

    def test_get_loot_for_monster_invalid_type(self):
        """Test get_loot_for_monster with invalid monster type"""
        # Arrange & Act
        result = get_loot_for_monster("invalid_monster")

        # Assert
        assert result is None

    def test_loot_table_banshee_exists(self):
        """Test LOOT_TABLES contains banshee entry"""
        assert "banshee" in LOOT_TABLES
        assert isinstance(LOOT_TABLES["banshee"], LootTable)

    def test_loot_table_leprechaun_exists(self):
        """Test LOOT_TABLES contains leprechaun entry"""
        assert "leprechaun" in LOOT_TABLES
        assert isinstance(LOOT_TABLES["leprechaun"], LootTable)

    def test_loot_table_pooka_exists(self):
        """Test LOOT_TABLES contains pooka entry"""
        assert "pooka" in LOOT_TABLES
        assert isinstance(LOOT_TABLES["pooka"], LootTable)

    def test_loot_table_selkie_exists(self):
        """Test LOOT_TABLES contains selkie entry"""
        assert "selkie" in LOOT_TABLES
        assert isinstance(LOOT_TABLES["selkie"], LootTable)

    def test_loot_table_dullahan_exists(self):
        """Test LOOT_TABLES contains dullahan entry"""
        assert "dullahan" in LOOT_TABLES
        assert isinstance(LOOT_TABLES["dullahan"], LootTable)

    def test_loot_table_changeling_exists(self):
        """Test LOOT_TABLES contains changeling entry"""
        assert "changeling" in LOOT_TABLES
        assert isinstance(LOOT_TABLES["changeling"], LootTable)

    def test_loot_table_clurichaun_exists(self):
        """Test LOOT_TABLES contains clurichaun entry"""
        assert "clurichaun" in LOOT_TABLES
        assert isinstance(LOOT_TABLES["clurichaun"], LootTable)

    def test_loot_table_merrow_exists(self):
        """Test LOOT_TABLES contains merrow entry"""
        assert "merrow" in LOOT_TABLES
        assert isinstance(LOOT_TABLES["merrow"], LootTable)

    def test_loot_table_fear_gorta_exists(self):
        """Test LOOT_TABLES contains fear_gorta entry"""
        assert "fear_gorta" in LOOT_TABLES
        assert isinstance(LOOT_TABLES["fear_gorta"], LootTable)

    def test_loot_table_cat_si_exists(self):
        """Test LOOT_TABLES contains cat_si entry"""
        assert "cat_si" in LOOT_TABLES
        assert isinstance(LOOT_TABLES["cat_si"], LootTable)

    def test_loot_table_banshee_has_valid_entries(self):
        """Test banshee loot table has valid entries"""
        loot_table = LOOT_TABLES["banshee"]
        assert len(loot_table.loot_entries) > 0
        first_item, first_chance = loot_table.loot_entries[0]
        assert isinstance(first_item, Item)
        assert isinstance(first_chance, float)
        assert 0.0 <= first_chance <= 1.0
