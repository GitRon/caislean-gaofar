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

# Monster types
MONSTER_TYPE_BANSHEE = "banshee"
MONSTER_TYPE_LEPRECHAUN = "leprechaun"
MONSTER_TYPE_POOKA = "pooka"
MONSTER_TYPE_SELKIE = "selkie"
MONSTER_TYPE_DULLAHAN = "dullahan"
MONSTER_TYPE_CHANGELING = "changeling"
MONSTER_TYPE_CLURICHAUN = "clurichaun"
MONSTER_TYPE_MERROW = "merrow"
MONSTER_TYPE_FEAR_GORTA = "fear_gorta"
MONSTER_TYPE_CAT_SI = "cat_si"

# Monster type stats (health, attack_damage, speed, chase_range, attack_range)
MONSTER_STATS = {
    MONSTER_TYPE_BANSHEE: {
        'health': 60,
        'attack_damage': 12,
        'speed': 1,
        'chase_range': 6,
        'attack_range': 2,  # Can wail from a distance
        'description': 'Ghostly spirit - fast, ranged attacks'
    },
    MONSTER_TYPE_LEPRECHAUN: {
        'health': 40,
        'attack_damage': 8,
        'speed': 2,  # Very fast and tricky
        'chase_range': 4,
        'attack_range': 1,
        'description': 'Mischievous fairy - weak but very fast'
    },
    MONSTER_TYPE_POOKA: {
        'health': 100,
        'attack_damage': 15,
        'speed': 1,
        'chase_range': 7,  # Pursues relentlessly
        'attack_range': 1,
        'description': 'Shape-shifter - high health, relentless pursuit'
    },
    MONSTER_TYPE_SELKIE: {
        'health': 70,
        'attack_damage': 10,
        'speed': 1,
        'chase_range': 5,
        'attack_range': 1,
        'description': 'Seal-human hybrid - balanced stats'
    },
    MONSTER_TYPE_DULLAHAN: {
        'health': 120,
        'attack_damage': 20,
        'speed': 1,
        'chase_range': 8,  # Omen of death, wide chase range
        'attack_range': 1,
        'description': 'Headless rider - very powerful, deadly'
    },
    MONSTER_TYPE_CHANGELING: {
        'health': 50,
        'attack_damage': 14,
        'speed': 1,
        'chase_range': 4,
        'attack_range': 1,
        'description': 'Fairy child - deceptively dangerous'
    },
    MONSTER_TYPE_CLURICHAUN: {
        'health': 45,
        'attack_damage': 9,
        'speed': 1,  # Drunk, slower reactions
        'chase_range': 3,  # Short chase (guards wine cellars)
        'attack_range': 1,
        'description': 'Drunken fairy - weak but unpredictable'
    },
    MONSTER_TYPE_MERROW: {
        'health': 75,
        'attack_damage': 11,
        'speed': 1,
        'chase_range': 5,
        'attack_range': 1,
        'description': 'Sea being - moderate threat'
    },
    MONSTER_TYPE_FEAR_GORTA: {
        'health': 55,
        'attack_damage': 13,
        'speed': 1,
        'chase_range': 6,
        'attack_range': 1,
        'description': 'Hunger spirit - drains vitality'
    },
    MONSTER_TYPE_CAT_SI: {
        'health': 65,
        'attack_damage': 16,
        'speed': 2,  # Fast like a cat
        'chase_range': 5,
        'attack_range': 1,
        'description': 'Fairy cat - fast and deadly'
    },
}

# Game states
STATE_PLAYING = "playing"
STATE_VICTORY = "victory"
STATE_GAME_OVER = "game_over"
STATE_INVENTORY = "inventory"
