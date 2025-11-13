"""Event dispatching system for handling input and coordinating components."""

import pygame
from typing import Callable
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.core.game_state_manager import GameStateManager
from caislean_gaofar.systems.turn_processor import TurnProcessor
from caislean_gaofar.entities.entity_manager import EntityManager
from caislean_gaofar.ui.inventory_ui import InventoryUI
from caislean_gaofar.objects.shop import Shop
from caislean_gaofar.ui.shop_ui import ShopUI
from caislean_gaofar.core import config


class EventDispatcher:
    """Coordinates inter-component communication and event handling."""

    def __init__(self):
        """Initialize the event dispatcher."""
        self.running = True
        self.last_key_time = 0
        self.key_delay = 200  # milliseconds between key presses

    def handle_events(
        self,
        warrior: Warrior,
        game_state_manager: GameStateManager,
        turn_processor: TurnProcessor,
        entity_manager: EntityManager,
        inventory_ui: InventoryUI,
        shop: Shop,
        shop_ui: ShopUI,
        dungeon_manager,
        on_restart: Callable,
        on_save: Callable,
        on_pickup_item: Callable,
        on_use_potion: Callable,
        on_use_town_portal: Callable,
        on_use_return_portal: Callable,
        on_shop_check: Callable,
        inventory_game_ref,
    ):
        """
        Handle pygame events and dispatch to appropriate handlers.

        Args:
            warrior: The warrior entity
            game_state_manager: The game state manager
            turn_processor: The turn processor
            entity_manager: The entity manager
            inventory_ui: The inventory UI
            shop: The shop instance
            shop_ui: The shop UI
            dungeon_manager: The dungeon manager
            on_restart: Callback for restarting the game
            on_save: Callback for saving the game
            on_pickup_item: Callback for picking up items
            on_use_potion: Callback for using potions
            on_use_town_portal: Callback for using town portals
            on_use_return_portal: Callback for using return portals
            on_shop_check: Callback for checking shop proximity
            inventory_game_ref: Reference to game object for inventory UI
        """
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(
                    event,
                    current_time,
                    warrior,
                    game_state_manager,
                    turn_processor,
                    entity_manager,
                    inventory_ui,
                    shop,
                    shop_ui,
                    dungeon_manager,
                    on_restart,
                    on_save,
                    on_pickup_item,
                    on_use_potion,
                    on_use_town_portal,
                    on_use_return_portal,
                    on_shop_check,
                    inventory_game_ref,
                )

            # Handle inventory input when inventory is open
            if game_state_manager.state == config.STATE_INVENTORY:
                inventory_ui.handle_input(event, warrior.inventory, inventory_game_ref)

            # Handle shop input when shop is open
            if game_state_manager.state == config.STATE_SHOP:
                shop_ui.handle_input(event, shop, warrior)

    def _handle_keydown(
        self,
        event,
        current_time,
        warrior: Warrior,
        game_state_manager: GameStateManager,
        turn_processor: TurnProcessor,
        entity_manager: EntityManager,
        inventory_ui: InventoryUI,
        shop: Shop,
        shop_ui: ShopUI,
        dungeon_manager,
        on_restart: Callable,
        on_save: Callable,
        on_pickup_item: Callable,
        on_use_potion: Callable,
        on_use_town_portal: Callable,
        on_use_return_portal: Callable,
        on_shop_check: Callable,
        inventory_game_ref,
    ):
        """
        Handle keydown events.

        Args:
            event: The pygame event
            current_time: Current time in milliseconds
            warrior: The warrior entity
            game_state_manager: The game state manager
            turn_processor: The turn processor
            entity_manager: The entity manager
            inventory_ui: The inventory UI
            shop: The shop instance
            shop_ui: The shop UI
            dungeon_manager: The dungeon manager
            on_restart: Callback for restarting the game
            on_save: Callback for saving the game
            on_pickup_item: Callback for picking up items
            on_use_potion: Callback for using potions
            on_use_town_portal: Callback for using town portals
            on_use_return_portal: Callback for using return portals
            on_shop_check: Callback for checking shop proximity
            inventory_game_ref: Reference to game object for inventory UI
        """
        # Global commands
        if event.key == pygame.K_ESCAPE:
            if game_state_manager.state == config.STATE_SHOP:
                if game_state_manager.return_portal:
                    on_use_return_portal()
            else:
                self.running = False

        # Game over commands
        elif (
            event.key == pygame.K_r
            and game_state_manager.state == config.STATE_GAME_OVER
        ):
            on_restart()

        # Quick save
        elif (
            event.key == pygame.K_F5
            and game_state_manager.state == config.STATE_PLAYING
        ):
            on_save("quicksave")

        # Inventory toggle
        elif event.key == pygame.K_i and game_state_manager.state in [
            config.STATE_PLAYING,
            config.STATE_INVENTORY,
            config.STATE_SHOP,
        ]:
            if game_state_manager.state == config.STATE_INVENTORY:
                game_state_manager.transition_from_inventory()
            else:
                game_state_manager.transition_to_inventory()

        # Skills toggle
        elif event.key == pygame.K_c and game_state_manager.state in [
            config.STATE_PLAYING,
            config.STATE_SKILLS,
        ]:
            if game_state_manager.state == config.STATE_PLAYING:
                game_state_manager.state = config.STATE_SKILLS
            else:
                game_state_manager.state = config.STATE_PLAYING

        # Shop toggle
        elif event.key == pygame.K_s and game_state_manager.state in [
            config.STATE_PLAYING,
            config.STATE_SHOP,
        ]:
            if game_state_manager.state == config.STATE_PLAYING:
                # Check if player is on town map and near shop
                is_near, message = on_shop_check()
                if is_near:
                    game_state_manager.transition_to_shop(True)
                else:
                    game_state_manager.show_message(message)
            else:
                # Exit shop without penalty
                game_state_manager.transition_from_shop()

        # Playing state commands
        elif game_state_manager.state == config.STATE_PLAYING:
            # Pickup (instant, doesn't consume a turn)
            if event.key == pygame.K_g:
                on_pickup_item(warrior.grid_x, warrior.grid_y)

            # Health potion usage (instant, doesn't consume a turn)
            elif event.key == pygame.K_p:
                on_use_potion()

            # Town portal usage (instant, doesn't consume a turn)
            elif event.key == pygame.K_t:
                on_use_town_portal()

            # Turn-based movement input
            elif turn_processor.waiting_for_player_input:
                if current_time - self.last_key_time >= self.key_delay:
                    action_queued = False
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        turn_processor.queue_player_action("move", warrior, 0, -1)
                        action_queued = True
                    elif event.key in [pygame.K_s, pygame.K_DOWN]:
                        turn_processor.queue_player_action("move", warrior, 0, 1)
                        action_queued = True
                    elif event.key in [pygame.K_a, pygame.K_LEFT]:
                        turn_processor.queue_player_action("move", warrior, -1, 0)
                        action_queued = True
                    elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                        turn_processor.queue_player_action("move", warrior, 1, 0)
                        action_queued = True
                    elif event.key == pygame.K_SPACE:
                        turn_processor.queue_player_action("attack", warrior)
                        action_queued = True

                    if action_queued:
                        self.last_key_time = current_time

        # Shop state - return portal usage
        elif event.key == pygame.K_t and game_state_manager.state == config.STATE_SHOP:
            if game_state_manager.return_portal:
                on_use_return_portal()

    def reset(self):
        """Reset event dispatcher state."""
        self.last_key_time = 0
