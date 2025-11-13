"""Turn processing system for managing game turns and actions."""

from typing import Callable, TYPE_CHECKING
from warrior import Warrior
from entity_manager import EntityManager

if TYPE_CHECKING:
    from attack_effect import AttackEffectManager


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
        attack_effect_manager: "AttackEffectManager" = None,
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
            attack_effect_manager: Optional attack effect manager for visual effects
        """
        # Hero turn
        warrior.on_turn_start()

        # Find nearest monster for targeting
        nearest_monster = entity_manager.get_nearest_alive_monster(warrior)

        result = warrior.execute_turn(nearest_monster, world_map)

        # Trigger attack visual effect if warrior attacked successfully
        if (
            attack_effect_manager
            and result.get("success")
            and nearest_monster
            and result.get("damage", 0) > 0
        ):
            # Get center position of target for effect
            target_x = nearest_monster.x + nearest_monster.size / 2
            target_y = nearest_monster.y + nearest_monster.size / 2
            is_crit = result.get("crit", False)
            attack_effect_manager.add_effect(target_x, target_y, is_crit)

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
        for loot_item, grid_x, grid_y, monster_type, xp_value in loot_drops:
            # Create ground item at monster location
            entity_manager.drop_item(loot_item, grid_x, grid_y)
            on_monster_death(loot_item, monster_type, xp_value)

        # Monster turns
        for monster in entity_manager.monsters:
            if monster.is_alive:
                monster.on_turn_start()

                # Check if monster will attack (in range and can attack)
                can_attack = (
                    monster.grid_distance_to(warrior) <= monster.attack_range
                    and monster.can_attack()
                )

                monster.execute_turn(warrior, world_map)

                # Trigger attack visual effect if monster attacked
                if attack_effect_manager and can_attack and warrior.is_alive:
                    # Get center position of warrior for effect
                    target_x = warrior.x + warrior.size / 2
                    target_y = warrior.y + warrior.size / 2
                    attack_effect_manager.add_effect(target_x, target_y, False)

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
