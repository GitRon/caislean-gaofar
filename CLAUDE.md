# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a PyGame-based action RPG inspired by "Castle of the Winds". The game features real-time combat between a player-controlled warrior and an AI-controlled monster, with an inventory system for equipment management.

## Running the Game

```bash
# Run the game
python main.py
```

The project uses `uv` for dependency management (Python 3.13+) with pygame as the only dependency.

## Git Branching Conventions

**IMPORTANT**: When creating new branches for development, follow this naming convention:

```
<prefix>/#<ticket-id>-<description>
```

**Prefix options**:
- `feature` - For new features or enhancements
- `refactor` - For code refactoring without changing functionality
- `bugfix` - For bug fixes

**Format rules**:
- Use a forward slash (`/`) after the prefix
- Follow with `#` and the ticket/issue ID
- Add a descriptive name of the feature/issue
- Replace all whitespaces with hyphens (`-`)
- Use lowercase for consistency

**Examples**:
```
feature/#12-mouse-driven-inventory
bugfix/#23-monster-chase-behavior
refactor/#45-combat-system-cleanup
feature/#8-loot-system
```

## Architecture

### Core Game Loop (game.py:165-174)
The game follows a standard game loop pattern:
1. **Event Handling** - Process input and window events
2. **Update** - Update game state based on delta time
3. **Draw** - Render all game objects and UI
4. **Clock Tick** - Maintain 60 FPS (config.FPS)

### Game States (config.py:35-39)
The game uses a state machine with four states:
- `STATE_PLAYING` - Active gameplay
- `STATE_INVENTORY` - Inventory screen overlay
- `STATE_VICTORY` - Player wins
- `STATE_GAME_OVER` - Player loses

State transitions occur in game.py:100-104 (death detection) and game.py:60-65 (inventory toggle).

### Entity System
All game characters inherit from the base `Entity` class (entity.py):

**Base Entity** provides:
- Position, size, and color
- Health management with health bars
- Movement with screen bounds clamping (entity.py:84-86)
- Attack/damage system with cooldowns
- Collision detection via pygame.Rect
- Distance calculations between entities

**Warrior** (warrior.py) - Player character:
- Keyboard input handling (WASD/Arrow keys)
- Inventory system integration
- Attack damage boosted by equipped weapon (warrior.py:27-29)
- Movement speed normalized for diagonal movement (warrior.py:64-67)

**Monster** (monster.py) - AI enemy:
- Chase behavior when player within MONSTER_CHASE_RANGE (300 pixels)
- Attack when within MONSTER_ATTACK_RANGE (60 pixels)
- Simple pursuit AI: moves directly toward player (monster.py:24-58)

### Combat System (combat.py)
Combat is handled through a static CombatSystem class:
- Player attacks with SPACE key when in range
- Visual attack range indicator (yellow line) drawn when entities are close
- Cooldown system prevents attack spam (config.py:25, 31)
- Monster auto-attacks when in range using same cooldown logic

### Inventory System
**Structure** (inventory.py:8-11):
- 1 weapon slot (WEAPON items)
- 1 armor slot (ARMOR items)
- 3 backpack slots (any item type)

**Key Mechanics**:
- Items auto-equip to appropriate slots when added if slot is empty
- Equipping from backpack swaps with currently equipped item (inventory.py:67-78)
- Equipped items provide cumulative bonuses (attack, defense, health)
- Only weapon attack bonuses currently affect damage (warrior.py:41)

**Item Types** (item.py:5-10):
- WEAPON - Provides attack_bonus
- ARMOR - Provides defense_bonus and health_bonus
- CONSUMABLE - Health restoration (not yet implemented in gameplay)
- MISC - No stat bonuses

### UI Architecture
**InventoryUI** (inventory_ui.py) - Separate rendering system:
- Draws semi-transparent overlay over game (game.py:128-129)
- Slot-based grid layout for visual organization
- Mouse interaction for equipping/managing items
- Press 'I' to toggle (game.py:60-65)

**CombatUI** (combat.py:37-67):
- HP display for both entities
- Control hints in top-right
- Always visible during gameplay

## Configuration System
All game constants are centralized in config.py:
- Screen dimensions and FPS
- Color definitions (RGB tuples)
- Entity stats (health, damage, speed, cooldowns)
- AI behavior ranges (chase and attack distances)
- Game state constants

To adjust game difficulty, modify monster stats or attack ranges in config.py.

## Key Design Patterns

**Composition Over Inheritance**: Warrior uses an Inventory instance rather than inheriting inventory behavior.

**Delta Time Updates**: Movement and updates use dt (seconds) for frame-rate independent physics (game.py:168).

**Cooldown System**: Time-based cooldowns prevent attack spam using pygame.time.get_ticks() (entity.py:54-56).

**Visual Feedback**: Health bars auto-render above entities, attack range shown with yellow line connector.

## Development Notes

- The game initializes with sample items in warrior inventory (game.py:33-47)
- Monster AI is intentionally simple (direct pursuit) - suitable for single enemy encounters
- Defense and health bonuses from armor are calculated but not yet applied to damage reduction or max health
- Screen bounds clamping happens in Entity.move() to prevent entities from leaving the playable area
