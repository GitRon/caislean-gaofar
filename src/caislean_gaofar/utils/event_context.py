"""Event context for encapsulating event handler dependencies."""

from typing import Callable
from dataclasses import dataclass
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.core.game_state_manager import GameStateManager
from caislean_gaofar.systems.turn_processor import TurnProcessor
from caislean_gaofar.entities.entity_manager import EntityManager
from caislean_gaofar.ui.inventory_ui import InventoryUI
from caislean_gaofar.objects.shop import Shop
from caislean_gaofar.ui.shop_ui import ShopUI
from caislean_gaofar.ui.skill_ui import SkillUI


@dataclass
class EventContext:
    """
    Context object that encapsulates all dependencies needed for event handling.

    This reduces parameter explosion in EventDispatcher methods by grouping
    related dependencies into a single object.
    """

    # Core game objects
    warrior: Warrior
    game_state_manager: GameStateManager
    turn_processor: TurnProcessor
    entity_manager: EntityManager

    # UI components
    inventory_ui: InventoryUI
    shop: Shop
    shop_ui: ShopUI
    skill_ui: SkillUI

    # Managers
    dungeon_manager: object  # DungeonManager (avoiding circular import)

    # Callbacks
    on_restart: Callable
    on_save: Callable
    on_pickup_item: Callable
    on_use_potion: Callable
    on_use_town_portal: Callable
    on_use_return_portal: Callable
    on_shop_check: Callable

    # Game reference for inventory UI
    inventory_game_ref: object
