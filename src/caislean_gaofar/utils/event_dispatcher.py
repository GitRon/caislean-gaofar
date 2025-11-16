"""Event dispatching system for handling input and coordinating components."""

import pygame
from caislean_gaofar.utils.event_context import EventContext
from caislean_gaofar.core import config


class EventDispatcher:
    """Coordinates inter-component communication and event handling."""

    def __init__(self):
        """Initialize the event dispatcher."""
        self.running = True
        self.last_key_time = 0
        self.key_delay = 200  # milliseconds between key presses

    def handle_events(self, ctx: EventContext):
        """
        Handle pygame events and dispatch to appropriate handlers.

        Args:
            ctx: EventContext containing all event handler dependencies
        """
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event, current_time, ctx)

            # Handle inventory input when inventory is open
            if ctx.game_state_manager.state == config.STATE_INVENTORY:
                ctx.inventory_ui.handle_input(
                    event, ctx.warrior.inventory, ctx.inventory_game_ref
                )

            # Handle shop input when shop is open
            if ctx.game_state_manager.state == config.STATE_SHOP:
                ctx.shop_ui.handle_input(event, ctx.shop, ctx.warrior)

            # Handle skill UI input when skills screen is open
            if ctx.game_state_manager.state == config.STATE_SKILLS:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click - learn skill
                        ctx.skill_ui.handle_click(event.pos, ctx.warrior, False)
                    elif event.button == 3:  # Right click - set active
                        ctx.skill_ui.handle_click(event.pos, ctx.warrior, True)

    def _handle_keydown(self, event, current_time, ctx: EventContext):
        """
        Handle keydown events.

        Args:
            event: The pygame event
            current_time: Current time in milliseconds
            ctx: EventContext containing all event handler dependencies
        """
        # Global commands
        if event.key == pygame.K_ESCAPE:
            if ctx.game_state_manager.state == config.STATE_SHOP:
                if ctx.game_state_manager.return_portal:
                    ctx.on_use_return_portal()
            else:
                self.running = False

        # Game over commands
        elif (
            event.key == pygame.K_r
            and ctx.game_state_manager.state == config.STATE_GAME_OVER
        ):
            ctx.on_restart()

        # Quick save
        elif (
            event.key == pygame.K_F5
            and ctx.game_state_manager.state == config.STATE_PLAYING
        ):
            ctx.on_save("quicksave")

        # Inventory toggle
        elif event.key == pygame.K_i and ctx.game_state_manager.state in [
            config.STATE_PLAYING,
            config.STATE_INVENTORY,
            config.STATE_SHOP,
        ]:
            if ctx.game_state_manager.state == config.STATE_INVENTORY:
                ctx.game_state_manager.transition_from_inventory()
            else:
                ctx.game_state_manager.transition_to_inventory()

        # Skills toggle
        elif event.key == pygame.K_c and ctx.game_state_manager.state in [
            config.STATE_PLAYING,
            config.STATE_SKILLS,
        ]:
            if ctx.game_state_manager.state == config.STATE_PLAYING:
                ctx.game_state_manager.state = config.STATE_SKILLS
            else:
                ctx.game_state_manager.state = config.STATE_PLAYING

        # Shop toggle
        elif event.key == pygame.K_s and ctx.game_state_manager.state in [
            config.STATE_PLAYING,
            config.STATE_SHOP,
        ]:
            if ctx.game_state_manager.state == config.STATE_PLAYING:
                # Check if player is on town map and near shop
                is_near, message = ctx.on_shop_check()
                if is_near:
                    ctx.game_state_manager.transition_to_shop(True)
                else:
                    ctx.game_state_manager.show_message(message)
            else:
                # Exit shop without penalty
                ctx.game_state_manager.transition_from_shop()

        # Playing state commands
        elif ctx.game_state_manager.state == config.STATE_PLAYING:
            # Pickup (instant, doesn't consume a turn)
            if event.key == pygame.K_g:
                ctx.on_pickup_item(ctx.warrior.grid_x, ctx.warrior.grid_y)

            # Health potion usage (instant, doesn't consume a turn)
            elif event.key == pygame.K_p:
                ctx.on_use_potion()

            # Town portal usage (instant, doesn't consume a turn)
            elif event.key == pygame.K_t:
                ctx.on_use_town_portal()

            # Turn-based movement input
            elif ctx.turn_processor.waiting_for_player_input:
                if current_time - self.last_key_time >= self.key_delay:
                    action_queued = False
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        ctx.turn_processor.queue_player_action(
                            "move", ctx.warrior, 0, -1
                        )
                        action_queued = True
                    elif event.key in [pygame.K_s, pygame.K_DOWN]:
                        ctx.turn_processor.queue_player_action(
                            "move", ctx.warrior, 0, 1
                        )
                        action_queued = True
                    elif event.key in [pygame.K_a, pygame.K_LEFT]:
                        ctx.turn_processor.queue_player_action(
                            "move", ctx.warrior, -1, 0
                        )
                        action_queued = True
                    elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                        ctx.turn_processor.queue_player_action(
                            "move", ctx.warrior, 1, 0
                        )
                        action_queued = True
                    elif event.key == pygame.K_SPACE:
                        ctx.turn_processor.queue_player_action("attack", ctx.warrior)
                        action_queued = True

                    if action_queued:
                        self.last_key_time = current_time

        # Shop state - return portal usage
        elif (
            event.key == pygame.K_t
            and ctx.game_state_manager.state == config.STATE_SHOP
        ):
            if ctx.game_state_manager.return_portal:
                ctx.on_use_return_portal()

    def reset(self):
        """Reset event dispatcher state."""
        self.last_key_time = 0
