"""Save game functionality for persisting game state."""

import datetime
import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class SaveGame:
    """Handle saving and loading game state."""

    SAVE_DIR = "saves"
    SAVE_EXTENSION = ".sav"

    @staticmethod
    def ensure_save_directory():
        """Create save directory if it doesn't exist."""
        Path(SaveGame.SAVE_DIR).mkdir(exist_ok=True)

    @staticmethod
    def serialize_item(item) -> Optional[Dict]:
        """
        Serialize an Item to a dictionary.

        Args:
            item: Item object or None

        Returns:
            Dictionary representation or None
        """
        if item is None:
            return None

        return {
            "name": item.name,
            "item_type": item.item_type.value,
            "description": item.description,
            "attack_bonus": item.attack_bonus,
            "defense_bonus": item.defense_bonus,
            "health_bonus": item.health_bonus,
            "gold_value": item.gold_value,
        }

    @staticmethod
    def deserialize_item(data: Optional[Dict]):
        """
        Deserialize a dictionary to an Item.

        Args:
            data: Dictionary representation or None

        Returns:
            Item object or None
        """
        if data is None:
            return None

        from item import Item, ItemType

        return Item(
            name=data["name"],
            item_type=ItemType(data["item_type"]),
            description=data.get("description", ""),
            attack_bonus=data.get("attack_bonus", 0),
            defense_bonus=data.get("defense_bonus", 0),
            health_bonus=data.get("health_bonus", 0),
            gold_value=data.get("gold_value", 0),
        )

    @staticmethod
    def serialize_inventory(inventory) -> Dict:
        """
        Serialize an Inventory to a dictionary.

        Args:
            inventory: Inventory object

        Returns:
            Dictionary representation
        """
        return {
            "weapon_slot": SaveGame.serialize_item(inventory.weapon_slot),
            "armor_slot": SaveGame.serialize_item(inventory.armor_slot),
            "backpack_slots": [
                SaveGame.serialize_item(item) for item in inventory.backpack_slots
            ],
        }

    @staticmethod
    def deserialize_inventory(data: Dict):
        """
        Deserialize a dictionary to an Inventory.

        Args:
            data: Dictionary representation

        Returns:
            Inventory object
        """
        from inventory import Inventory

        inventory = Inventory()
        inventory.weapon_slot = SaveGame.deserialize_item(data.get("weapon_slot"))
        inventory.armor_slot = SaveGame.deserialize_item(data.get("armor_slot"))
        inventory.backpack_slots = [
            SaveGame.deserialize_item(item) for item in data.get("backpack_slots", [])
        ]
        return inventory

    @staticmethod
    def save_game(game, filename: str = "quicksave") -> bool:
        """
        Save the current game state to a file.

        Args:
            game: Game object to save
            filename: Name of the save file (without extension)

        Returns:
            True if save was successful, False otherwise
        """
        try:
            SaveGame.ensure_save_directory()

            # Serialize game state
            save_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "player": {
                    "grid_x": game.warrior.grid_x,
                    "grid_y": game.warrior.grid_y,
                    "health": game.warrior.health,
                    "max_health": game.warrior.max_health,
                    "gold": game.warrior.gold,
                    "inventory": SaveGame.serialize_inventory(game.warrior.inventory),
                },
                "current_map_id": game.dungeon_manager.current_map_id,
                "return_location": game.dungeon_manager.return_location,
                "killed_monsters": game.killed_monsters,
                "opened_chests": game.opened_chests,
                "ground_items": [
                    {
                        "item": SaveGame.serialize_item(gi.item),
                        "grid_x": gi.grid_x,
                        "grid_y": gi.grid_y,
                        "map_id": game.dungeon_manager.current_map_id,
                    }
                    for gi in game.ground_items
                ],
            }

            # Write to file
            filepath = os.path.join(
                SaveGame.SAVE_DIR, filename + SaveGame.SAVE_EXTENSION
            )
            with open(filepath, "w") as f:
                json.dump(save_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    @staticmethod
    def load_game(filename: str = "quicksave") -> Optional[Dict]:
        """
        Load a game state from a file.

        Args:
            filename: Name of the save file (without extension)

        Returns:
            Dictionary containing game state, or None if load failed
        """
        try:
            filepath = os.path.join(
                SaveGame.SAVE_DIR, filename + SaveGame.SAVE_EXTENSION
            )

            if not os.path.exists(filepath):
                print(f"Save file not found: {filepath}")
                return None

            with open(filepath, "r") as f:
                save_data = json.load(f)

            return save_data

        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    @staticmethod
    def list_save_files() -> List[Dict]:
        """
        List all available save files with metadata.

        Returns:
            List of dictionaries containing save file info
        """
        SaveGame.ensure_save_directory()
        save_files = []

        for filename in os.listdir(SaveGame.SAVE_DIR):
            if filename.endswith(SaveGame.SAVE_EXTENSION):
                filepath = os.path.join(SaveGame.SAVE_DIR, filename)
                try:
                    with open(filepath, "r") as f:
                        data = json.load(f)

                    save_files.append(
                        {
                            "filename": filename[: -len(SaveGame.SAVE_EXTENSION)],
                            "timestamp": data.get("timestamp", "Unknown"),
                            "player_health": data.get("player", {}).get("health", "?"),
                            "player_gold": data.get("player", {}).get("gold", 0),
                            "current_map": data.get("current_map_id", "world"),
                        }
                    )
                except Exception as e:
                    print(f"Error reading save file {filename}: {e}")

        # Sort by timestamp (newest first)
        save_files.sort(key=lambda x: x["timestamp"], reverse=True)
        return save_files

    @staticmethod
    def delete_save(filename: str) -> bool:
        """
        Delete a save file.

        Args:
            filename: Name of the save file (without extension)

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            filepath = os.path.join(
                SaveGame.SAVE_DIR, filename + SaveGame.SAVE_EXTENSION
            )
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting save file: {e}")
            return False
