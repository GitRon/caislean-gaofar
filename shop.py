"""Shop system for buying and selling items."""

from typing import Tuple
from item import Item, ItemType
from inventory import Inventory


class ShopItem:
    """Represents an item in the shop with quantity."""

    def __init__(self, item: Item, quantity: int = 1, infinite: bool = False):
        """
        Initialize a shop item.

        Args:
            item: The item being sold
            quantity: Number of items in stock (ignored if infinite is True)
            infinite: If True, item is always available for purchase
        """
        self.item = item
        self.quantity = quantity
        self.infinite = infinite

    def is_available(self) -> bool:
        """Check if item is available for purchase."""
        return self.infinite or self.quantity > 0

    def decrease_quantity(self):
        """Decrease quantity by 1 (no effect if infinite)."""
        if not self.infinite:
            self.quantity = max(0, self.quantity - 1)

    def increase_quantity(self):
        """Increase quantity by 1 (no effect if infinite)."""
        if not self.infinite:
            self.quantity += 1


class Shop:
    """Shop system for buying and selling items."""

    def __init__(self, grid_x: int, grid_y: int):
        """
        Initialize the shop.

        Args:
            grid_x: Grid x position of the shop
            grid_y: Grid y position of the shop
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.inventory: list[ShopItem] = []
        self._initialize_shop_inventory()

    def _initialize_shop_inventory(self):
        """Initialize the shop with default items."""
        # Health potions - always available (AC5)
        health_potion = Item(
            name="Health Potion",
            item_type=ItemType.CONSUMABLE,
            description="Restores 30 HP",
            gold_value=25,
        )
        self.inventory.append(ShopItem(health_potion, quantity=999, infinite=True))

        # Weapons
        iron_sword = Item(
            name="Iron Sword",
            item_type=ItemType.WEAPON,
            description="A sturdy iron sword",
            attack_bonus=5,
            gold_value=50,
        )
        self.inventory.append(ShopItem(iron_sword, quantity=3))

        steel_sword = Item(
            name="Steel Sword",
            item_type=ItemType.WEAPON,
            description="A well-crafted steel sword",
            attack_bonus=8,
            gold_value=100,
        )
        self.inventory.append(ShopItem(steel_sword, quantity=2))

        # Armor
        leather_armor = Item(
            name="Leather Armor",
            item_type=ItemType.ARMOR,
            description="Basic leather protection",
            defense_bonus=3,
            gold_value=40,
        )
        self.inventory.append(ShopItem(leather_armor, quantity=3))

        chainmail = Item(
            name="Chainmail",
            item_type=ItemType.ARMOR,
            description="Strong chainmail armor",
            defense_bonus=5,
            gold_value=80,
        )
        self.inventory.append(ShopItem(chainmail, quantity=2))

    def buy_item(
        self, shop_item: ShopItem, player_gold: int, player_inventory: Inventory
    ) -> Tuple[bool, str]:
        """
        Attempt to buy an item from the shop (atomic transaction).

        Args:
            shop_item: The shop item to purchase
            player_gold: Player's current gold amount
            player_inventory: Player's inventory

        Returns:
            Tuple of (success, message)
        """
        # AC2: Check if player has sufficient gold
        if player_gold < shop_item.item.gold_value:
            return False, "Not enough gold!"

        # AC1: Check if item is available
        if not shop_item.is_available():
            return False, "Item out of stock!"

        # Check if player inventory has space
        if not player_inventory.has_space():
            return False, "Inventory is full!"

        # AC14: Atomic transaction - all updates happen together
        # Try to add to inventory first (this is the critical check)
        if player_inventory.add_item(shop_item.item):
            # AC3: Successfully purchased - update gold and stock
            shop_item.decrease_quantity()
            return (
                True,
                f"Purchased {shop_item.item.name} for {shop_item.item.gold_value} gold!",
            )
        else:
            return False, "Failed to add item to inventory!"

    def sell_item(
        self, item: Item, player_inventory: Inventory
    ) -> Tuple[bool, str, int]:
        """
        Attempt to sell an item to the shop (atomic transaction).

        Args:
            item: The item to sell
            player_inventory: Player's inventory

        Returns:
            Tuple of (success, message, gold_earned)
        """
        # AC9: Check if item is sellable
        if item.unsellable:
            return False, "This item cannot be sold!", 0

        # AC7: Check if item is in player's inventory
        if not player_inventory.contains_item(item):
            return False, "Item not found in inventory!", 0

        # AC14: Atomic transaction - remove item from inventory
        if player_inventory.remove_item(item):
            # AC8: Calculate sell price and update shop stock
            gold_earned = item.sell_price

            # AC10: Update shop stock when item is sold to it
            # Check if we already have this item type in stock
            for shop_item in self.inventory:
                if shop_item.item.name == item.name:
                    shop_item.increase_quantity()
                    return (
                        True,
                        f"Sold {item.name} for {gold_earned} gold!",
                        gold_earned,
                    )

            # If not in stock, add it as a new shop item
            new_shop_item = ShopItem(item, quantity=1)
            self.inventory.append(new_shop_item)
            return True, f"Sold {item.name} for {gold_earned} gold!", gold_earned
        else:
            return False, "Failed to remove item from inventory!", 0

    def get_available_items(self) -> list[ShopItem]:
        """Get all available items in the shop."""
        return [item for item in self.inventory if item.is_available()]
