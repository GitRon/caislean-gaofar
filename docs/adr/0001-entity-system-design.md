# ADR 0001: Entity System Design

## Status

Accepted

## Context

The game requires a flexible system for managing game characters (player, monsters) with shared functionality like movement, combat, and health. The game is inspired by "Castle of the Winds" which uses a grid-based, turn-based approach.

Key requirements:
- Support for multiple entity types (warrior, various monsters)
- Grid-based positioning for tactical gameplay
- Turn-based combat system
- Visual health representation
- Collision detection for combat and movement
- Camera offset support for scrolling world

## Decision

We will use a **base Entity class** with the following architectural choices:

### Grid-Based Positioning
- Entities use grid coordinates (`grid_x`, `grid_y`) as the source of truth
- Pixel coordinates are computed properties derived from grid position
- Grid size defined by `config.TILE_SIZE`
- Benefits: Simpler collision detection, clear movement rules, easier pathfinding

### Turn-Based Combat
- Attack cooldown system based on turns, not real-time
- Entities track `turns_since_last_attack` counter
- `can_attack()` method enforces cooldown rules
- `on_turn_start()` called each turn to increment cooldowns
- Benefits: Predictable combat, easier to balance, strategic depth

### Inheritance Hierarchy
- Single base `Entity` class in `entities/entity.py`
- Specialized classes (`Warrior`, `BaseMonster`) inherit from Entity
- Common functionality (health, movement, combat) in base class
- Specific behavior (input handling, AI) in subclasses
- Benefits: Code reuse, consistent interface, easy to extend

### Camera-Relative Rendering
- Drawing methods accept `camera_offset_x` and `camera_offset_y` parameters
- Screen coordinates computed as: `(grid_x - camera_offset_x) * TILE_SIZE`
- Allows for scrolling world larger than screen size
- Benefits: Scalable world size, smooth camera following

### Health Bar Integration
- Health bars drawn automatically as part of entity rendering
- Visual feedback without separate UI overlay
- Positioned above entity sprite
- Benefits: Immediate visual feedback, reduces UI clutter

## Consequences

### Positive
- **Consistent behavior**: All entities share common movement/combat logic
- **Easy to extend**: New entity types can be added by subclassing
- **Grid-based simplicity**: Movement and collision detection are straightforward
- **Turn-based strategy**: Combat is predictable and strategic
- **Testable**: Clear interfaces make unit testing easier

### Negative
- **Grid constraints**: Limited to tile-based movement (no sub-tile positioning)
- **Turn synchronization**: Requires careful management of turn order
- **Inheritance coupling**: Changes to base Entity affect all subclasses
- **Limited flexibility**: Real-time combat features would require refactoring

### Neutral
- **Performance**: Grid-based approach is efficient for current game scale
- **Camera system**: Requires coordination between entities and rendering system

## Related Decisions
- [ADR 0003: Game State Management](0003-game-state-management.md) - Turn processing
- [ADR 0004: UI Architecture Pattern](0004-ui-architecture-pattern.md) - Rendering coordination
