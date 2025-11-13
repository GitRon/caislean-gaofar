"""Tests for item.py - Item class and ItemType enum"""

from caislean_gaofar.objects.item import Item, ItemType


class TestItemType:
    """Tests for ItemType enum"""

    def test_itemtype_weapon_value(self):
        """Test WEAPON enum value"""
        # Arrange & Act & Assert
        assert ItemType.WEAPON.value == "weapon"

    def test_itemtype_armor_value(self):
        """Test ARMOR enum value"""
        # Arrange & Act & Assert
        assert ItemType.ARMOR.value == "armor"

    def test_itemtype_consumable_value(self):
        """Test CONSUMABLE enum value"""
        # Arrange & Act & Assert
        assert ItemType.CONSUMABLE.value == "consumable"

    def test_itemtype_misc_value(self):
        """Test MISC enum value"""
        # Arrange & Act & Assert
        assert ItemType.MISC.value == "misc"


class TestItem:
    """Tests for Item class"""

    def test_item_initialization_minimal(self):
        """Test Item initialization with minimal parameters"""
        # Arrange & Act
        item = Item("Sword", ItemType.WEAPON)

        # Assert
        assert item.name == "Sword"
        assert item.item_type == ItemType.WEAPON
        assert item.description == ""
        assert item.attack_bonus == 0
        assert item.defense_bonus == 0

    def test_item_initialization_with_description(self):
        """Test Item initialization with description"""
        # Arrange & Act
        item = Item("Shield", ItemType.ARMOR, description="A sturdy shield")

        # Assert
        assert item.name == "Shield"
        assert item.item_type == ItemType.ARMOR
        assert item.description == "A sturdy shield"
        assert item.attack_bonus == 0
        assert item.defense_bonus == 0

    def test_item_initialization_with_attack_bonus(self):
        """Test Item initialization with attack bonus"""
        # Arrange & Act
        item = Item("Sword", ItemType.WEAPON, attack_bonus=10)

        # Assert
        assert item.name == "Sword"
        assert item.attack_bonus == 10
        assert item.defense_bonus == 0

    def test_item_initialization_with_defense_bonus(self):
        """Test Item initialization with defense bonus"""
        # Arrange & Act
        item = Item("Shield", ItemType.ARMOR, defense_bonus=5)

        # Assert
        assert item.name == "Shield"
        assert item.defense_bonus == 5
        assert item.attack_bonus == 0

    def test_item_initialization_with_all_bonuses(self):
        """Test Item initialization with all bonuses"""
        # Arrange & Act
        item = Item(
            "Magic Sword",
            ItemType.WEAPON,
            description="A powerful weapon",
            attack_bonus=15,
            defense_bonus=3,
        )

        # Assert
        assert item.name == "Magic Sword"
        assert item.item_type == ItemType.WEAPON
        assert item.description == "A powerful weapon"
        assert item.attack_bonus == 15
        assert item.defense_bonus == 3

    def test_item_initialization_with_gold_value(self):
        """Test Item initialization with gold value"""
        # Arrange & Act
        item = Item("Gold Coins", ItemType.MISC, gold_value=100)

        # Assert
        assert item.name == "Gold Coins"
        assert item.gold_value == 100
        assert item.attack_bonus == 0
        assert item.defense_bonus == 0

    def test_item_repr_weapon(self):
        """Test Item __repr__ for weapon"""
        # Arrange
        item = Item("Sword", ItemType.WEAPON)

        # Act
        result = repr(item)

        # Assert
        assert result == "Item(Sword, weapon)"

    def test_item_repr_armor(self):
        """Test Item __repr__ for armor"""
        # Arrange
        item = Item("Shield", ItemType.ARMOR)

        # Act
        result = repr(item)

        # Assert
        assert result == "Item(Shield, armor)"

    def test_item_repr_consumable(self):
        """Test Item __repr__ for consumable"""
        # Arrange
        item = Item("Potion", ItemType.CONSUMABLE)

        # Act
        result = repr(item)

        # Assert
        assert result == "Item(Potion, consumable)"

    def test_item_repr_misc(self):
        """Test Item __repr__ for misc"""
        # Arrange
        item = Item("Key", ItemType.MISC)

        # Act
        result = repr(item)

        # Assert
        assert result == "Item(Key, misc)"
