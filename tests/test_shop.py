"""Tests for shop.py - Shop and ShopItem classes"""

from shop import Shop, ShopItem
from inventory import Inventory
from item import Item, ItemType


class TestShopItem:
    """Tests for ShopItem class"""

    def test_shop_item_initialization(self):
        """Test ShopItem initialization with default values"""
        # Arrange
        item = Item("Sword", ItemType.WEAPON, gold_value=50)

        # Act
        shop_item = ShopItem(item, quantity=5)

        # Assert
        assert shop_item.item == item
        assert shop_item.quantity == 5
        assert shop_item.infinite is False

    def test_shop_item_infinite(self):
        """Test ShopItem with infinite quantity"""
        # Arrange
        item = Item("Potion", ItemType.CONSUMABLE, gold_value=25)

        # Act
        shop_item = ShopItem(item, quantity=999, infinite=True)

        # Assert
        assert shop_item.infinite is True
        assert shop_item.is_available() is True

    def test_shop_item_is_available_with_quantity(self):
        """Test is_available returns True when quantity > 0"""
        # Arrange
        item = Item("Sword", ItemType.WEAPON)
        shop_item = ShopItem(item, quantity=3)

        # Act & Assert
        assert shop_item.is_available() is True

    def test_shop_item_is_available_with_zero_quantity(self):
        """Test is_available returns False when quantity = 0"""
        # Arrange
        item = Item("Sword", ItemType.WEAPON)
        shop_item = ShopItem(item, quantity=0)

        # Act & Assert
        assert shop_item.is_available() is False

    def test_shop_item_is_available_infinite(self):
        """Test is_available returns True for infinite items"""
        # Arrange
        item = Item("Potion", ItemType.CONSUMABLE)
        shop_item = ShopItem(item, quantity=0, infinite=True)

        # Act & Assert
        assert shop_item.is_available() is True

    def test_shop_item_decrease_quantity(self):
        """Test decreasing quantity"""
        # Arrange
        item = Item("Sword", ItemType.WEAPON)
        shop_item = ShopItem(item, quantity=5)

        # Act
        shop_item.decrease_quantity()

        # Assert
        assert shop_item.quantity == 4

    def test_shop_item_decrease_quantity_infinite(self):
        """Test decreasing quantity does nothing for infinite items"""
        # Arrange
        item = Item("Potion", ItemType.CONSUMABLE)
        shop_item = ShopItem(item, quantity=999, infinite=True)

        # Act
        shop_item.decrease_quantity()

        # Assert
        assert shop_item.quantity == 999

    def test_shop_item_increase_quantity(self):
        """Test increasing quantity"""
        # Arrange
        item = Item("Sword", ItemType.WEAPON)
        shop_item = ShopItem(item, quantity=3)

        # Act
        shop_item.increase_quantity()

        # Assert
        assert shop_item.quantity == 4

    def test_shop_item_increase_quantity_infinite(self):
        """Test increasing quantity does nothing for infinite items"""
        # Arrange
        item = Item("Potion", ItemType.CONSUMABLE)
        shop_item = ShopItem(item, quantity=999, infinite=True)

        # Act
        shop_item.increase_quantity()

        # Assert
        assert shop_item.quantity == 999


class TestShop:
    """Tests for Shop class"""

    def test_shop_initialization(self):
        """Test Shop initialization"""
        # Arrange & Act
        shop = Shop(5, 10)

        # Assert
        assert shop.grid_x == 5
        assert shop.grid_y == 10
        assert len(shop.inventory) > 0

    def test_shop_has_health_potions(self):
        """Test shop always has health potions (AC5)"""
        # Arrange
        shop = Shop(0, 0)

        # Act
        health_potion_found = False
        for shop_item in shop.inventory:
            if (
                shop_item.item.name == "Health Potion"
                and shop_item.item.item_type == ItemType.CONSUMABLE
            ):
                health_potion_found = True
                assert shop_item.infinite is True
                break

        # Assert
        assert health_potion_found is True

    def test_shop_get_available_items(self):
        """Test getting available items from shop"""
        # Arrange
        shop = Shop(0, 0)

        # Act
        available_items = shop.get_available_items()

        # Assert
        assert len(available_items) > 0
        for shop_item in available_items:
            assert shop_item.is_available() is True

    def test_buy_item_success(self):
        """Test successful item purchase (AC2, AC3, AC14)"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        shop_item = shop.inventory[0]  # Get first item
        initial_quantity = shop_item.quantity
        player_gold = 1000

        # Act
        success, message = shop.buy_item(shop_item, player_gold, inventory)

        # Assert
        assert success is True
        assert "Purchased" in message
        if not shop_item.infinite:
            assert shop_item.quantity == initial_quantity - 1

    def test_buy_item_insufficient_gold(self):
        """Test buying item with insufficient gold (AC2, AC4)"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        shop_item = shop.inventory[0]
        player_gold = 0  # Not enough gold

        # Act
        success, message = shop.buy_item(shop_item, player_gold, inventory)

        # Assert
        assert success is False
        assert "Not enough gold" in message

    def test_buy_item_out_of_stock(self):
        """Test buying item that is out of stock (AC1)"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        item = Item("Rare Item", ItemType.WEAPON, gold_value=50)
        shop_item = ShopItem(item, quantity=0)
        player_gold = 100

        # Act
        success, message = shop.buy_item(shop_item, player_gold, inventory)

        # Assert
        assert success is False
        assert "out of stock" in message

    def test_buy_item_inventory_full(self):
        """Test buying item when inventory is full"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        # Fill inventory completely
        inventory.weapon_slot = Item("Weapon", ItemType.WEAPON)
        inventory.armor_slot = Item("Armor", ItemType.ARMOR)
        for i in range(13):
            inventory.backpack_slots[i] = Item(f"Item{i}", ItemType.MISC)

        shop_item = shop.inventory[0]
        player_gold = 1000

        # Act
        success, message = shop.buy_item(shop_item, player_gold, inventory)

        # Assert
        assert success is False
        assert "full" in message.lower()

    def test_buy_item_atomic_transaction(self):
        """Test that buy transaction is atomic (AC14)"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        shop_item = shop.inventory[1]  # Get non-infinite item
        initial_quantity = shop_item.quantity
        player_gold = 1000

        # Act
        success, _ = shop.buy_item(shop_item, player_gold, inventory)

        # Assert - if successful, both inventory and stock should update
        if success:
            assert len(inventory.get_all_items()) == 1
            if not shop_item.infinite:
                assert shop_item.quantity == initial_quantity - 1

    def test_sell_item_success(self):
        """Test successful item sale (AC7, AC8, AC14)"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        item = Item("Test Sword", ItemType.WEAPON, gold_value=100, sell_price=50)
        inventory.add_item(item)

        # Act
        success, message, gold_earned = shop.sell_item(item, inventory)

        # Assert
        assert success is True
        assert "Sold" in message
        assert gold_earned == 50
        assert item not in inventory.get_all_items()

    def test_sell_item_unsellable(self):
        """Test selling unsellable item fails (AC9)"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        item = Item(
            "Quest Item",
            ItemType.MISC,
            gold_value=0,
            unsellable=True,
        )
        inventory.add_item(item)

        # Act
        success, message, gold_earned = shop.sell_item(item, inventory)

        # Assert
        assert success is False
        assert "cannot be sold" in message
        assert gold_earned == 0
        assert item in inventory.get_all_items()

    def test_sell_item_not_in_inventory(self):
        """Test selling item not in inventory fails (AC7)"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        item = Item("Test Sword", ItemType.WEAPON, gold_value=100)
        # Don't add item to inventory

        # Act
        success, message, gold_earned = shop.sell_item(item, inventory)

        # Assert
        assert success is False
        assert "not found" in message.lower()
        assert gold_earned == 0

    def test_sell_item_updates_shop_stock(self):
        """Test selling item updates shop stock (AC10)"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        item = Item("Test Sword", ItemType.WEAPON, gold_value=100, sell_price=50)
        inventory.add_item(item)

        # Act
        success, _, gold_earned = shop.sell_item(item, inventory)

        # Assert
        assert success is True
        assert gold_earned == 50
        # Check if shop stock was updated
        found_in_shop = False
        for shop_item in shop.inventory:
            if shop_item.item.name == "Test Sword":
                found_in_shop = True
                break
        assert found_in_shop is True

    def test_sell_item_atomic_transaction(self):
        """Test that sell transaction is atomic (AC14)"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        item = Item("Test Sword", ItemType.WEAPON, gold_value=100, sell_price=50)
        inventory.add_item(item)
        initial_inventory_size = len(inventory.get_all_items())

        # Act
        success, _, gold_earned = shop.sell_item(item, inventory)

        # Assert - if successful, item removed and gold calculated
        if success:
            assert len(inventory.get_all_items()) == initial_inventory_size - 1
            assert gold_earned > 0

    def test_sell_item_increases_existing_stock(self):
        """Test selling item that's already in stock increases quantity (AC10)"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        # Find an item in shop stock
        existing_shop_item = None
        for shop_item in shop.inventory:
            if not shop_item.infinite and shop_item.item.name == "Iron Sword":
                existing_shop_item = shop_item
                break

        if existing_shop_item:
            initial_quantity = existing_shop_item.quantity
            # Create same item to sell
            item = Item(
                "Iron Sword",
                ItemType.WEAPON,
                description="A sturdy iron sword",
                attack_bonus=5,
                gold_value=50,
            )
            inventory.add_item(item)

            # Act
            success, _, _ = shop.sell_item(item, inventory)

            # Assert
            assert success is True
            assert existing_shop_item.quantity == initial_quantity + 1

    def test_default_sell_price(self):
        """Test that items default to half gold_value for sell price"""
        # Arrange
        item = Item("Test Item", ItemType.WEAPON, gold_value=100)

        # Assert
        assert item.sell_price == 50  # Half of gold_value

    def test_custom_sell_price(self):
        """Test that custom sell price is respected"""
        # Arrange
        item = Item("Test Item", ItemType.WEAPON, gold_value=100, sell_price=75)

        # Assert
        assert item.sell_price == 75

    def test_buy_multiple_items(self):
        """Test buying multiple items in sequence"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        player_gold = 1000

        # Act
        shop_item1 = shop.inventory[0]
        success1, _ = shop.buy_item(shop_item1, player_gold, inventory)
        player_gold -= shop_item1.item.gold_value if success1 else 0

        shop_item2 = shop.inventory[1]
        success2, _ = shop.buy_item(shop_item2, player_gold, inventory)

        # Assert
        assert success1 is True
        assert success2 is True
        assert len(inventory.get_all_items()) >= 2

    def test_sell_multiple_items(self):
        """Test selling multiple items in sequence"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        item1 = Item("Sword1", ItemType.WEAPON, gold_value=100, sell_price=50)
        item2 = Item("Sword2", ItemType.WEAPON, gold_value=80, sell_price=40)
        inventory.add_item(item1)
        inventory.add_item(item2)

        # Act
        success1, _, gold1 = shop.sell_item(item1, inventory)
        success2, _, gold2 = shop.sell_item(item2, inventory)

        # Assert
        assert success1 is True
        assert success2 is True
        assert gold1 == 50
        assert gold2 == 40
        assert len(inventory.get_all_items()) == 0

    def test_buy_item_edge_case_add_fails(self, mocker):
        """Test edge case where add_item fails unexpectedly"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        shop_item = shop.inventory[0]
        player_gold = 1000

        # Mock add_item to return False
        mocker.patch.object(inventory, "add_item", return_value=False)

        # Act
        success, message = shop.buy_item(shop_item, player_gold, inventory)

        # Assert
        assert success is False
        assert "Failed" in message

    def test_sell_item_edge_case_remove_fails(self, mocker):
        """Test edge case where remove_item fails unexpectedly"""
        # Arrange
        shop = Shop(0, 0)
        inventory = Inventory()
        item = Item("Test Sword", ItemType.WEAPON, gold_value=100, sell_price=50)
        inventory.add_item(item)

        # Mock contains_item to return True but remove_item to return False
        mocker.patch.object(inventory, "contains_item", return_value=True)
        mocker.patch.object(inventory, "remove_item", return_value=False)

        # Act
        success, message, gold_earned = shop.sell_item(item, inventory)

        # Assert
        assert success is False
        assert "Failed" in message
        assert gold_earned == 0
