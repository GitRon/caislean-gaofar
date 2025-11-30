from typing import Optional
from caislean_gaofar.objects.item import Item, ItemType


class Inventory:
    """Manages inventory slots: weapon, armor, and 10 backpack slots"""

    def __init__(self):
        self.weapon_slot: Optional[Item] = None
        self.armor_slot: Optional[Item] = None
        self.backpack_slots: list[Optional[Item]] = [None] * 10

    def add_item(self, item: Item) -> bool:
        """
        Add an item to the inventory.
        Returns True if successful, False if no space available.
        """
        # Try to add to appropriate equipment slot first if empty
        if item.item_type == ItemType.WEAPON and self.weapon_slot is None:
            self.weapon_slot = item
            return True
        elif item.item_type == ItemType.ARMOR and self.armor_slot is None:
            self.armor_slot = item
            return True

        # Otherwise, try to add to backpack
        for i in range(len(self.backpack_slots)):
            if self.backpack_slots[i] is None:
                self.backpack_slots[i] = item
                return True

        return False  # No space available

    def remove_item_from_slot(
        self, slot_type: str, slot_index: int = 0
    ) -> Optional[Item]:
        """
        Remove and return an item from a specific slot.
        slot_type can be: 'weapon', 'armor', or 'backpack'
        slot_index is used for backpack slots (0-9)
        """
        if slot_type == "weapon":
            item = self.weapon_slot
            self.weapon_slot = None
            return item
        elif slot_type == "armor":
            item = self.armor_slot
            self.armor_slot = None
            return item
        elif slot_type == "backpack" and 0 <= slot_index < 10:
            item = self.backpack_slots[slot_index]
            self.backpack_slots[slot_index] = None
            return item
        return None

    def equip_from_backpack(self, backpack_index: int) -> bool:
        """
        Equip an item from backpack to appropriate slot.
        Returns True if successful.
        """
        if not (0 <= backpack_index < 10):
            return False

        item = self.backpack_slots[backpack_index]
        if item is None:
            return False

        # Try to equip based on item type
        if item.item_type == ItemType.WEAPON:
            # Swap with current weapon if exists
            old_weapon = self.weapon_slot
            self.weapon_slot = item
            self.backpack_slots[backpack_index] = old_weapon
            return True
        elif item.item_type == ItemType.ARMOR:
            # Swap with current armor if exists
            old_armor = self.armor_slot
            self.armor_slot = item
            self.backpack_slots[backpack_index] = old_armor
            return True

        return False

    def get_total_attack_bonus(self) -> int:
        """Calculate total attack bonus from all equipped items"""
        bonus = 0
        if self.weapon_slot:
            bonus += self.weapon_slot.attack_bonus
        if self.armor_slot:
            bonus += self.armor_slot.attack_bonus
        return bonus

    def get_total_defense_bonus(self) -> int:
        """Calculate total defense bonus from all equipped items"""
        bonus = 0
        if self.weapon_slot:
            bonus += self.weapon_slot.defense_bonus
        if self.armor_slot:
            bonus += self.armor_slot.defense_bonus
        return bonus

    def has_space(self) -> bool:
        """Check if inventory has space for at least one more item."""
        # Check if any backpack slot is empty
        for slot in self.backpack_slots:
            if slot is None:
                return True
        return False

    def contains_item(self, item: Item) -> bool:
        """
        Check if inventory contains a specific item instance.

        Args:
            item: The item to check for

        Returns:
            True if item is in inventory, False otherwise
        """
        # Check weapon slot
        if self.weapon_slot is item:
            return True
        # Check armor slot
        if self.armor_slot is item:
            return True
        # Check backpack slots
        if item in self.backpack_slots:
            return True
        return False

    def remove_item(self, item: Item) -> bool:
        """
        Remove a specific item instance from inventory.

        Args:
            item: The item to remove

        Returns:
            True if item was removed, False if not found
        """
        # Check weapon slot
        if self.weapon_slot is item:
            self.weapon_slot = None
            return True
        # Check armor slot
        if self.armor_slot is item:
            self.armor_slot = None
            return True
        # Check backpack slots
        for i in range(len(self.backpack_slots)):
            if self.backpack_slots[i] is item:
                self.backpack_slots[i] = None
                return True
        return False

    def get_all_items(self) -> list[Item]:
        """
        Get all items in inventory (weapon, armor, and backpack).

        Returns:
            List of all items in inventory
        """
        items = []
        if self.weapon_slot:
            items.append(self.weapon_slot)
        if self.armor_slot:
            items.append(self.armor_slot)
        for item in self.backpack_slots:
            if item:
                items.append(item)
        return items
