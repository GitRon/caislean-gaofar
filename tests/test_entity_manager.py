"""Unit tests for EntityManager class."""

from unittest.mock import Mock, patch
from entity_manager import EntityManager
from item import Item, ItemType
from chest import Chest


class TestEntityManager:
    """Test cases for EntityManager class."""

    def test_initialization(self):
        """Test EntityManager initialization."""
        manager = EntityManager()
        assert manager.monsters == []
        assert manager.chests == []
        assert manager.ground_items == []
        assert manager.killed_monsters == []
        assert manager.opened_chests == []

    @patch("entity_manager.ALL_MONSTER_CLASSES")
    def test_spawn_monsters_from_map_data(self, mock_monster_classes):
        """Test spawning monsters from map spawn data."""
        # Arrange
        mock_monster = Mock()
        mock_monster.MONSTER_TYPE = "banshee"
        mock_monster_classes.__iter__.return_value = [mock_monster]
        mock_monster_instance = Mock()
        mock_monster.return_value = mock_monster_instance

        world_map = Mock()
        world_map.get_entity_spawns.return_value = [
            {"type": "banshee", "x": 5, "y": 10}
        ]
        world_map.spawn_point = (0, 0)

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test_map"

        manager = EntityManager()

        # Act
        manager.spawn_monsters(world_map, dungeon_manager)

        # Assert
        assert len(manager.monsters) == 1
        mock_monster.assert_called_once_with(5, 10)

    @patch("entity_manager.ALL_MONSTER_CLASSES")
    @patch("entity_manager.random")
    def test_spawn_monsters_default_when_no_spawns(
        self, mock_random, mock_monster_classes
    ):
        """Test spawning default monster when no spawn data."""
        # Arrange
        mock_monster = Mock()
        mock_random.choice.return_value = mock_monster
        mock_monster_instance = Mock()
        mock_monster.return_value = mock_monster_instance

        world_map = Mock()
        world_map.get_entity_spawns.return_value = []
        world_map.spawn_point = (5, 5)

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test_map"

        manager = EntityManager()

        # Act
        manager.spawn_monsters(world_map, dungeon_manager)

        # Assert
        assert len(manager.monsters) == 1
        mock_monster.assert_called_once_with(10, 5)  # spawn_x + 5, spawn_y

    def test_spawn_monsters_skip_killed_monsters(self):
        """Test that killed monsters are not respawned."""
        # Arrange
        world_map = Mock()
        world_map.get_entity_spawns.return_value = [
            {"type": "banshee", "x": 5, "y": 10}
        ]
        world_map.spawn_point = (0, 0)

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test_map"

        manager = EntityManager()
        manager.killed_monsters = [
            {"type": "banshee", "x": 5, "y": 10, "map_id": "test_map"}
        ]

        # Act
        manager.spawn_monsters(world_map, dungeon_manager)

        # Assert
        assert len(manager.monsters) == 0

    def test_spawn_chests_from_map_data(self):
        """Test spawning chests from map spawn data."""
        # Arrange
        world_map = Mock()
        world_map.get_entity_spawns.return_value = [{"x": 3, "y": 7}]

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test_map"

        manager = EntityManager()

        # Act
        manager.spawn_chests(world_map, dungeon_manager)

        # Assert
        assert len(manager.chests) == 1
        assert manager.chests[0].grid_x == 3
        assert manager.chests[0].grid_y == 7

    def test_spawn_chests_skip_in_town(self):
        """Test that chests are not spawned in town."""
        # Arrange
        world_map = Mock()
        world_map.get_entity_spawns.return_value = [{"x": 3, "y": 7}]

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "town"

        manager = EntityManager()

        # Act
        manager.spawn_chests(world_map, dungeon_manager)

        # Assert
        assert len(manager.chests) == 0

    def test_spawn_chests_skip_opened_chests(self):
        """Test that opened chests are not respawned."""
        # Arrange
        world_map = Mock()
        world_map.get_entity_spawns.return_value = [{"x": 3, "y": 7}]

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test_map"

        manager = EntityManager()
        manager.opened_chests = [{"x": 3, "y": 7, "map_id": "test_map"}]

        # Act
        manager.spawn_chests(world_map, dungeon_manager)

        # Assert
        assert len(manager.chests) == 0

    @patch("entity_manager.random")
    def test_spawn_chests_random_fallback(self, mock_random):
        """Test spawning random chests when no spawn data."""
        # Arrange
        mock_random.randint.return_value = 3
        mock_random.sample.return_value = [(5, 3), (10, 2), (7, 5)]

        world_map = Mock()
        world_map.get_entity_spawns.return_value = []

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test_map"

        manager = EntityManager()

        # Act
        manager.spawn_chests(world_map, dungeon_manager)

        # Assert
        assert len(manager.chests) == 3

    def test_drop_item(self):
        """Test dropping an item on the ground."""
        # Arrange
        manager = EntityManager()
        item = Item("Test Item", ItemType.MISC)

        # Act
        manager.drop_item(item, 5, 10)

        # Assert
        assert len(manager.ground_items) == 1
        assert manager.ground_items[0].item == item
        assert manager.ground_items[0].grid_x == 5
        assert manager.ground_items[0].grid_y == 10

    def test_get_item_at_position_found(self):
        """Test getting an item at a position when one exists."""
        # Arrange
        manager = EntityManager()
        item = Item("Test Item", ItemType.MISC)
        manager.drop_item(item, 5, 10)

        # Act
        result = manager.get_item_at_position(5, 10)

        # Assert
        assert result is not None
        assert result.item == item

    def test_get_item_at_position_not_found(self):
        """Test getting an item at a position when none exists."""
        # Arrange
        manager = EntityManager()

        # Act
        result = manager.get_item_at_position(5, 10)

        # Assert
        assert result is None

    def test_pickup_item_at_position_gold(self):
        """Test picking up gold item."""
        # Arrange
        manager = EntityManager()
        gold_item = Item("Gold", ItemType.MISC, gold_value=50)
        manager.drop_item(gold_item, 5, 10)

        warrior = Mock()
        warrior.add_gold = Mock()

        # Act
        success, message = manager.pickup_item_at_position(5, 10, warrior)

        # Assert
        assert success is True
        assert "50 gold" in message
        warrior.add_gold.assert_called_once_with(50)
        assert len(manager.ground_items) == 0

    def test_pickup_item_at_position_regular_item_success(self):
        """Test picking up a regular item successfully."""
        # Arrange
        manager = EntityManager()
        item = Item("Sword", ItemType.WEAPON)
        manager.drop_item(item, 5, 10)

        warrior = Mock()
        warrior.inventory.add_item.return_value = True

        # Act
        success, message = manager.pickup_item_at_position(5, 10, warrior)

        # Assert
        assert success is True
        assert "Sword" in message
        warrior.inventory.add_item.assert_called_once_with(item)
        assert len(manager.ground_items) == 0

    def test_pickup_item_at_position_inventory_full(self):
        """Test picking up item when inventory is full."""
        # Arrange
        manager = EntityManager()
        item = Item("Sword", ItemType.WEAPON)
        manager.drop_item(item, 5, 10)

        warrior = Mock()
        warrior.inventory.add_item.return_value = False

        # Act
        success, message = manager.pickup_item_at_position(5, 10, warrior)

        # Assert
        assert success is False
        assert "full" in message.lower()
        assert len(manager.ground_items) == 1  # Item still on ground

    def test_pickup_item_at_position_no_item(self):
        """Test picking up when no item exists."""
        # Arrange
        manager = EntityManager()
        warrior = Mock()

        # Act
        success, message = manager.pickup_item_at_position(5, 10, warrior)

        # Assert
        assert success is False
        assert message == ""

    def test_get_nearest_alive_monster(self):
        """Test finding nearest alive monster."""
        # Arrange
        manager = EntityManager()

        warrior = Mock()
        warrior.grid_distance_to = Mock(side_effect=[5.0, 3.0, 10.0])

        monster1 = Mock(is_alive=True)
        monster2 = Mock(is_alive=True)
        monster3 = Mock(is_alive=True)

        manager.monsters = [monster1, monster2, monster3]

        # Act
        result = manager.get_nearest_alive_monster(warrior)

        # Assert
        assert result == monster2

    def test_get_nearest_alive_monster_none_alive(self):
        """Test finding nearest monster when none are alive."""
        # Arrange
        manager = EntityManager()

        warrior = Mock()

        monster1 = Mock(is_alive=False)
        monster2 = Mock(is_alive=False)

        manager.monsters = [monster1, monster2]

        # Act
        result = manager.get_nearest_alive_monster(warrior)

        # Assert
        assert result is None

    @patch("entity_manager.get_loot_for_monster")
    def test_check_monster_deaths(self, mock_get_loot):
        """Test checking for dead monsters and dropping loot."""
        # Arrange
        loot_item = Item("Loot", ItemType.MISC)
        mock_get_loot.return_value = loot_item

        manager = EntityManager()

        monster = Mock()
        monster.is_alive = False
        monster.monster_type = "banshee"
        monster.grid_x = 5
        monster.grid_y = 10

        manager.monsters = [monster]

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test_map"

        # Act
        loot_drops = manager.check_monster_deaths(dungeon_manager)

        # Assert
        assert len(loot_drops) == 1
        assert loot_drops[0][0] == loot_item
        assert loot_drops[0][1] == 5
        assert loot_drops[0][2] == 10
        assert loot_drops[0][3] == "banshee"
        assert len(manager.monsters) == 0  # Monster removed
        assert len(manager.killed_monsters) == 1

    def test_check_chest_collision_found(self):
        """Test checking chest collision when warrior steps on chest."""
        # Arrange
        manager = EntityManager()
        chest = Chest(5, 10)
        manager.chests = [chest]

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test_map"

        # Act
        result = manager.check_chest_collision(warrior, dungeon_manager)

        # Assert
        assert result is not None
        item, grid_x, grid_y = result
        assert grid_x == 5
        assert grid_y == 10
        assert len(manager.chests) == 0  # Chest removed
        assert len(manager.opened_chests) == 1

    def test_check_chest_collision_not_found(self):
        """Test checking chest collision when no collision."""
        # Arrange
        manager = EntityManager()
        chest = Chest(5, 10)
        manager.chests = [chest]

        warrior = Mock()
        warrior.grid_x = 7
        warrior.grid_y = 12

        dungeon_manager = Mock()

        # Act
        result = manager.check_chest_collision(warrior, dungeon_manager)

        # Assert
        assert result is None
        assert len(manager.chests) == 1  # Chest still there

    def test_check_ground_item_pickup_gold(self):
        """Test auto-pickup of gold on ground."""
        # Arrange
        manager = EntityManager()
        gold_item = Item("Gold", ItemType.MISC, gold_value=100)
        manager.drop_item(gold_item, 5, 10)

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10
        warrior.add_gold = Mock()

        # Act
        success, message = manager.check_ground_item_pickup(warrior)

        # Assert
        assert success is True
        assert "100 gold" in message
        warrior.add_gold.assert_called_once_with(100)
        assert len(manager.ground_items) == 0

    def test_check_ground_item_pickup_regular_item(self):
        """Test auto-pickup of regular item."""
        # Arrange
        manager = EntityManager()
        item = Item("Potion", ItemType.CONSUMABLE)
        manager.drop_item(item, 5, 10)

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10
        warrior.inventory.add_item.return_value = True

        # Act
        success, message = manager.check_ground_item_pickup(warrior)

        # Assert
        assert success is True
        assert "Potion" in message
        assert len(manager.ground_items) == 0

    def test_check_ground_item_pickup_inventory_full(self):
        """Test auto-pickup when inventory is full."""
        # Arrange
        manager = EntityManager()
        item = Item("Potion", ItemType.CONSUMABLE)
        manager.drop_item(item, 5, 10)

        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10
        warrior.inventory.add_item.return_value = False

        # Act
        success, message = manager.check_ground_item_pickup(warrior)

        # Assert
        assert success is False
        assert "full" in message.lower()
        assert len(manager.ground_items) == 1  # Item still on ground

    def test_check_ground_item_pickup_no_item(self):
        """Test auto-pickup when no item at position."""
        # Arrange
        manager = EntityManager()
        warrior = Mock()
        warrior.grid_x = 5
        warrior.grid_y = 10

        # Act
        success, message = manager.check_ground_item_pickup(warrior)

        # Assert
        assert success is False
        assert message == ""

    def test_clear_ground_items(self):
        """Test clearing all ground items."""
        # Arrange
        manager = EntityManager()
        item1 = Item("Item1", ItemType.MISC)
        item2 = Item("Item2", ItemType.MISC)
        manager.drop_item(item1, 1, 1)
        manager.drop_item(item2, 2, 2)

        # Act
        manager.clear_ground_items()

        # Assert
        assert len(manager.ground_items) == 0

    def test_reset_tracking(self):
        """Test resetting tracking lists."""
        # Arrange
        manager = EntityManager()
        manager.killed_monsters = [{"type": "test", "x": 1, "y": 1, "map_id": "map"}]
        manager.opened_chests = [{"x": 1, "y": 1, "map_id": "map"}]

        # Act
        manager.reset_tracking()

        # Assert
        assert len(manager.killed_monsters) == 0
        assert len(manager.opened_chests) == 0

    @patch("entity_manager.ALL_MONSTER_CLASSES")
    @patch("entity_manager.random")
    def test_spawn_monsters_unknown_type_fallback(
        self, mock_random, mock_monster_classes
    ):
        """Test spawning monster with unknown type falls back to random choice."""
        # Arrange
        mock_monster = Mock()
        mock_monster.MONSTER_TYPE = "known_type"
        mock_monster_classes.__iter__.return_value = [mock_monster]

        fallback_monster = Mock()
        mock_random.choice.return_value = fallback_monster
        mock_instance = Mock()
        fallback_monster.return_value = mock_instance

        world_map = Mock()
        world_map.get_entity_spawns.return_value = [
            {"type": "unknown_monster_type", "x": 7, "y": 8}
        ]
        world_map.spawn_point = (0, 0)

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test_map"

        manager = EntityManager()

        # Act
        manager.spawn_monsters(world_map, dungeon_manager)

        # Assert
        assert len(manager.monsters) == 1
        mock_random.choice.assert_called_once_with(mock_monster_classes)
        fallback_monster.assert_called_once_with(7, 8)

    def test_spawn_monsters_default_killed(self):
        """Test that default spawn monster is not created if already killed."""
        # Arrange
        world_map = Mock()
        world_map.get_entity_spawns.return_value = []
        world_map.spawn_point = (5, 5)

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test_map"

        manager = EntityManager()
        # Mark the default spawn position as killed
        manager.killed_monsters = [
            {"x": 10, "y": 5, "map_id": "test_map"}  # spawn_x + 5, spawn_y
        ]

        # Act
        manager.spawn_monsters(world_map, dungeon_manager)

        # Assert
        assert len(manager.monsters) == 0

    @patch("entity_manager.random")
    def test_spawn_chests_random_with_opened_chests(self, mock_random):
        """Test spawning random chests skips already opened chests."""
        # Arrange
        mock_random.randint.return_value = 3
        mock_random.sample.return_value = [(5, 3), (10, 2), (7, 5)]

        world_map = Mock()
        world_map.get_entity_spawns.return_value = []

        dungeon_manager = Mock()
        dungeon_manager.current_map_id = "test_map"

        manager = EntityManager()
        # Mark one of the random positions as already opened
        manager.opened_chests = [{"x": 5, "y": 3, "map_id": "test_map"}]

        # Act
        manager.spawn_chests(world_map, dungeon_manager)

        # Assert - only 2 chests should spawn (one was already opened)
        assert len(manager.chests) == 2
