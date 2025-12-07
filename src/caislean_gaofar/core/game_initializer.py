"""Game initialization component - handles all subsystem initialization."""

from typing import TYPE_CHECKING
import os
import pygame
from caislean_gaofar.entities.warrior import Warrior
from caislean_gaofar.objects.shop import Shop
from caislean_gaofar.ui.skill_ui import SkillUI
from caislean_gaofar.objects.item import Item, ItemType
from caislean_gaofar.world.camera import Camera
from caislean_gaofar.world.dungeon_manager import DungeonManager
from caislean_gaofar.objects.temple import Temple
from caislean_gaofar.objects.library import Library
from caislean_gaofar.world.fog_of_war import FogOfWar
from caislean_gaofar.core import config
from caislean_gaofar.entities.entity_manager import EntityManager
from caislean_gaofar.systems.turn_processor import TurnProcessor
from caislean_gaofar.world.world_renderer import WorldRenderer
from caislean_gaofar.core.game_state_manager import GameStateManager
from caislean_gaofar.utils.event_dispatcher import EventDispatcher
from caislean_gaofar.core.game_loop import GameLoop
from caislean_gaofar.world.dungeon_transition_manager import DungeonTransitionManager

if TYPE_CHECKING:
    from caislean_gaofar.world.world_map import WorldMap


class GameComponents:
    """Container for all initialized game components."""

    def __init__(self):
        """Initialize empty container."""
        # Core pygame objects
        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None

        # Managers
        self.entity_manager: EntityManager | None = None
        self.turn_processor: TurnProcessor | None = None
        self.renderer: WorldRenderer | None = None
        self.state_manager: GameStateManager | None = None
        self.event_dispatcher: EventDispatcher | None = None
        self.game_loop: GameLoop | None = None
        self.dungeon_transition_manager: DungeonTransitionManager | None = None
        self.dungeon_manager: DungeonManager | None = None

        # World objects
        self.world_map: "WorldMap | None" = None
        self.camera: Camera | None = None
        self.fog_of_war: FogOfWar | None = None

        # Game entities
        self.warrior: Warrior | None = None
        self.shop: Shop | None = None
        self.temple: Temple | None = None
        self.library: Library | None = None
        self.skill_ui: SkillUI | None = None


class GameInitializer:
    """Handles initialization of all game subsystems."""

    def __init__(self, map_file: str | None = None):
        """
        Initialize the game initializer.

        Args:
            map_file: Optional path to map JSON file. If None, uses default map.
        """
        self.map_file = map_file

    def initialize(self) -> GameComponents:
        """
        Initialize all game subsystems and return them in a container.

        Returns:
            GameComponents containing all initialized subsystems
        """
        components = GameComponents()

        # Initialize pygame and display
        self._initialize_pygame(components)

        # Initialize core systems
        self._initialize_core_systems(components)

        # Initialize dungeon manager and world
        self._initialize_world(components)

        # Initialize game entities
        self._initialize_entities(components)

        # Initialize starting items
        assert components.warrior is not None
        self._add_starting_items(components.warrior)

        # Spawn monsters and chests
        assert components.entity_manager is not None
        components.entity_manager.spawn_monsters(
            components.world_map, components.dungeon_manager
        )
        components.entity_manager.spawn_chests(
            components.world_map, components.dungeon_manager
        )

        return components

    def _initialize_pygame(self, components: GameComponents):
        """
        Initialize pygame and create display.

        Args:
            components: GameComponents to populate
        """
        pygame.init()
        components.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(config.TITLE)
        components.clock = pygame.time.Clock()

    def _initialize_core_systems(self, components: GameComponents):
        """
        Initialize core game systems (managers, processors, etc.).

        Args:
            components: GameComponents to populate
        """
        components.entity_manager = EntityManager()
        components.turn_processor = TurnProcessor()
        assert components.screen is not None
        components.renderer = WorldRenderer(components.screen)
        components.state_manager = GameStateManager()
        components.event_dispatcher = EventDispatcher()
        assert components.clock is not None
        components.game_loop = GameLoop(components.clock)
        components.dungeon_transition_manager = DungeonTransitionManager()

    def _initialize_world(self, components: GameComponents):
        """
        Initialize world map, dungeons, and camera.

        Args:
            components: GameComponents to populate
        """
        # Determine map file path
        map_file = self.map_file
        if map_file is None:
            map_file = config.resource_path(
                os.path.join("data", "maps", "overworld.json")
            )
        else:
            # Apply resource_path to custom map if it's a relative path
            if not os.path.isabs(map_file):
                map_file = config.resource_path(map_file)

        # Initialize dungeon manager
        components.dungeon_manager = DungeonManager(map_file)
        components.dungeon_manager.load_world_map()

        # Load all dungeons
        self._load_dungeons(components.dungeon_manager)

        # Start in town instead of world map
        components.dungeon_manager.current_map_id = "town"

        # Set return location to town entrance on world map
        # This ensures first-time exit from town works correctly
        if components.dungeon_manager.town_entrance:
            components.dungeon_manager.return_location = (
                components.dungeon_manager.town_entrance
            )

        # Get current map (initially town)
        components.world_map = components.dungeon_manager.get_current_map()

        # Initialize camera
        components.camera = Camera(
            components.world_map.width, components.world_map.height
        )

        # Initialize fog of war (2 tile visibility radius)
        components.fog_of_war = FogOfWar(visibility_radius=2)

    def _load_dungeons(self, dungeon_manager: DungeonManager):
        """
        Load all dungeon maps.

        Args:
            dungeon_manager: DungeonManager to load dungeons into
        """
        # Load dungeons - map unique IDs to actual dungeon files
        dark_cave_path = config.resource_path(
            os.path.join("data", "maps", "dark_cave.json")
        )
        ancient_castle_path = config.resource_path(
            os.path.join("data", "maps", "ancient_castle.json")
        )

        # Cave-type dungeons
        dungeon_manager.load_dungeon("dark_cave_1", dark_cave_path)
        dungeon_manager.load_dungeon("mystic_grotto", dark_cave_path)
        dungeon_manager.load_dungeon("dark_woods_lair", dark_cave_path)
        dungeon_manager.load_dungeon("southern_caverns", dark_cave_path)

        # Castle-type dungeons
        dungeon_manager.load_dungeon("haunted_crypt", ancient_castle_path)
        dungeon_manager.load_dungeon("shadow_keep", ancient_castle_path)
        dungeon_manager.load_dungeon("ruined_fortress", ancient_castle_path)
        dungeon_manager.load_dungeon("ancient_keep", ancient_castle_path)

        # Town
        dungeon_manager.load_dungeon(
            "town", config.resource_path(os.path.join("data", "maps", "town.json"))
        )

    def _initialize_entities(self, components: GameComponents):
        """
        Initialize game entities (warrior, shop, temple, UI).

        Args:
            components: GameComponents to populate
        """
        # Initialize warrior at spawn point
        assert components.world_map is not None
        spawn_x, spawn_y = components.world_map.spawn_point
        components.warrior = Warrior(spawn_x, spawn_y)

        # Initialize skill UI
        components.skill_ui = SkillUI()

        # Initialize shop (located at specific position on town map)
        components.shop = Shop(grid_x=4, grid_y=3)

        # Initialize temple (located at specific position on town map)
        components.temple = Temple(grid_x=8, grid_y=1)

        # Initialize library (located at specific position on town map)
        components.library = Library(grid_x=2, grid_y=6)

    def _add_starting_items(self, warrior: Warrior):
        """
        Add starting equipment to warrior inventory.

        Args:
            warrior: Warrior to add items to
        """
        # Import loot table function for town portal
        from caislean_gaofar.systems.loot_table import create_town_portal

        # Create starting equipment
        short_sword = Item(
            name="Short Sword",
            item_type=ItemType.WEAPON,
            description="A basic short sword",
            attack_bonus=3,
            gold_value=30,
        )
        woolen_tunic = Item(
            name="Woolen Tunic",
            item_type=ItemType.ARMOR,
            description="A simple woolen tunic",
            defense_bonus=1,
            gold_value=10,
        )
        health_potion = Item(
            name="Health Potion",
            item_type=ItemType.CONSUMABLE,
            description="Restores 30 HP",
            gold_value=30,
        )

        # Equip starting items
        warrior.inventory.add_item(short_sword)
        warrior.inventory.add_item(woolen_tunic)
        warrior.inventory.add_item(health_potion)

        # Add a starting town portal
        warrior.inventory.add_item(create_town_portal())

        # Player starts with some gold
        warrior.add_gold(100)
