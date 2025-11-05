from typing import Optional
from item import Item, ItemType


class Inventory:
    """Manages inventory slots: weapon, armor, and 5 backpack slots"""

    def __init__(self):
        self.weapon_slot: Optional[Item] = None
        self.armor_slot: Optional[Item] = None
        self.backpack_slots: list[Optional[Item]] = [None, None, None, None, None]

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
        slot_index is used for backpack slots (0-4)
        """
        if slot_type == "weapon":
            item = self.weapon_slot
            self.weapon_slot = None
            return item
        elif slot_type == "armor":
            item = self.armor_slot
            self.armor_slot = None
            return item
        elif slot_type == "backpack" and 0 <= slot_index < 5:
            item = self.backpack_slots[slot_index]
            self.backpack_slots[slot_index] = None
            return item
        return None

    def equip_from_backpack(self, backpack_index: int) -> bool:
        """
        Equip an item from backpack to appropriate slot.
        Returns True if successful.
        """
        if not (0 <= backpack_index < 5):
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

    def get_total_health_bonus(self) -> int:
        """Calculate total health bonus from all equipped items"""
        bonus = 0
        if self.weapon_slot:
            bonus += self.weapon_slot.health_bonus
        if self.armor_slot:
            bonus += self.armor_slot.health_bonus
        return bonus
