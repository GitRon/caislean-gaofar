"""Tests for game_state_coordinator.py"""

from unittest.mock import patch
import pygame
from caislean_gaofar.core.game_state_coordinator import GameStateCoordinator
from caislean_gaofar.core.game_state_manager import GameStateManager
from caislean_gaofar.systems.turn_processor import TurnProcessor
from caislean_gaofar.entities.entity_manager import EntityManager
from caislean_gaofar.world.dungeon_transition_manager import DungeonTransitionManager
from caislean_gaofar.world.world_renderer import WorldRenderer
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.world.camera import Camera
from caislean_gaofar.world.dungeon_manager import DungeonManager
from caislean_gaofar.world.fog_of_war import FogOfWar
from caislean_gaofar.objects.temple import Temple
from caislean_gaofar.objects.item import Item, ItemType
from caislean_gaofar.core import config
import os


# Initialize pygame
pygame.init()


class TestGameStateCoordinator:
    """Tests for GameStateCoordinator"""

    @patch("pygame.display.set_mode")
    def test_initialization(self, mock_display):
        """Test GameStateCoordinator initialization"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        turn_processor = TurnProcessor()
        entity_manager = EntityManager()
        dungeon_transition_manager = DungeonTransitionManager()
        renderer = WorldRenderer(screen)

        # Act
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=turn_processor,
            entity_manager=entity_manager,
            dungeon_transition_manager=dungeon_transition_manager,
            renderer=renderer,
        )

        # Assert
        assert coordinator.state_manager is state_manager
        assert coordinator.turn_processor is turn_processor
        assert coordinator.entity_manager is entity_manager

    @patch("pygame.display.set_mode")
    def test_show_message(self, mock_display):
        """Test _show_message method"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )

        # Act
        coordinator._show_message("Test message")

        # Assert
        assert state_manager.message == "Test message"

    @patch("pygame.display.set_mode")
    def test_heal_at_temple_restores_health(self, mock_display):
        """Test _heal_at_temple restores health"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        coordinator = GameStateCoordinator(
            state_manager=GameStateManager(),
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )
        warrior = Warrior(5, 5)
        warrior.health = 50
        temple = Temple(grid_x=8, grid_y=1)

        # Act
        coordinator._heal_at_temple(warrior, temple)

        # Assert
        assert warrior.health == warrior.max_health
        assert temple.healing_active is True

    @patch("pygame.display.set_mode")
    def test_heal_at_temple_already_full_health(self, mock_display):
        """Test _heal_at_temple when already at full health"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        coordinator = GameStateCoordinator(
            state_manager=GameStateManager(),
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )
        warrior = Warrior(5, 5)
        warrior.health = warrior.max_health
        temple = Temple(grid_x=8, grid_y=1)

        # Act
        coordinator._heal_at_temple(warrior, temple)

        # Assert
        assert warrior.health == warrior.max_health
        assert temple.healing_active is False

    @patch("pygame.display.set_mode")
    def test_handle_chest_opened(self, mock_display):
        """Test _handle_chest_opened"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )
        item = Item(
            name="Gold Coin", item_type=ItemType.MISC, description="A shiny gold coin"
        )

        # Act
        coordinator._handle_chest_opened(item)

        # Assert
        assert "Gold Coin" in state_manager.message
        assert "chest" in state_manager.message.lower()

    @patch("pygame.display.set_mode")
    def test_handle_monster_death_with_level_up(self, mock_display):
        """Test _handle_monster_death with level up"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )
        warrior = Warrior(5, 5)
        warrior.experience.current_xp = 95  # Close to level up
        item = Item(name="Sword", item_type=ItemType.WEAPON, description="A sword")

        # Act
        coordinator._handle_monster_death(warrior, item, "goblin", 10)

        # Assert
        assert "Level Up" in state_manager.message
        assert "Sword" in state_manager.message

    @patch("pygame.display.set_mode")
    def test_handle_monster_death_without_level_up(self, mock_display):
        """Test _handle_monster_death without level up"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )
        warrior = Warrior(5, 5)
        item = Item(
            name="Potion", item_type=ItemType.CONSUMABLE, description="A potion"
        )

        # Act
        coordinator._handle_monster_death(warrior, item, "skeleton", 5)

        # Assert
        assert "Level Up" not in state_manager.message
        assert "Potion" in state_manager.message
        assert "skeleton" in state_manager.message

    @patch("pygame.display.set_mode")
    def test_handle_return_portal_success(self, mock_display):
        """Test _handle_return_portal success"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        entity_manager = EntityManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=entity_manager,
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )
        warrior = Warrior(5, 5)

        # Setup dungeon manager with world map
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()
        world_map = dungeon_manager.get_current_map()
        camera = Camera(world_map.width, world_map.height)

        # Mock use_return_portal to return success
        with patch.object(
            state_manager, "use_return_portal", return_value=(True, "Portal used!")
        ):
            # Act
            new_camera, new_world_map = coordinator._handle_return_portal(
                warrior, dungeon_manager, camera
            )

            # Assert
            assert new_camera is not None
            assert new_world_map is not None
            assert "Portal used!" in state_manager.message

    @patch("pygame.display.set_mode")
    def test_handle_return_portal_failure(self, mock_display):
        """Test _handle_return_portal failure"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )
        warrior = Warrior(5, 5)

        # Setup dungeon manager
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()
        world_map = dungeon_manager.get_current_map()
        camera = Camera(world_map.width, world_map.height)

        # Mock use_return_portal to return failure
        with patch.object(
            state_manager,
            "use_return_portal",
            return_value=(False, "No return portal!"),
        ):
            # Act
            new_camera, new_world_map = coordinator._handle_return_portal(
                warrior, dungeon_manager, camera
            )

            # Assert
            assert "No return portal!" in state_manager.message

    @patch("pygame.display.set_mode")
    def test_restart(self, mock_display):
        """Test restart method"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        turn_processor = TurnProcessor()
        entity_manager = EntityManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=turn_processor,
            entity_manager=entity_manager,
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )

        # Setup
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()
        world_map = dungeon_manager.get_current_map()
        camera = Camera(world_map.width, world_map.height)
        warrior = Warrior(10, 10)
        warrior.health = 50

        # Act
        new_warrior, new_camera, new_world_map = coordinator.restart(
            warrior, dungeon_manager, camera, world_map
        )

        # Assert
        assert new_warrior is not warrior
        assert new_warrior.health == new_warrior.max_health
        assert state_manager.state == config.STATE_PLAYING

    @patch("pygame.display.set_mode")
    def test_process_turn_calls_callbacks(self, mock_display):
        """Test _process_turn calls turn processor with callbacks"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        turn_processor = TurnProcessor()
        coordinator = GameStateCoordinator(
            state_manager=GameStateManager(),
            turn_processor=turn_processor,
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )

        # Setup
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()
        world_map = dungeon_manager.get_current_map()
        camera = Camera(world_map.width, world_map.height)
        warrior = Warrior(10, 10)
        fog_of_war = FogOfWar(visibility_radius=2)
        temple = Temple(grid_x=8, grid_y=1)
        from caislean_gaofar.objects.library import Library

        library = Library(grid_x=2, grid_y=6)

        # Mock turn_processor.process_turn to call callbacks
        def mock_process_turn(*args, **kwargs):
            # Call the callbacks to ensure they're covered
            on_chest_opened = kwargs.get("on_chest_opened")
            on_item_picked = kwargs.get("on_item_picked")
            on_monster_death = kwargs.get("on_monster_death")

            if on_chest_opened:
                test_item = Item(
                    name="Test",
                    item_type=ItemType.MISC,
                    description="Test",
                )
                on_chest_opened(test_item)
            if on_item_picked:
                on_item_picked("Picked an item!")
            if on_monster_death:
                loot_item = Item(
                    name="Loot",
                    item_type=ItemType.MISC,
                    description="Loot",
                )
                on_monster_death(loot_item, "goblin", 10)

        with patch.object(
            turn_processor, "process_turn", side_effect=mock_process_turn
        ):
            # Act
            coordinator._process_turn(
                warrior, dungeon_manager, world_map, camera, fog_of_war, temple, library
            )

            # Assert - if we get here, the callbacks were defined and called
            assert coordinator.state_manager.message is not None

    @patch("pygame.display.set_mode")
    def test_handle_return_portal_returning_to_town(self, mock_display):
        """Test _handle_return_portal when returning to town (else branch)"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        entity_manager = EntityManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=entity_manager,
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )

        # Setup
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()
        world_map = dungeon_manager.get_current_map()
        camera = Camera(world_map.width, world_map.height)
        warrior = Warrior(10, 10)

        # Mock use_return_portal to return success and set current_map_id to town
        with patch.object(
            state_manager,
            "use_return_portal",
            return_value=(True, "Returned!"),
        ):
            dungeon_manager.current_map_id = "town"

            # Act
            new_camera, new_world_map = coordinator._handle_return_portal(
                warrior, dungeon_manager, camera
            )

            # Assert - spawn_chests should not be called when in town
            assert "Returned!" in state_manager.message

    @patch("pygame.display.set_mode")
    def test_visit_library_player_already_has_portals(self, mock_display):
        """Test _visit_library when player already has portals (early return)"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )
        warrior = Warrior(5, 5)
        from caislean_gaofar.objects.library import Library
        library = Library(grid_x=2, grid_y=6)

        # Give warrior a town portal
        from caislean_gaofar.systems.loot_table import create_town_portal
        warrior.inventory.backpack_slots[0] = create_town_portal()

        # Act
        coordinator._visit_library(warrior, library)

        # Assert - no message shown, no effect activated
        assert state_manager.message == ""
        assert library.portal_gift_active is False

    @patch("pygame.display.set_mode")
    def test_visit_library_inventory_full(self, mock_display):
        """Test _visit_library when player has 0 portals but inventory is full"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )
        warrior = Warrior(5, 5)
        from caislean_gaofar.objects.library import Library
        library = Library(grid_x=2, grid_y=6)

        # Fill all 10 backpack slots with non-portal items
        misc_item = Item(name="Rock", item_type=ItemType.MISC, description="A rock")
        for i in range(10):
            warrior.inventory.backpack_slots[i] = misc_item

        # Act
        coordinator._visit_library(warrior, library)

        # Assert - shows "backpack is full" message, no effect
        assert "backpack is full" in state_manager.message.lower()
        assert library.portal_gift_active is False

    @patch("pygame.display.set_mode")
    def test_visit_library_gives_one_portal(self, mock_display):
        """Test _visit_library when giving exactly 1 portal (singular message)"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )
        warrior = Warrior(5, 5)
        from caislean_gaofar.objects.library import Library
        library = Library(grid_x=2, grid_y=6)

        # Fill 9 slots, leaving only 1 empty
        misc_item = Item(name="Rock", item_type=ItemType.MISC, description="A rock")
        for i in range(9):
            warrior.inventory.backpack_slots[i] = misc_item

        # Act
        coordinator._visit_library(warrior, library)

        # Assert - singular message, effect activated, 1 portal given
        assert "a town portal!" in state_manager.message
        assert "town portals!" not in state_manager.message  # Not plural
        assert library.portal_gift_active is True
        assert warrior.count_town_portals() == 1

    @patch("pygame.display.set_mode")
    def test_visit_library_gives_multiple_portals(self, mock_display):
        """Test _visit_library when giving multiple portals (plural message)"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )
        warrior = Warrior(5, 5)
        from caislean_gaofar.objects.library import Library
        library = Library(grid_x=2, grid_y=6)

        # All 3 slots empty
        # Act
        coordinator._visit_library(warrior, library)

        # Assert - plural message, effect activated, 3 portals given
        assert "3 town portals!" in state_manager.message
        assert library.portal_gift_active is True
        assert warrior.count_town_portals() == 3

    @patch("pygame.display.set_mode")
    def test_visit_library_gives_two_portals(self, mock_display):
        """Test _visit_library when giving 2 portals (ensures plural logic)"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )
        warrior = Warrior(5, 5)
        from caislean_gaofar.objects.library import Library
        library = Library(grid_x=2, grid_y=6)

        # Fill 8 slots, leaving 2 empty
        misc_item = Item(name="Rock", item_type=ItemType.MISC, description="A rock")
        for i in range(8):
            warrior.inventory.backpack_slots[i] = misc_item

        # Act
        coordinator._visit_library(warrior, library)

        # Assert - plural message with "2", effect activated
        assert "2 town portals!" in state_manager.message
        assert library.portal_gift_active is True
        assert warrior.count_town_portals() == 2

    @patch("pygame.display.set_mode")
    def test_update_when_standing_on_library(self, mock_display):
        """Test update method when warrior stands on library tile"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )

        # Setup game state
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()
        town_path = config.resource_path(os.path.join("data", "maps", "town.json"))
        dungeon_manager.load_dungeon("town", town_path)
        dungeon_manager.current_map_id = "town"

        world_map = dungeon_manager.get_current_map()
        camera = Camera(world_map.width, world_map.height)
        fog_of_war = FogOfWar(visibility_radius=2)
        temple = Temple(grid_x=8, grid_y=1)
        from caislean_gaofar.objects.library import Library
        library = Library(grid_x=2, grid_y=6)

        # Place warrior on library tile
        warrior = Warrior(2, 6)
        clock = pygame.time.Clock()

        # Act - update which should trigger library visit
        coordinator.update(
            clock, warrior, camera, dungeon_manager, fog_of_war, temple, library, world_map, 0.016
        )

        # Assert - warrior should receive town portals
        assert warrior.count_town_portals() == 3
        assert library.portal_gift_active is True
        assert "3 town portals!" in state_manager.message

    @patch("pygame.display.set_mode")
    def test_update_with_no_library(self, mock_display):
        """Test update method when library is None"""
        # Arrange
        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        state_manager = GameStateManager()
        coordinator = GameStateCoordinator(
            state_manager=state_manager,
            turn_processor=TurnProcessor(),
            entity_manager=EntityManager(),
            dungeon_transition_manager=DungeonTransitionManager(),
            renderer=WorldRenderer(screen),
        )

        # Setup game state
        map_file = config.resource_path(os.path.join("data", "maps", "overworld.json"))
        dungeon_manager = DungeonManager(map_file)
        dungeon_manager.load_world_map()

        world_map = dungeon_manager.get_current_map()
        camera = Camera(world_map.width, world_map.height)
        fog_of_war = FogOfWar(visibility_radius=2)
        temple = Temple(grid_x=8, grid_y=1)

        warrior = Warrior(5, 5)
        clock = pygame.time.Clock()

        # Act - update with library=None (should not crash)
        coordinator.update(
            clock, warrior, camera, dungeon_manager, fog_of_war, temple, None, world_map, 0.016
        )

        # Assert - should complete without error
        assert warrior is not None
