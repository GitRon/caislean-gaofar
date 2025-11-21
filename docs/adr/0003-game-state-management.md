# ADR 0003: Game State Management

## Status

Accepted

## Context

The game requires different modes of operation: normal gameplay, inventory management, shop interaction, skills menu, and game over screen. Each mode has different input handling, rendering, and update logic.

Key requirements:
- Clear separation between game modes
- Safe state transitions
- Prevent invalid operations in wrong states
- Support for pause-like states (inventory, shop)
- Portal/teleportation system state
- Message display system

## Decision

We will use a **Finite State Machine (FSM)** pattern with centralized state management:

### State Enumeration
Defined in `core/config.py`:
```python
STATE_PLAYING = "playing"      # Normal gameplay
STATE_GAME_OVER = "game_over"  # Player death
STATE_INVENTORY = "inventory"  # Inventory UI overlay
STATE_SHOP = "shop"            # Shop interaction
STATE_SKILLS = "skills"        # Skills menu
```

Benefits:
- String-based for clarity and debugging
- Centralized in config for consistency
- Easy to add new states

### State Manager Class
`GameStateManager` (core/game_state_manager.py) centralizes state logic:

**Responsibilities**:
- Track current state
- Manage state transitions with validation
- Handle temporary message display
- Manage portal system state
- Update timers and animations

**Key Methods**:
- `transition_to_inventory()`: Enter inventory from playing/shop
- `transition_from_inventory()`: Return to previous state
- `transition_to_shop(is_near_shop)`: Enter shop if valid
- `transition_to_game_over()`: Handle player death
- `show_message(msg)`: Temporary message display

### State Transition Rules
- **Playing → Inventory**: Allowed anytime
- **Shop → Inventory**: Allowed anytime
- **Inventory → Playing/Shop**: Returns to previous state
- **Playing → Shop**: Only when near shop
- **Any → Game Over**: Allowed (closes portals, resets state)
- **Game Over → Playing**: Requires game restart

Benefits:
- Prevents invalid state combinations
- Encapsulates business rules
- Centralized validation

### Message System
- Temporary messages shown over gameplay
- Timer-based auto-dismiss (3 seconds default)
- Non-blocking (game continues)
- Single message at a time (new replaces old)

### Portal State Management
Portal teleportation requires complex state:
- `active_portal`: Portal in dungeon/world
- `return_portal`: Portal in town
- `portal_return_location`: Saved position (map_id, x, y)
- `portal_cooldown`: Prevent instant re-teleportation

Benefits:
- Prevents portal bugs
- Ensures cleanup on game over
- Cooldown prevents accidental double-teleports

## Consequences

### Positive
- **Clear contracts**: Each state has defined entry/exit conditions
- **Centralized logic**: State transitions in one place
- **Testable**: State machine logic is isolated
- **Debuggable**: String states are easy to log and inspect
- **Maintainable**: Adding new states follows clear pattern
- **Safe**: Invalid transitions are prevented

### Negative
- **Indirection**: State logic is not colocated with feature code
- **Manager dependency**: Many systems need GameStateManager reference
- **State explosion risk**: Too many states increases complexity
- **Memory of previous state**: Inventory→previous requires tracking

### Neutral
- **Performance**: Negligible overhead from state checks
- **Coupling**: Moderate coupling between manager and game systems

## Implementation Details

### State Checking Pattern
```python
# In game loop
if state_manager.state == config.STATE_PLAYING:
    handle_playing_input()
    update_entities()
elif state_manager.state == config.STATE_INVENTORY:
    handle_inventory_input()
# etc.
```

### Message Display Pattern
```python
state_manager.show_message("Item picked up!")
# Message auto-dismisses after 3 seconds
```

### Portal State Pattern
```python
# Using town portal
success, message = state_manager.use_town_portal(warrior, dungeon_manager)
state_manager.show_message(message)

# Return portal collision
if state_manager.check_return_portal_collision(warrior):
    success, message = state_manager.use_return_portal(warrior, dungeon_manager)
```

## Alternatives Considered

### 1. State Pattern (OOP)
Create State classes with polymorphic behavior.

**Rejected because**:
- Overkill for simple state machine
- More boilerplate code
- String states sufficient for current complexity

### 2. Flags Instead of States
Use boolean flags (is_inventory_open, is_shop_open, etc.)

**Rejected because**:
- Allows invalid combinations (inventory + shop both open)
- No clear transition logic
- Harder to reason about all states

### 3. Global State Variable
Single global variable without manager class.

**Rejected because**:
- No transition validation
- Message/portal state would need separate globals
- Harder to test

## Related Decisions
- [ADR 0001: Entity System Design](0001-entity-system-design.md) - Turn processing coordination
- [ADR 0004: UI Architecture Pattern](0004-ui-architecture-pattern.md) - State-dependent rendering
