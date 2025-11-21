# ADR 0004: UI Architecture Pattern

## Status

Accepted

## Context

The game needs complex UI systems (inventory, shop, HUD, skills) that handle:
- State management (selected items, drag-and-drop, context menus)
- Rendering (drawing overlays, tooltips, sprites)
- Input handling (mouse clicks, keyboard shortcuts)

Early implementations suffered from "God Object" pattern where single UI classes had 500+ lines mixing all concerns, making them hard to test and maintain.

Key requirements:
- Testable UI logic
- Clear separation of concerns
- Reusable rendering components
- Maintainable codebase
- Support for complex interactions (drag-and-drop, context menus)

## Decision

We will use a **Model-View-Controller (MVC) inspired pattern** with three-component separation:

### Component Separation

#### 1. State Component (`*_state.py`)
**Responsibility**: Manage UI state (the Model)

**Contains**:
- Selected items/slots
- Drag-and-drop state
- Context menu state
- Hover state
- Slot position tracking

**Examples**:
- `InventoryState`: Tracks dragged item, selected slot, context menu
- `HudState`: Tracks panel dimensions, button states
- `ShopState`: Tracks selected shop items, transaction state

**Benefits**:
- Pure data structures (easy to test)
- State can be serialized/inspected
- Clear ownership of state variables

#### 2. Renderer Component (`*_renderer.py`)
**Responsibility**: Handle drawing (the View)

**Contains**:
- Drawing methods for UI elements
- Layout calculations
- Visual styling
- Tooltip rendering
- Context menu rendering

**No Business Logic**: Renderers don't modify state or handle input

**Examples**:
- `InventoryRenderer.draw(screen, inventory, state)`
- `HudRenderer.draw_panel(screen, state, panel_data)`
- `ShopRenderer.draw_item_list(screen, shop, state)`

**Benefits**:
- Visual logic isolated
- Easy to change styling
- Testable with mock surfaces

#### 3. Input Handler Component (`*_input_handler.py`)
**Responsibility**: Process user input (the Controller)

**Contains**:
- Event processing (mouse clicks, keyboard)
- State updates based on input
- Business logic (item swapping, purchases)
- Action execution

**Examples**:
- `InventoryInputHandler.handle_event(event, inventory)`
- `ShopInputHandler.handle_purchase(item, warrior)`

**Benefits**:
- Input logic centralized
- Business rules in one place
- Easy to test with mock events

### Coordinator Class Pattern

A lightweight coordinator class (`InventoryUI`, `HUD`, `ShopUI`) composes the three components:

```python
class InventoryUI:
    def __init__(self):
        self.state = InventoryState()
        self.renderer = InventoryRenderer()
        self.input_handler = InventoryInputHandler(self.state, self.renderer)

    def draw(self, screen, inventory):
        self.renderer.draw(screen, inventory, self.state)

    def handle_event(self, event, inventory):
        self.input_handler.handle_event(event, inventory, self.state)
```

**Benefits**:
- Simple public API
- Components can be tested in isolation
- Easy to replace components

### Backward Compatibility Layer

For gradual refactoring, coordinator classes provide delegation methods:

```python
def _draw_tooltip(self, screen, inventory):
    return self.renderer._draw_tooltip(screen, inventory, self.state)
```

This allows incremental migration of existing code.

## Consequences

### Positive
- **Testability**: Each component can be unit tested independently
- **Maintainability**: Small, focused files (~100-200 lines each)
- **Clarity**: Clear responsibility for each component
- **Reusability**: Renderer components can be shared
- **Parallel development**: Multiple developers can work on different components
- **Easier debugging**: State can be inspected separately from rendering

### Negative
- **Indirection**: More files and classes to navigate
- **Ceremony**: Simple UIs require more boilerplate
- **State passing**: State parameter passed to many methods
- **Learning curve**: Developers must understand pattern

### Neutral
- **File count**: Each UI system has 3-4 files instead of 1
- **Performance**: Negligible overhead from delegation
- **Coupling**: Components are loosely coupled via state objects

## Implementation Examples

### File Structure
```
ui/
  inventory_ui.py          # Coordinator
  inventory_state.py       # State management
  inventory_renderer.py    # Rendering
  inventory_input_handler.py # Input processing

  hud.py                   # Coordinator
  hud_state.py            # State management
  hud_renderer.py         # Rendering

  shop_ui.py              # Coordinator
  shop_state.py           # State management
  shop_renderer.py        # Rendering
  shop_input_handler.py   # Input processing
```

### Testing Pattern
```python
# Test state in isolation
def test_drag_start():
    state = InventoryState()
    item = Item("sword")
    state.start_drag(item, ("backpack", 0))
    assert state.dragged_item == item
    assert state.drag_source == ("backpack", 0)

# Test renderer with mock state
def test_draw_dragged_item():
    state = Mock(dragged_item=item, drag_source=...)
    renderer = InventoryRenderer()
    # Verify drawing calls
```

## Migration Strategy

1. **Create State class**: Extract state variables to `*_state.py`
2. **Create Renderer class**: Extract drawing methods to `*_renderer.py`
3. **Create Input Handler class**: Extract event handling to `*_input_handler.py`
4. **Update Coordinator**: Compose components, add delegation methods
5. **Gradual migration**: Update callers incrementally
6. **Remove delegation**: Once all callers updated, remove backward compatibility

## Alternatives Considered

### 1. Keep Monolithic UI Classes
**Rejected because**:
- Classes grew to 500+ lines
- Hard to test
- Mixed concerns
- Difficult to maintain

### 2. React-style Component Tree
**Rejected because**:
- Overkill for immediate-mode rendering
- PyGame doesn't support this pattern natively
- More complex than needed

### 3. Observer Pattern for State
**Rejected because**:
- Unnecessary complexity
- Polling state is sufficient at 60 FPS
- No performance benefit

## Related Decisions
- [ADR 0002: Inventory System Architecture](0002-inventory-system-architecture.md) - Inventory business logic
- [ADR 0003: Game State Management](0003-game-state-management.md) - Game-level state
