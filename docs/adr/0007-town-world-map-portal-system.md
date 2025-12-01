# ADR 0007: Town-World Map Portal System

## Status

Accepted

## Context

The game needed a way for players to navigate between the town and the world map, and a mechanism to discover and collect town portal items. Previously, the town was only accessible via town portal consumable items, which required players to already have portals to reach the town. This created a circular dependency where players needed to be in town to buy portals, but needed portals to reach town.

Key requirements:
- Players should be able to enter town from the world map without using portal items
- Town should have a visible exit to return to the world map
- A library building should provide free portals to players who have none
- Portal items should only be usable once obtained (not available by default)
- Visual feedback when receiving portals from the library

## Decision

We implemented a bidirectional town-world map transition system with the following components:

### 1. Map Markers

- **Town Entrance** (`E`): Added to overworld.json at position (8, 5) as a gold-colored passable tile
- **Town Exit** (`<`): Added to town.json at position (6, 6) using existing exit marker
- **Library Building** (`L`): Added to town.json at position (2, 6) as a brown-colored passable tile

### 2. DungeonManager Extensions

Extended the existing DungeonManager to handle town as a special case:
- `town_entrance: Optional[Tuple[int, int]]`: Stores town entrance location from world map
- `_load_town_entrance()`: Scans world map for 'E' tiles
- `check_for_town_entrance(x, y)`: Checks if player is on town entrance
- `check_for_town_exit(x, y)`: Checks if player is on town exit marker
- `enter_town(x, y)`: Transitions player to town, saves return location
- `exit_town()`: Returns player to world map with +1 tile offset

### 3. DungeonTransitionManager Extensions

Added transition handlers for town:
- `_handle_town_entry()`: Spawns player at town spawn point, clears monsters/chests
- `_handle_town_exit()`: Respawns world monsters/chests, returns player to entrance

### 4. Library Building

Created Library class (similar to Temple):
- Visual design: Brown wooden building with book-themed decorations
- `activate_portal_gift()`: Triggers purple pulsing glow effect (1.5s duration)
- Positioned at grid (2, 6) in town

### 5. Library Interaction Logic

Added `_visit_library()` method in GameStateCoordinator:
- Checks if player has 0 town portals (only gives portals to players without any)
- Verifies inventory space availability
- Gives up to 3 town portals (limited by available slots)
- Activates visual effect and shows toast notification
- Uses existing `create_town_portal()` function from loot_table.py

### 6. Entry Point Logic

Town portals (return portals) are NOT created when:
- Entering town via world map entrance marker
- Starting the game

Town portals ARE created when:
- Using a town portal consumable item from inventory

This distinction is handled automatically by the existing portal system in GameStateManager, which only creates portals when `use_town_portal()` is called.

## Consequences

### Positive

- **Solves Bootstrap Problem**: Players can now reach town without having portals first
- **Intuitive Navigation**: Physical entrance/exit markers are clearer than abstract item usage
- **Resource Management**: Library provides limited portal supply, encouraging strategic use
- **Consistent Architecture**: Reuses existing dungeon transition system and portal mechanics
- **Visual Feedback**: Purple glow effect and toast messages inform players of portal acquisition
- **Discoverable**: Players naturally find the town entrance while exploring the world map

### Negative

- **Map Modifications Required**: Both overworld.json and town.json needed updates
- **Additional Complexity**: New tile markers and transition logic add to codebase
- **Testing Surface**: More code paths to test (town entry/exit, library interaction, portal conditions)

### Neutral

- **Town as Dungeon**: Treating town as a dungeon map (using DungeonManager) is conceptually odd but pragmatic
- **Single Town Entrance**: Only one entrance on world map (could be extended to multiple in future)
- **Library-Specific Logic**: Portal distribution is hardcoded to library building (could be generalized)

## Implementation Notes

- Library gives 3 portals when player has 0, respecting inventory space
- Town entrance placed near world spawn (8, 5) for easy discovery
- Exit marker placed in town for intuitive navigation back to world
- Purple glow effect distinguishes library from temple (green) and shop (yellow)
- All transitions use existing camera update and entity respawn patterns

## Alternatives Considered

1. **Starting Inventory**: Give players 3 portals at game start
   - Rejected: Less discoverable, doesn't teach the portal mechanic

2. **Free Portal Usage**: Make town always accessible via menu
   - Rejected: Removes resource management aspect, less immersive

3. **Multiple Town Entrances**: Place entrances at multiple world locations
   - Deferred: Can be added later if needed, YAGNI principle

4. **Quest-Based Portal Unlock**: Require completing a quest to unlock library
   - Rejected: Adds complexity without clear benefit for this feature

## Related ADRs

- ADR-0003: Game State Management - Uses existing FSM and transition patterns
- ADR-0001: Entity System Design - Library follows same pattern as Temple
- ADR-0002: Inventory System Architecture - Integrates with existing inventory slots
