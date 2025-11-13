"""Loot table system for monster drops."""

import random
from typing import List, Tuple, Optional
from item import Item, ItemType


class LootTable:
    """Defines possible loot drops for monsters."""

    def __init__(self, loot_entries: List[Tuple[Item, float]]):
        """
        Initialize a loot table.

        Args:
            loot_entries: List of tuples (Item, drop_chance)
                         where drop_chance is between 0.0 and 1.0
        """
        self.loot_entries = loot_entries

    def roll_loot(self) -> Optional[Item]:
        """
        Roll for loot drops.

        Returns:
            An Item if a drop occurred, None otherwise
        """
        for item, drop_chance in self.loot_entries:
            if random.random() < drop_chance:
                return item
        return None


# Common item pool for loot generation
def create_common_weapon(name: str, attack_bonus: int) -> Item:
    """Create a common weapon item."""
    # Gold value based on attack power (10 gold per attack point)
    gold_value = attack_bonus * 10
    return Item(
        name,
        ItemType.WEAPON,
        f"Deals {attack_bonus} extra damage",
        attack_bonus=attack_bonus,
        gold_value=gold_value,
    )


def create_common_armor(name: str, defense_bonus: int) -> Item:
    """Create a common armor item."""
    # Gold value based on defense (10 gold per defense point)
    gold_value = defense_bonus * 10
    return Item(
        name,
        ItemType.ARMOR,
        f"+{defense_bonus} defense",
        defense_bonus=defense_bonus,
        gold_value=gold_value,
    )


def create_consumable(name: str) -> Item:
    """Create a consumable health potion item."""
    # Standard potion price
    return Item(
        name,
        ItemType.CONSUMABLE,
        "Restores 30 health",
        gold_value=30,
    )


def create_misc_item(name: str, description: str, gold_value: int = 10) -> Item:
    """Create a misc item."""
    return Item(name, ItemType.MISC, description, gold_value=gold_value)


def create_gold_drop(min_amount: int, max_amount: int) -> Item:
    """Create a gold drop item with random amount."""
    amount = random.randint(min_amount, max_amount)
    return Item(
        name=f"{amount} Gold",
        item_type=ItemType.MISC,
        description=f"{amount} pieces of gold",
        gold_value=amount,
    )


def create_town_portal() -> Item:
    """Create a town portal consumable item."""
    return Item(
        "Town Portal",
        ItemType.CONSUMABLE,
        "Opens a portal to town. Use with 'T' key.",
        gold_value=100,  # Valuable utility item
    )


# Monster-specific loot tables
LOOT_TABLES = {
    "banshee": LootTable(
        [
            (
                create_common_armor("Spectral Veil", defense_bonus=8),
                0.3,
            ),
            (create_consumable("Tear of Sorrow"), 0.6),
            (create_gold_drop(1, 5), 0.5),
            (create_town_portal(), 0.15),  # 15% chance for town portal
        ]
    ),
    "leprechaun": LootTable(
        [
            (create_common_weapon("Lucky Shillelagh", attack_bonus=12), 0.4),
            (create_gold_drop(5, 15), 0.9),
            (create_misc_item("Four-Leaf Clover", "Brings good fortune"), 0.3),
            (create_town_portal(), 0.15),
        ]
    ),
    "pooka": LootTable(
        [
            (create_common_weapon("Twisted Horn", attack_bonus=15), 0.35),
            (
                create_common_armor("Shadow Pelt", defense_bonus=10),
                0.3,
            ),
            (create_consumable("Dark Berry"), 0.7),
            (create_gold_drop(2, 6), 0.5),
            (create_town_portal(), 0.15),
        ]
    ),
    "selkie": LootTable(
        [
            (
                create_common_armor("Seal Skin Cloak", defense_bonus=12),
                0.4,
            ),
            (create_consumable("Ocean Pearl"), 0.6),
            (create_gold_drop(2, 7), 0.5),
            (create_town_portal(), 0.15),
        ]
    ),
    "dullahan": LootTable(
        [
            (create_common_weapon("Headless Blade", attack_bonus=25), 0.4),
            (
                create_common_armor("Dark Rider's Mail", defense_bonus=15),
                0.3,
            ),
            (create_gold_drop(5, 12), 0.6),
            (create_town_portal(), 0.15),
        ]
    ),
    "changeling": LootTable(
        [
            (create_common_weapon("Fae Dagger", attack_bonus=18), 0.35),
            (create_consumable("Glamour Essence"), 0.65),
            (create_gold_drop(3, 8), 0.5),
            (create_town_portal(), 0.15),
        ]
    ),
    "clurichaun": LootTable(
        [
            (create_common_weapon("Drunken Bottle", attack_bonus=14), 0.4),
            (create_consumable("Fine Whiskey"), 0.75),
            (create_gold_drop(4, 10), 0.65),
            (create_town_portal(), 0.15),
        ]
    ),
    "merrow": LootTable(
        [
            (
                create_common_armor("Coral Crown", defense_bonus=11),
                0.35,
            ),
            (create_common_weapon("Trident Shard", attack_bonus=20), 0.3),
            (create_consumable("Sea Kelp"), 0.7),
            (create_gold_drop(3, 9), 0.5),
            (create_town_portal(), 0.15),
        ]
    ),
    "fear_gorta": LootTable(
        [
            (create_consumable("Blessed Bread"), 0.7),
            (
                create_common_armor("Tattered Robes", defense_bonus=6),
                0.4,
            ),
            (create_gold_drop(1, 4), 0.4),
            (create_town_portal(), 0.15),
        ]
    ),
    "cat_si": LootTable(
        [
            (create_common_weapon("Cat's Claw", attack_bonus=16), 0.4),
            (create_common_armor("Fur Mantle", defense_bonus=9), 0.35),
            (create_gold_drop(2, 6), 0.5),
            (create_town_portal(), 0.15),
        ]
    ),
}


def get_loot_for_monster(monster_type: str) -> Optional[Item]:
    """
    Get a loot drop for a specific monster type.

    Args:
        monster_type: The type of monster (e.g., 'banshee', 'leprechaun')

    Returns:
        An Item if loot drops, None otherwise
    """
    loot_table = LOOT_TABLES.get(monster_type)
    if loot_table:
        return loot_table.roll_loot()
    return None
