"""Game configuration and constants."""

import sys
import os


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.

    When running as a PyInstaller bundle, resources are extracted to a temp folder
    accessible via sys._MEIPASS. In development, we use the normal relative path.

    Args:
        relative_path: Path relative to the project root

    Returns:
        Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running in normal Python environment
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Warrior vs Monster"

# HUD layout settings
HUD_WIDTH = 200
HUD_HEIGHT = 600
GAME_AREA_WIDTH = 600  # SCREEN_WIDTH - HUD_WIDTH
GAME_AREA_HEIGHT = 600  # SCREEN_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 50, 220)
DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)  # Chest color
GOLD = (255, 215, 0)  # Ground item color

# Color aliases for readability
COLOR_WHITE = WHITE
COLOR_GROUND_ITEM = GOLD
COLOR_CHEST = BROWN

# Grid settings
TILE_SIZE = 50  # Size of each grid tile
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE  # 16 tiles
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE  # 12 tiles
GAME_GRID_WIDTH = GAME_AREA_WIDTH // TILE_SIZE  # 12 tiles (for game area without HUD)
GAME_GRID_HEIGHT = GAME_AREA_HEIGHT // TILE_SIZE  # 12 tiles

# Entity settings
WARRIOR_SIZE = TILE_SIZE  # Same as tile size
WARRIOR_SPEED = 1  # Movement in tiles per turn
WARRIOR_MAX_HEALTH = 100
WARRIOR_ATTACK_DAMAGE = 15
WARRIOR_ATTACK_COOLDOWN = 1  # turns between attacks

MONSTER_SIZE = TILE_SIZE  # Same as tile size
MONSTER_ATTACK_COOLDOWN = 1  # turns between attacks

# Note: All other monster stats (health, damage, speed, ranges) are defined
# in each monster class (see monsters/ directory)

# Game states
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_INVENTORY = "inventory"
