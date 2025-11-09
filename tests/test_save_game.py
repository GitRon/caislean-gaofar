"""Tests for save game functionality."""

import os
import json
import tempfile
import shutil
import pytest
from save_game import SaveGame
from item import Item, ItemType
from inventory import Inventory


@pytest.fixture
def temp_save_dir(monkeypatch):
    """Create a temporary save directory for testing."""
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setattr(SaveGame, "SAVE_DIR", temp_dir)
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir)


def test_serialize_item_with_data():
    """Test serializing an item with all data."""
    item = Item(
        name="Test Sword",
        item_type=ItemType.WEAPON,
        description="A test weapon",
        attack_bonus=5,
        defense_bonus=1,
        health_bonus=2,
        gold_value=100,
    )

    serialized = SaveGame.serialize_item(item)

    assert serialized["name"] == "Test Sword"
    assert serialized["item_type"] == "weapon"
    assert serialized["description"] == "A test weapon"
    assert serialized["attack_bonus"] == 5
    assert serialized["defense_bonus"] == 1
    assert serialized["health_bonus"] == 2
    assert serialized["gold_value"] == 100


def test_serialize_item_none():
    """Test serializing None returns None."""
    assert SaveGame.serialize_item(None) is None


def test_deserialize_item_with_data():
    """Test deserializing an item with all data."""
    data = {
        "name": "Test Armor",
        "item_type": "armor",
        "description": "Test armor piece",
        "attack_bonus": 2,
        "defense_bonus": 5,
        "health_bonus": 10,
        "gold_value": 50,
    }

    item = SaveGame.deserialize_item(data)

    assert item.name == "Test Armor"
    assert item.item_type == ItemType.ARMOR
    assert item.description == "Test armor piece"
    assert item.attack_bonus == 2
    assert item.defense_bonus == 5
    assert item.health_bonus == 10
    assert item.gold_value == 50


def test_deserialize_item_none():
    """Test deserializing None returns None."""
    assert SaveGame.deserialize_item(None) is None


def test_deserialize_item_minimal_data():
    """Test deserializing an item with minimal data."""
    data = {
        "name": "Minimal Item",
        "item_type": "misc",
    }

    item = SaveGame.deserialize_item(data)

    assert item.name == "Minimal Item"
    assert item.item_type == ItemType.MISC
    assert item.description == ""
    assert item.attack_bonus == 0
    assert item.defense_bonus == 0
    assert item.health_bonus == 0
    assert item.gold_value == 0


def test_serialize_inventory():
    """Test serializing an inventory."""
    inventory = Inventory()

    weapon = Item("Sword", ItemType.WEAPON, attack_bonus=3)
    armor = Item("Shield", ItemType.ARMOR, defense_bonus=2)
    potion = Item("Potion", ItemType.CONSUMABLE, health_bonus=20)

    inventory.weapon_slot = weapon
    inventory.armor_slot = armor
    inventory.backpack_slots[0] = potion

    serialized = SaveGame.serialize_inventory(inventory)

    assert serialized["weapon_slot"]["name"] == "Sword"
    assert serialized["armor_slot"]["name"] == "Shield"
    assert serialized["backpack_slots"][0]["name"] == "Potion"
    assert serialized["backpack_slots"][1] is None


def test_deserialize_inventory():
    """Test deserializing an inventory."""
    data = {
        "weapon_slot": {
            "name": "Axe",
            "item_type": "weapon",
            "attack_bonus": 5,
        },
        "armor_slot": None,
        "backpack_slots": [
            {"name": "Gold Coin", "item_type": "misc", "gold_value": 10},
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ],
    }

    inventory = SaveGame.deserialize_inventory(data)

    assert inventory.weapon_slot.name == "Axe"
    assert inventory.weapon_slot.attack_bonus == 5
    assert inventory.armor_slot is None
    assert inventory.backpack_slots[0].name == "Gold Coin"
    assert inventory.backpack_slots[0].gold_value == 10
    assert inventory.backpack_slots[1] is None


def test_list_save_files_empty(temp_save_dir):
    """Test listing save files when directory is empty."""
    files = SaveGame.list_save_files()
    assert files == []


def test_list_save_files_with_saves(temp_save_dir):
    """Test listing save files with existing saves."""
    # Create some test save files
    save1 = {
        "timestamp": "2024-01-01T12:00:00",
        "player": {"health": 100, "gold": 50},
        "current_map_id": "world",
    }
    save2 = {
        "timestamp": "2024-01-02T12:00:00",
        "player": {"health": 80, "gold": 100},
        "current_map_id": "dungeon",
    }

    with open(os.path.join(temp_save_dir, "save1.sav"), "w") as f:
        json.dump(save1, f)
    with open(os.path.join(temp_save_dir, "save2.sav"), "w") as f:
        json.dump(save2, f)

    files = SaveGame.list_save_files()

    assert len(files) == 2
    # Should be sorted by timestamp (newest first)
    assert files[0]["filename"] == "save2"
    assert files[0]["timestamp"] == "2024-01-02T12:00:00"
    assert files[0]["player_health"] == 80
    assert files[0]["player_gold"] == 100
    assert files[0]["current_map"] == "dungeon"


def test_delete_save_existing(temp_save_dir):
    """Test deleting an existing save file."""
    # Create a test save
    filepath = os.path.join(temp_save_dir, "test.sav")
    with open(filepath, "w") as f:
        json.dump({"test": "data"}, f)

    assert os.path.exists(filepath)

    result = SaveGame.delete_save("test")
    assert result is True
    assert not os.path.exists(filepath)


def test_delete_save_nonexistent(temp_save_dir):
    """Test deleting a non-existent save file."""
    result = SaveGame.delete_save("nonexistent")
    assert result is False


def test_ensure_save_directory(temp_save_dir):
    """Test that ensure_save_directory creates the directory."""
    # Remove the directory
    shutil.rmtree(temp_save_dir)
    assert not os.path.exists(temp_save_dir)

    # Ensure it gets created
    SaveGame.ensure_save_directory()
    assert os.path.exists(temp_save_dir)


def test_save_game_creates_file(temp_save_dir):
    """Test that save_game creates a save file with correct data."""
    from unittest.mock import MagicMock
    from warrior import Warrior

    # Create a mock game object
    game = MagicMock()
    game.warrior = Warrior(5, 10)
    game.warrior.health = 80
    game.warrior.gold = 100
    game.dungeon_manager = MagicMock()
    game.dungeon_manager.current_map_id = "world"
    game.dungeon_manager.return_location = None
    game.killed_monsters = [{"type": "banshee", "x": 3, "y": 4, "map_id": "world"}]
    game.opened_chests = [{"x": 5, "y": 6, "map_id": "world"}]
    game.ground_items = []

    # Save the game
    result = SaveGame.save_game(game, "test_save")
    assert result is True

    # Verify file was created
    filepath = os.path.join(temp_save_dir, "test_save.sav")
    assert os.path.exists(filepath)

    # Load and verify contents
    with open(filepath, "r") as f:
        data = json.load(f)

    assert "timestamp" in data
    assert data["player"]["grid_x"] == 5
    assert data["player"]["grid_y"] == 10
    assert data["player"]["health"] == 80
    assert data["player"]["gold"] == 100
    assert data["current_map_id"] == "world"
    assert len(data["killed_monsters"]) == 1
    assert len(data["opened_chests"]) == 1


def test_load_game_returns_data(temp_save_dir):
    """Test that load_game returns correct data."""
    # Create a test save file
    save_data = {
        "timestamp": "2024-01-01T12:00:00",
        "player": {
            "grid_x": 7,
            "grid_y": 8,
            "health": 90,
            "max_health": 100,
            "gold": 50,
            "inventory": {
                "weapon_slot": None,
                "armor_slot": None,
                "backpack_slots": [None] * 13,
            },
        },
        "current_map_id": "dungeon",
        "return_location": [5, 6],
        "killed_monsters": [],
        "opened_chests": [],
        "ground_items": [],
    }

    filepath = os.path.join(temp_save_dir, "test_load.sav")
    with open(filepath, "w") as f:
        json.dump(save_data, f)

    # Load the game
    loaded_data = SaveGame.load_game("test_load")

    assert loaded_data is not None
    assert loaded_data["player"]["grid_x"] == 7
    assert loaded_data["player"]["grid_y"] == 8
    assert loaded_data["current_map_id"] == "dungeon"
    assert loaded_data["return_location"] == [5, 6]


def test_load_game_nonexistent_file(temp_save_dir):
    """Test that load_game returns None for nonexistent file."""
    result = SaveGame.load_game("nonexistent")
    assert result is None


def test_save_game_with_ground_items(temp_save_dir):
    """Test saving game with ground items."""
    from unittest.mock import MagicMock
    from warrior import Warrior
    from ground_item import GroundItem
    from item import Item, ItemType

    # Create a mock game object
    game = MagicMock()
    game.warrior = Warrior(5, 10)
    game.dungeon_manager = MagicMock()
    game.dungeon_manager.current_map_id = "world"
    game.dungeon_manager.return_location = None
    game.killed_monsters = []
    game.opened_chests = []

    # Add a ground item
    item = Item("Test Item", ItemType.MISC, gold_value=10)
    ground_item = GroundItem(item, 3, 4)
    game.ground_items = [ground_item]

    # Save the game
    result = SaveGame.save_game(game, "test_ground_items")
    assert result is True

    # Load and verify
    filepath = os.path.join(temp_save_dir, "test_ground_items.sav")
    with open(filepath, "r") as f:
        data = json.load(f)

    assert len(data["ground_items"]) == 1
    assert data["ground_items"][0]["item"]["name"] == "Test Item"
    assert data["ground_items"][0]["grid_x"] == 3
    assert data["ground_items"][0]["grid_y"] == 4


def test_list_save_files_handles_invalid_file(temp_save_dir):
    """Test that list_save_files handles invalid JSON gracefully."""
    # Create an invalid save file
    filepath = os.path.join(temp_save_dir, "invalid.sav")
    with open(filepath, "w") as f:
        f.write("invalid json{{{")

    # Should not crash, just skip the invalid file
    files = SaveGame.list_save_files()
    assert files == []


def test_save_game_handles_exception(temp_save_dir):
    """Test that save_game handles exceptions gracefully."""
    from unittest.mock import MagicMock, patch

    # Create a mock game object
    game = MagicMock()
    game.warrior = MagicMock()
    game.warrior.grid_x = 5
    game.warrior.grid_y = 10

    # Make json.dump raise an exception
    with patch("save_game.json.dump", side_effect=Exception("Test error")):
        result = SaveGame.save_game(game, "test_error")
        assert result is False


def test_load_game_handles_exception(temp_save_dir):
    """Test that load_game handles JSON decode errors."""
    # Create a file with invalid JSON
    filepath = os.path.join(temp_save_dir, "corrupt.sav")
    with open(filepath, "w") as f:
        f.write("{ invalid json")

    result = SaveGame.load_game("corrupt")
    assert result is None


def test_delete_save_handles_exception(temp_save_dir):
    """Test that delete_save handles exceptions gracefully."""
    from unittest.mock import patch

    # Make os.remove raise an exception
    filepath = os.path.join(temp_save_dir, "test.sav")
    with open(filepath, "w") as f:
        json.dump({"test": "data"}, f)

    with patch("save_game.os.remove", side_effect=Exception("Test error")):
        result = SaveGame.delete_save("test")
        assert result is False


def test_list_save_files_ignores_non_sav_files(temp_save_dir):
    """Test that list_save_files ignores files that don't have .sav extension."""
    # Create a valid save file
    save_data = {
        "timestamp": "2024-01-01T12:00:00",
        "player": {"health": 100, "gold": 50},
        "current_map_id": "world",
    }
    with open(os.path.join(temp_save_dir, "save1.sav"), "w") as f:
        json.dump(save_data, f)

    # Create a non-save file in the same directory
    with open(os.path.join(temp_save_dir, "readme.txt"), "w") as f:
        f.write("This is not a save file")

    files = SaveGame.list_save_files()

    # Should only include the .sav file
    assert len(files) == 1
    assert files[0]["filename"] == "save1"
