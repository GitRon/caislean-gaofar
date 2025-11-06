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
        health_bonus: int = 0,
        gold_value: int = 0,
    ):
        self.name = name
        self.item_type = item_type
        self.description = description
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.health_bonus = health_bonus
        self.gold_value = gold_value  # Gold/currency value of the item

    def __repr__(self):
        return f"Item({self.name}, {self.item_type.value})"
