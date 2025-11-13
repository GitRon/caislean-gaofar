"""Unit tests for TurnProcessor class."""

from unittest.mock import Mock
from caislean_gaofar.systems.turn_processor import TurnProcessor
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.entities.entity_manager import EntityManager


class TestTurnProcessor:
    """Test cases for TurnProcessor class."""

    def test_initialization(self):
        """Test TurnProcessor initialization."""
        processor = TurnProcessor()
        assert processor.waiting_for_player_input is True

    def test_process_turn_full_sequence(self):
        """Test processing a complete turn with all callbacks."""
        # Arrange
        processor = TurnProcessor()

        warrior = Mock(spec=Warrior)
        warrior.on_turn_start = Mock()
        warrior.execute_turn = Mock()

        entity_manager = Mock(spec=EntityManager)
        nearest_monster = Mock()
        entity_manager.get_nearest_alive_monster.return_value = nearest_monster
        entity_manager.check_chest_collision.return_value = None
        entity_manager.check_ground_item_pickup.return_value = (False, "")
        entity_manager.check_monster_deaths.return_value = []

        monster1 = Mock(is_alive=True)
        monster1.on_turn_start = Mock()
        monster1.execute_turn = Mock()

        monster2 = Mock(is_alive=True)
        monster2.on_turn_start = Mock()
        monster2.execute_turn = Mock()

        entity_manager.monsters = [monster1, monster2]

        world_map = Mock()
        dungeon_manager = Mock()

        on_dungeon_transition = Mock()
        on_chest_opened = Mock()
        on_item_picked = Mock()
        on_monster_death = Mock()

        # Act
        processor.process_turn(
            warrior=warrior,
            entity_manager=entity_manager,
            world_map=world_map,
            dungeon_manager=dungeon_manager,
            on_dungeon_transition=on_dungeon_transition,
            on_chest_opened=on_chest_opened,
            on_item_picked=on_item_picked,
            on_monster_death=on_monster_death,
        )

        # Assert
        warrior.on_turn_start.assert_called_once()
        warrior.execute_turn.assert_called_once_with(nearest_monster, world_map)
        on_dungeon_transition.assert_called_once()
        entity_manager.check_chest_collision.assert_called_once()
        entity_manager.check_ground_item_pickup.assert_called_once()
        entity_manager.check_monster_deaths.assert_called_once()
        monster1.on_turn_start.assert_called_once()
        monster1.execute_turn.assert_called_once_with(warrior, world_map)
        monster2.on_turn_start.assert_called_once()
        monster2.execute_turn.assert_called_once_with(warrior, world_map)
        assert processor.waiting_for_player_input is True

    def test_process_turn_with_chest_opened(self):
        """Test processing turn when chest is opened."""
        # Arrange
        processor = TurnProcessor()

        warrior = Mock()
        warrior.on_turn_start = Mock()
        warrior.execute_turn = Mock()

        from caislean_gaofar.objects.item import Item, ItemType

        chest_item = Item("Test Item", ItemType.MISC)

        entity_manager = Mock()
        entity_manager.get_nearest_alive_monster.return_value = None
        entity_manager.check_chest_collision.return_value = (chest_item, 5, 10)
        entity_manager.check_ground_item_pickup.return_value = (False, "")
        entity_manager.check_monster_deaths.return_value = []
        entity_manager.drop_item = Mock()
        entity_manager.monsters = []

        world_map = Mock()
        dungeon_manager = Mock()
        on_dungeon_transition = Mock()
        on_chest_opened = Mock()
        on_item_picked = Mock()
        on_monster_death = Mock()

        # Act
        processor.process_turn(
            warrior=warrior,
            entity_manager=entity_manager,
            world_map=world_map,
            dungeon_manager=dungeon_manager,
            on_dungeon_transition=on_dungeon_transition,
            on_chest_opened=on_chest_opened,
            on_item_picked=on_item_picked,
            on_monster_death=on_monster_death,
        )

        # Assert
        entity_manager.drop_item.assert_called_once_with(chest_item, 5, 10)
        on_chest_opened.assert_called_once_with(chest_item)

    def test_process_turn_with_item_pickup(self):
        """Test processing turn when item is picked up."""
        # Arrange
        processor = TurnProcessor()

        warrior = Mock()
        warrior.on_turn_start = Mock()
        warrior.execute_turn = Mock()

        entity_manager = Mock()
        entity_manager.get_nearest_alive_monster.return_value = None
        entity_manager.check_chest_collision.return_value = None
        entity_manager.check_ground_item_pickup.return_value = (
            True,
            "Picked up item!",
        )
        entity_manager.check_monster_deaths.return_value = []
        entity_manager.monsters = []

        world_map = Mock()
        dungeon_manager = Mock()
        on_dungeon_transition = Mock()
        on_chest_opened = Mock()
        on_item_picked = Mock()
        on_monster_death = Mock()

        # Act
        processor.process_turn(
            warrior=warrior,
            entity_manager=entity_manager,
            world_map=world_map,
            dungeon_manager=dungeon_manager,
            on_dungeon_transition=on_dungeon_transition,
            on_chest_opened=on_chest_opened,
            on_item_picked=on_item_picked,
            on_monster_death=on_monster_death,
        )

        # Assert
        on_item_picked.assert_called_once_with("Picked up item!")

    def test_process_turn_with_monster_death(self):
        """Test processing turn when monster dies and drops loot."""
        # Arrange
        processor = TurnProcessor()

        warrior = Mock()
        warrior.on_turn_start = Mock()
        warrior.execute_turn = Mock()

        from caislean_gaofar.objects.item import Item, ItemType

        loot_item = Item("Loot", ItemType.MISC)

        entity_manager = Mock()
        entity_manager.get_nearest_alive_monster.return_value = None
        entity_manager.check_chest_collision.return_value = None
        entity_manager.check_ground_item_pickup.return_value = (False, "")
        entity_manager.check_monster_deaths.return_value = [
            (loot_item, 7, 14, "banshee", 50)
        ]
        entity_manager.drop_item = Mock()
        entity_manager.monsters = []

        world_map = Mock()
        dungeon_manager = Mock()
        on_dungeon_transition = Mock()
        on_chest_opened = Mock()
        on_item_picked = Mock()
        on_monster_death = Mock()

        # Act
        processor.process_turn(
            warrior=warrior,
            entity_manager=entity_manager,
            world_map=world_map,
            dungeon_manager=dungeon_manager,
            on_dungeon_transition=on_dungeon_transition,
            on_chest_opened=on_chest_opened,
            on_item_picked=on_item_picked,
            on_monster_death=on_monster_death,
        )

        # Assert
        entity_manager.drop_item.assert_called_once_with(loot_item, 7, 14)
        on_monster_death.assert_called_once_with(loot_item, "banshee", 50)

    def test_process_turn_skips_dead_monsters(self):
        """Test that dead monsters don't take turns."""
        # Arrange
        processor = TurnProcessor()

        warrior = Mock()
        warrior.on_turn_start = Mock()
        warrior.execute_turn = Mock()

        entity_manager = Mock()
        entity_manager.get_nearest_alive_monster.return_value = None
        entity_manager.check_chest_collision.return_value = None
        entity_manager.check_ground_item_pickup.return_value = (False, "")
        entity_manager.check_monster_deaths.return_value = []

        alive_monster = Mock(is_alive=True)
        alive_monster.on_turn_start = Mock()
        alive_monster.execute_turn = Mock()

        dead_monster = Mock(is_alive=False)
        dead_monster.on_turn_start = Mock()
        dead_monster.execute_turn = Mock()

        entity_manager.monsters = [alive_monster, dead_monster]

        world_map = Mock()
        dungeon_manager = Mock()
        on_dungeon_transition = Mock()
        on_chest_opened = Mock()
        on_item_picked = Mock()
        on_monster_death = Mock()

        # Act
        processor.process_turn(
            warrior=warrior,
            entity_manager=entity_manager,
            world_map=world_map,
            dungeon_manager=dungeon_manager,
            on_dungeon_transition=on_dungeon_transition,
            on_chest_opened=on_chest_opened,
            on_item_picked=on_item_picked,
            on_monster_death=on_monster_death,
        )

        # Assert
        alive_monster.on_turn_start.assert_called_once()
        alive_monster.execute_turn.assert_called_once()
        dead_monster.on_turn_start.assert_not_called()
        dead_monster.execute_turn.assert_not_called()

    def test_queue_player_action_movement(self):
        """Test queuing a movement action."""
        # Arrange
        processor = TurnProcessor()
        processor.waiting_for_player_input = True

        warrior = Mock()
        warrior.queue_movement = Mock()

        # Act
        processor.queue_player_action("move", warrior, 1, 0)

        # Assert
        warrior.queue_movement.assert_called_once_with(1, 0)
        assert processor.waiting_for_player_input is False

    def test_queue_player_action_attack(self):
        """Test queuing an attack action."""
        # Arrange
        processor = TurnProcessor()
        processor.waiting_for_player_input = True

        warrior = Mock()
        warrior.queue_attack = Mock()

        # Act
        processor.queue_player_action("attack", warrior)

        # Assert
        warrior.queue_attack.assert_called_once()
        assert processor.waiting_for_player_input is False

    def test_reset(self):
        """Test resetting turn processor state."""
        # Arrange
        processor = TurnProcessor()
        processor.waiting_for_player_input = False

        # Act
        processor.reset()

        # Assert
        assert processor.waiting_for_player_input is True

    def test_queue_player_action_unknown_type(self):
        """Test queuing an unknown action type (does nothing but sets waiting to False)."""
        # Arrange
        processor = TurnProcessor()
        processor.waiting_for_player_input = True

        warrior = Mock()
        warrior.queue_movement = Mock()
        warrior.queue_attack = Mock()

        # Act
        processor.queue_player_action("unknown_action", warrior)

        # Assert - neither move nor attack should be called
        warrior.queue_movement.assert_not_called()
        warrior.queue_attack.assert_not_called()
        assert processor.waiting_for_player_input is False
