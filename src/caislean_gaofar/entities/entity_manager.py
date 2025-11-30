"""Entity management system for handling game entities."""

import random
from typing import List, Optional, Dict
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.entities.monsters import ALL_MONSTER_CLASSES
from caislean_gaofar.objects.chest import Chest
from caislean_gaofar.objects.ground_item import GroundItem
from caislean_gaofar.objects.item import Item
from caislean_gaofar.systems.loot_table import get_loot_for_monster


class EntityManager:
    """Manages entity lifecycle and data."""

    def __init__(self):
        """Initialize the entity manager."""
        self.monsters: List = []
        self.chests: List[Chest] = []
        self.ground_items: List[GroundItem] = []

        # Tracking for persistence
        self.killed_monsters: List[Dict] = []
        self.opened_chests: List[Dict] = []

    def spawn_monsters(self, world_map, dungeon_manager):
        """
        Spawn monsters from current map data, excluding killed monsters.

        Args:
            world_map: The current world map
            dungeon_manager: The dungeon manager instance
        """
        self.monsters = []
        current_map_id = dungeon_manager.current_map_id
        monster_spawns = world_map.get_entity_spawns("monsters")

        # DEBUG: Log spawn information
        print(f"[DEBUG] spawn_monsters called for map '{current_map_id}'")
        print(f"[DEBUG]   Found {len(monster_spawns)} monster spawns")
        print(f"[DEBUG]   Killed monsters list has {len(self.killed_monsters)} entries")

        for spawn in monster_spawns:
            monster_type = spawn.get("type", "banshee")
            monster_x = spawn["x"]
            monster_y = spawn["y"]

            # Check if this monster was already killed
            is_killed = any(
                km["type"] == monster_type
                and km["x"] == monster_x
                and km["y"] == monster_y
                and km["map_id"] == current_map_id
                for km in self.killed_monsters
            )

            if is_killed:
                print(
                    f"[DEBUG]   Skipping {monster_type} at ({monster_x}, {monster_y}) - already killed"
                )
                continue  # Skip this monster, it's dead
            else:
                print(
                    f"[DEBUG]   Spawning {monster_type} at ({monster_x}, {monster_y})"
                )

            # Find matching monster class
            monster_class = None
            for cls in ALL_MONSTER_CLASSES:
                if cls.MONSTER_TYPE == monster_type:
                    monster_class = cls
                    break
            if monster_class is None:
                monster_class = random.choice(ALL_MONSTER_CLASSES)
            monster = monster_class(monster_x, monster_y)
            self.monsters.append(monster)

        # If no monsters in map, spawn one randomly (only if not killed before)
        if not self.monsters and not monster_spawns:
            spawn_x, spawn_y = world_map.spawn_point
            default_x = spawn_x + 5
            default_y = spawn_y

            # Check if default spawn monster was killed
            is_killed = any(
                km["x"] == default_x
                and km["y"] == default_y
                and km["map_id"] == current_map_id
                for km in self.killed_monsters
            )

            if not is_killed:
                monster_class = random.choice(ALL_MONSTER_CLASSES)
                monster = monster_class(default_x, default_y)
                self.monsters.append(monster)

    def spawn_chests(self, world_map, dungeon_manager):
        """
        Spawn chests from map data or at random locations, excluding opened chests.

        Args:
            world_map: The current world map
            dungeon_manager: The dungeon manager instance
        """
        self.chests = []
        current_map_id = dungeon_manager.current_map_id

        # Don't spawn chests in town
        if dungeon_manager.current_map_id == "town":
            return

        # Try to spawn chests from map data
        chest_spawns = world_map.get_entity_spawns("chests")
        if chest_spawns:
            for spawn in chest_spawns:
                chest_x = spawn["x"]
                chest_y = spawn["y"]

                # Check if this chest was already opened
                is_opened = any(
                    oc["x"] == chest_x
                    and oc["y"] == chest_y
                    and oc["map_id"] == current_map_id
                    for oc in self.opened_chests
                )

                if not is_opened:
                    chest = Chest(chest_x, chest_y)
                    self.chests.append(chest)
        else:
            # Fallback: Define positions where chests can spawn
            chest_positions = [
                (5, 3),  # Top middle area
                (10, 2),  # Top right area
                (7, 5),  # Center
                (3, 8),  # Bottom left
                (12, 9),  # Bottom right
                (8, 10),  # Bottom center
            ]

            # Randomly select 3-5 positions for chests
            num_chests = random.randint(3, 5)
            selected_positions = random.sample(chest_positions, num_chests)

            for grid_x, grid_y in selected_positions:
                # Check if this chest was already opened
                is_opened = any(
                    oc["x"] == grid_x
                    and oc["y"] == grid_y
                    and oc["map_id"] == current_map_id
                    for oc in self.opened_chests
                )

                if not is_opened:
                    chest = Chest(grid_x, grid_y)
                    self.chests.append(chest)

    def drop_item(self, item: Item, grid_x: int, grid_y: int):
        """
        Drop an item on the ground at specified grid coordinates.

        Args:
            item: The item to drop
            grid_x: Grid x position
            grid_y: Grid y position
        """
        ground_item = GroundItem(item, grid_x, grid_y)
        self.ground_items.append(ground_item)

    def get_item_at_position(self, grid_x: int, grid_y: int) -> Optional[GroundItem]:
        """
        Get the item at a specific position.

        Args:
            grid_x: Grid x position
            grid_y: Grid y position

        Returns:
            GroundItem if found, None otherwise
        """
        for ground_item in self.ground_items:
            if ground_item.grid_x == grid_x and ground_item.grid_y == grid_y:
                return ground_item
        return None

    def pickup_item_at_position(
        self, grid_x: int, grid_y: int, warrior: Warrior
    ) -> tuple[bool, str]:
        """
        Try to pick up an item at the specified grid position.

        Args:
            grid_x: Grid x position
            grid_y: Grid y position
            warrior: The warrior picking up the item

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Find item at this position
        for ground_item in self.ground_items:
            if ground_item.grid_x == grid_x and ground_item.grid_y == grid_y:
                # Check if it's a gold currency item (gold drops have "Gold" in name)
                from caislean_gaofar.objects.item import ItemType

                if (
                    ground_item.item.item_type == ItemType.MISC
                    and "Gold" in ground_item.item.name
                ):
                    # Add gold to currency instead of inventory
                    warrior.add_gold(ground_item.item.gold_value)
                    self.ground_items.remove(ground_item)
                    return True, f"Picked up {ground_item.item.gold_value} gold!"
                # Try to add regular item to inventory
                elif warrior.inventory.add_item(ground_item.item):
                    self.ground_items.remove(ground_item)
                    return True, f"Picked up {ground_item.item.name}!"
                else:
                    # Inventory full
                    return False, "Inventory is full!"
        return False, ""

    def get_nearest_alive_monster(self, warrior: Warrior):
        """
        Get the nearest alive monster to the warrior.

        Args:
            warrior: The warrior to measure distance from

        Returns:
            The nearest alive monster, or None if no monsters are alive
        """
        nearest_monster = None
        min_distance = float("inf")
        for monster in self.monsters:
            if monster.is_alive:
                distance = warrior.grid_distance_to(monster)
                if distance < min_distance:
                    min_distance = distance
                    nearest_monster = monster
        return nearest_monster

    def check_monster_deaths(
        self, dungeon_manager
    ) -> list[tuple[Item, int, int, str, int]]:
        """
        Check for dead monsters and prepare their loot drops.

        Args:
            dungeon_manager: The dungeon manager instance

        Returns:
            List of tuples (item, grid_x, grid_y, monster_type, xp_value) for loot drops
        """
        current_map_id = dungeon_manager.current_map_id
        loot_drops = []

        for monster in self.monsters[:]:  # Iterate over copy to allow removal
            if not monster.is_alive:
                # Track killed monster
                killed_entry = {
                    "type": monster.monster_type,
                    "x": monster.grid_x,
                    "y": monster.grid_y,
                    "map_id": current_map_id,
                }
                self.killed_monsters.append(killed_entry)
                print(
                    f"[DEBUG] Monster killed: {monster.monster_type} at ({monster.grid_x}, {monster.grid_y}) on map '{current_map_id}'"
                )

                # Use loot_table system to generate loot
                loot_item = get_loot_for_monster(monster.monster_type)

                if loot_item:
                    loot_drops.append(
                        (
                            loot_item,
                            monster.grid_x,
                            monster.grid_y,
                            monster.monster_type,
                            monster.xp_value,
                        )
                    )

                # Remove dead monster from list so loot only drops once
                self.monsters.remove(monster)

        return loot_drops

    def check_chest_collision(
        self, warrior: Warrior, dungeon_manager
    ) -> Optional[tuple[Item, int, int]]:
        """
        Check if warrior stepped on a chest and open it.

        Args:
            warrior: The warrior to check collision for
            dungeon_manager: The dungeon manager instance

        Returns:
            Tuple of (item, grid_x, grid_y) if chest was opened, None otherwise
        """
        current_map_id = dungeon_manager.current_map_id

        for chest in self.chests[:]:  # Iterate over copy to allow removal
            if (
                not chest.is_opened
                and chest.grid_x == warrior.grid_x
                and chest.grid_y == warrior.grid_y
            ):
                # Open the chest
                item = chest.open()

                # Track opened chest
                self.opened_chests.append(
                    {"x": chest.grid_x, "y": chest.grid_y, "map_id": current_map_id}
                )

                # Remove chest from list
                self.chests.remove(chest)

                return (item, chest.grid_x, chest.grid_y)

        return None

    def check_ground_item_pickup(self, warrior: Warrior) -> tuple[bool, str]:
        """
        Check if warrior is standing on a ground item and pick it up.

        Args:
            warrior: The warrior to check for

        Returns:
            Tuple of (success: bool, message: str)
        """
        for ground_item in self.ground_items[:]:  # Iterate over copy to allow removal
            if (
                ground_item.grid_x == warrior.grid_x
                and ground_item.grid_y == warrior.grid_y
            ):
                # Check if it's a gold currency item (gold drops have "Gold" in name)
                from caislean_gaofar.objects.item import ItemType

                if (
                    ground_item.item.item_type == ItemType.MISC
                    and "Gold" in ground_item.item.name
                ):
                    # Add gold to currency instead of inventory
                    warrior.add_gold(ground_item.item.gold_value)
                    self.ground_items.remove(ground_item)
                    return True, f"Picked up {ground_item.item.gold_value} gold!"
                # Try to add regular item to inventory
                elif warrior.inventory.add_item(ground_item.item):
                    # Successfully added
                    self.ground_items.remove(ground_item)
                    return True, f"Picked up {ground_item.item.name}!"
                else:
                    # Inventory full
                    return False, "Inventory is full!"
        return False, ""

    def clear_ground_items(self):
        """Clear all ground items."""
        self.ground_items = []

    def reset_tracking(self):
        """Reset tracking lists for killed monsters and opened chests."""
        self.killed_monsters = []
        self.opened_chests = []
