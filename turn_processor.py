"""Turn processing system for managing game turns and actions."""

from typing import Callable
from warrior import Warrior
from entity_manager import EntityManager


class TurnProcessor:
    """Manages combat and turn logic."""

    def __init__(self):
        """Initialize the turn processor."""
        self.waiting_for_player_input = True

    def process_turn(
        self,
        warrior: Warrior,
        entity_manager: EntityManager,
        world_map,
        dungeon_manager,
        on_dungeon_transition: Callable,
        on_chest_opened: Callable,
        on_item_picked: Callable,
        on_monster_death: Callable,
    ):
        """
        Process one complete turn (hero then monsters).

        Args:
            warrior: The warrior entity
            entity_manager: The entity manager
            world_map: The current world map
            dungeon_manager: The dungeon manager
            on_dungeon_transition: Callback for dungeon transitions
            on_chest_opened: Callback when chest is opened
            on_item_picked: Callback when item is picked up
            on_monster_death: Callback when monster dies
        """
        # Hero turn
        warrior.on_turn_start()

        # Find nearest monster for targeting
        nearest_monster = entity_manager.get_nearest_alive_monster(warrior)

        warrior.execute_turn(nearest_monster, world_map)

        # Check for dungeon entrance/exit after warrior moves
        on_dungeon_transition()

        # Check for chest collision after warrior moves
        chest_result = entity_manager.check_chest_collision(warrior, dungeon_manager)
        if chest_result:
            item, grid_x, grid_y = chest_result
            # Create ground item at chest location
            entity_manager.drop_item(item, grid_x, grid_y)
            on_chest_opened(item)

        # Check for ground item pickup after warrior moves
        success, message = entity_manager.check_ground_item_pickup(warrior)
        if success or message:
            on_item_picked(message)

        # Check for monster deaths and drop loot (after warrior attacks)
        loot_drops = entity_manager.check_monster_deaths(dungeon_manager)
        for loot_item, grid_x, grid_y, monster_type in loot_drops:
            # Create ground item at monster location
            entity_manager.drop_item(loot_item, grid_x, grid_y)
            on_monster_death(loot_item, monster_type)

        # Monster turns
        for monster in entity_manager.monsters:
            if monster.is_alive:
                monster.on_turn_start()
                monster.execute_turn(warrior, world_map)

        # Wait for next player input
        self.waiting_for_player_input = True

    def queue_player_action(self, action_type: str, warrior: Warrior, *args):
        """
        Queue a player action for execution.

        Args:
            action_type: Type of action ('move' or 'attack')
            warrior: The warrior entity
            *args: Additional arguments for the action
        """
        if action_type == "move":
            dx, dy = args
            warrior.queue_movement(dx, dy)
        elif action_type == "attack":
            warrior.queue_attack()

        self.waiting_for_player_input = False

    def reset(self):
        """Reset turn processor state."""
        self.waiting_for_player_input = True
