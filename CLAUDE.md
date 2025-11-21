# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyGame-based action RPG inspired by "Castle of the Winds". Features real-time combat, inventory system, and equipment
management. Run with `python main.py`. Uses `uv` for dependency management (Python 3.13+).

## Quality Requirements

**IMPORTANT**: All features must meet these standards before merging:

- **100% branch coverage** - Every code path must be tested
- **All tests must pass** - Run test suite before committing
- **Pre-commit hooks must pass** - Ensure linting and formatting standards

## Git Branching Conventions

Use format: `<prefix>/#<ticket-id>-<description>`

**Prefixes**: `feature/`, `bugfix/`, `refactor/`

**Examples**: `feature/#12-mouse-driven-inventory`, `bugfix/#23-monster-chase-behavior`

## Architecture

### Game Loop & States

Standard loop: Event Handling → Update (delta time) → Draw → Clock Tick (60 FPS). Three states: `STATE_PLAYING`,
`STATE_INVENTORY`, `STATE_GAME_OVER`.

### Entity System

**Base Entity** (entity.py): Position, health bars, movement with screen bounds clamping, attack/damage with cooldowns,
collision detection.

**Warrior** (warrior.py): WASD/Arrow keys input, inventory integration, weapon attack bonuses, normalized diagonal
movement.

**Monster** (monster.py): Chase within 300px range, attack within 60px range, simple pursuit AI.

### Combat System (combat.py)

SPACE key attacks, visual range indicators, cooldown-based attack spam prevention, monster auto-attacks in range.

### Inventory System (inventory.py)

**Structure**: 1 weapon slot, 1 armor slot, 3 backpack slots.
**Mechanics**: Auto-equip to empty slots, swap when equipping from backpack, cumulative bonuses (attack, defense,
health).
**Item Types**: WEAPON (attack_bonus), ARMOR (defense_bonus, health_bonus), CONSUMABLE (health restore - not
implemented), MISC (no bonuses).

### UI

**InventoryUI** (inventory_ui.py): Semi-transparent overlay, mouse interaction, toggle with 'I' key.
**CombatUI** (combat.py:37-67): HP display, control hints.

### Configuration (config.py)

Centralized constants: screen size, FPS, colors, entity stats, AI ranges, game states.

## Design Patterns

- **Composition**: Warrior contains Inventory instance
- **Delta Time**: Frame-rate independent physics
- **Cooldowns**: Time-based using pygame.time.get_ticks()

## Architecture Decision Records (ADR)

**IMPORTANT**: When making significant architectural or design decisions, you MUST create an ADR.

### When to Create an ADR

Create an ADR when:
- Choosing between different architectural patterns
- Selecting a new library or framework
- Changing core system designs (entity system, state management, etc.)
- Making decisions that affect future development
- Establishing new conventions or patterns

Do NOT create ADRs for:
- Minor bug fixes
- Simple feature additions using existing patterns
- Refactoring without changing architecture
- Configuration changes

### ADR Process

1. **Check existing ADRs**: Read `docs/adr/README.md` to understand existing decisions
2. **Create new ADR**: Use next sequential number (e.g., `0006-my-decision.md`)
3. **Follow template**:
   ```markdown
   # ADR NNNN: Title

   ## Status
   Accepted | Proposed | Deprecated | Superseded

   ## Context
   What is the issue we're facing?

   ## Decision
   What did we decide to do and why?

   ## Consequences
   What are the positive, negative, and neutral outcomes?
   ```
4. **Update README**: Add entry to `docs/adr/README.md` index
5. **Commit with ADR**: Include ADR in the same commit as the implementation

### Example ADRs

See existing ADRs for examples:
- [ADR 0001: Entity System Design](docs/adr/0001-entity-system-design.md)
- [ADR 0002: Inventory System Architecture](docs/adr/0002-inventory-system-architecture.md)
- [ADR 0003: Game State Management](docs/adr/0003-game-state-management.md)
- [ADR 0004: UI Architecture Pattern](docs/adr/0004-ui-architecture-pattern.md)
- [ADR 0005: UV for Dependency Management](docs/adr/0005-uv-dependency-management.md)
