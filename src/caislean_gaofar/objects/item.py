from enum import Enum


class ItemType(Enum):
    """Types of items that can be stored in inventory"""

    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    MISC = "misc"


class Item:
    """Represents an item that can be stored in inventory"""

    def __init__(
        self,
        name: str,
        item_type: ItemType,
        description: str = "",
        attack_bonus: int = 0,
        defense_bonus: int = 0,
        health_restore: int = 0,
        gold_value: int = 0,
        sell_price: int | None = None,
        unsellable: bool = False,
    ):
        self.name = name
        self.item_type = item_type
        self.description = description
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.health_restore = health_restore  # Health points restored when consumed
        self.gold_value = gold_value  # Gold/currency value of the item (buy price)
        # Sell price defaults to half of buy price if not specified
        self.sell_price = sell_price if sell_price is not None else gold_value // 2
        self.unsellable = unsellable  # True for quest items or unsellable items

    def __repr__(self) -> str:
        return f"Item({self.name}, {self.item_type.value})"
