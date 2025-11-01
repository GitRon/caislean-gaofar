"""Game configuration and constants."""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Warrior vs Monster"

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

# Grid settings
TILE_SIZE = 50  # Size of each grid tile
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE  # 16 tiles
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE  # 12 tiles

# Entity settings
WARRIOR_SIZE = TILE_SIZE  # Same as tile size
WARRIOR_SPEED = 1  # Movement in tiles per turn
WARRIOR_MAX_HEALTH = 100
WARRIOR_ATTACK_DAMAGE = 15
WARRIOR_ATTACK_COOLDOWN = 1  # turns between attacks

MONSTER_SIZE = TILE_SIZE  # Same as tile size
MONSTER_SPEED = 1  # Movement in tiles per turn
MONSTER_MAX_HEALTH = 80
MONSTER_ATTACK_DAMAGE = 10
MONSTER_ATTACK_COOLDOWN = 1  # turns between attacks
MONSTER_CHASE_RANGE = 5  # Chase range in tiles
MONSTER_ATTACK_RANGE = 1  # Attack range in tiles (adjacent tiles)

# Game states
STATE_PLAYING = "playing"
STATE_VICTORY = "victory"
STATE_GAME_OVER = "game_over"
STATE_INVENTORY = "inventory"
