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
    return Item(
        name,
        ItemType.WEAPON,
        f"Deals {attack_bonus} extra damage",
        attack_bonus=attack_bonus,
    )


def create_common_armor(name: str, defense_bonus: int, health_bonus: int = 0) -> Item:
    """Create a common armor item."""
    return Item(
        name,
        ItemType.ARMOR,
        f"+{defense_bonus} defense",
        defense_bonus=defense_bonus,
        health_bonus=health_bonus,
    )


def create_consumable(name: str, health_bonus: int) -> Item:
    """Create a consumable item."""
    return Item(
        name,
        ItemType.CONSUMABLE,
        f"Restores {health_bonus} health",
        health_bonus=health_bonus,
    )


def create_misc_item(name: str, description: str) -> Item:
    """Create a misc item."""
    return Item(name, ItemType.MISC, description)


# Monster-specific loot tables
LOOT_TABLES = {
    "banshee": LootTable(
        [
            (
                create_common_armor("Spectral Veil", defense_bonus=8, health_bonus=15),
                0.3,
            ),
            (create_consumable("Tear of Sorrow", health_bonus=25), 0.4),
            (create_misc_item("Ethereal Echo", "A haunting whisper from beyond"), 0.5),
        ]
    ),
    "leprechaun": LootTable(
        [
            (create_common_weapon("Lucky Shillelagh", attack_bonus=12), 0.4),
            (create_misc_item("Gold Coin", "A shiny golden coin"), 0.8),
            (create_misc_item("Four-Leaf Clover", "Brings good fortune"), 0.3),
        ]
    ),
    "pooka": LootTable(
        [
            (create_common_weapon("Twisted Horn", attack_bonus=15), 0.35),
            (
                create_common_armor("Shadow Pelt", defense_bonus=10, health_bonus=20),
                0.3,
            ),
            (create_consumable("Dark Berry", health_bonus=30), 0.5),
        ]
    ),
    "selkie": LootTable(
        [
            (
                create_common_armor(
                    "Seal Skin Cloak", defense_bonus=12, health_bonus=25
                ),
                0.4,
            ),
            (create_consumable("Ocean Pearl", health_bonus=40), 0.3),
            (create_misc_item("Sea Shell", "Echoes with ocean sounds"), 0.6),
        ]
    ),
    "dullahan": LootTable(
        [
            (create_common_weapon("Headless Blade", attack_bonus=25), 0.4),
            (
                create_common_armor(
                    "Dark Rider's Mail", defense_bonus=15, health_bonus=30
                ),
                0.3,
            ),
            (create_misc_item("Spine Whip", "A fearsome trophy"), 0.35),
        ]
    ),
    "changeling": LootTable(
        [
            (create_common_weapon("Fae Dagger", attack_bonus=18), 0.35),
            (create_consumable("Glamour Essence", health_bonus=35), 0.4),
            (create_misc_item("Fairy Dust", "Shimmers with magic"), 0.5),
        ]
    ),
    "clurichaun": LootTable(
        [
            (create_common_weapon("Drunken Bottle", attack_bonus=14), 0.4),
            (create_consumable("Fine Whiskey", health_bonus=45), 0.6),
            (create_misc_item("Silver Flask", "Never seems to empty"), 0.3),
        ]
    ),
    "merrow": LootTable(
        [
            (
                create_common_armor("Coral Crown", defense_bonus=11, health_bonus=22),
                0.35,
            ),
            (create_common_weapon("Trident Shard", attack_bonus=20), 0.3),
            (create_consumable("Sea Kelp", health_bonus=28), 0.5),
        ]
    ),
    "fear_gorta": LootTable(
        [
            (create_consumable("Blessed Bread", health_bonus=50), 0.5),
            (
                create_common_armor("Tattered Robes", defense_bonus=6, health_bonus=10),
                0.4,
            ),
            (create_misc_item("Famine Token", "A grim reminder"), 0.3),
        ]
    ),
    "cat_si": LootTable(
        [
            (create_common_weapon("Cat's Claw", attack_bonus=16), 0.4),
            (create_common_armor("Fur Mantle", defense_bonus=9, health_bonus=18), 0.35),
            (create_misc_item("White Star Mark", "Symbol of the Cat Sidhe"), 0.4),
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
