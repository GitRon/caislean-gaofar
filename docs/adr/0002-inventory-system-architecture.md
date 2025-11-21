# ADR 0002: Inventory System Architecture

## Status

Accepted

## Context

The game needs an inventory system for managing player equipment and items. Inspired by "Castle of the Winds", which featured dedicated equipment slots and a backpack for storage.

Key requirements:
- Weapon and armor equipment slots
- Backpack storage for additional items
- Stat bonuses from equipped items
- Item swapping between slots
- Integration with combat system
- Support for future item types (consumables, misc items)

## Decision

We will use a **slot-based inventory system** with composition pattern:

### Slot Structure
- **Equipment Slots**: 1 weapon slot, 1 armor slot
- **Backpack Slots**: 13 general-purpose storage slots
- Each slot can hold one item or be empty (Optional[Item])
- Slots are typed only at the conceptual level (no type enforcement at runtime)

### Item Auto-Equip Logic
```python
def add_item(item):
    if item_type matches empty equipment slot:
        auto-equip to equipment slot
    else:
        add to first empty backpack slot
```

Benefits:
- Reduces clicks for common actions
- Intuitive for new players
- Respects player's existing equipment

### Item Swapping
- Equipping from backpack swaps with currently equipped item
- Swapped item returns to the backpack slot
- No items are lost during swaps
- Prevents inventory overflow errors

### Bonus Aggregation
- `get_total_attack_bonus()` sums bonuses from all equipped items
- `get_total_defense_bonus()` sums defense from all equipped items
- Both weapon and armor can provide any bonus type
- Bonuses applied in combat calculations

### Composition Over Inheritance
- `Warrior` class contains an `Inventory` instance
- Inventory is a separate system, not inherited
- Inventory has no knowledge of entities or combat
- Benefits: Clear separation of concerns, easier testing

### Item Type Enum
```python
class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"  # Not yet implemented
    MISC = "misc"
```

Benefits: Type safety, extensibility, clear categorization

## Consequences

### Positive
- **Simple mental model**: Fixed slots are easy to understand
- **No weight/volume complexity**: Just slot limits
- **Type safety**: ItemType enum prevents errors
- **Flexible bonuses**: Any item can provide any bonus
- **Testable**: Inventory logic is isolated from game logic
- **Extensible**: Easy to add new item types

### Negative
- **Limited backpack size**: 13 slots may feel restrictive
- **No stacking**: Each slot holds one item only
- **Consumables not implemented**: Placeholder for future feature
- **No sorting**: Items stay where placed

### Neutral
- **Performance**: Minimal overhead with small slot count
- **UI implications**: Slot-based UI is straightforward to implement

## Implementation Details

### File Structure
- `systems/inventory.py`: Core inventory logic
- `objects/item.py`: Item class and ItemType enum
- `ui/inventory_ui.py`: Visual representation and interaction

### Key Methods
- `add_item(item)`: Auto-equip or add to backpack
- `equip_from_backpack(index)`: Swap equipment
- `get_total_attack_bonus()`: Aggregate stat bonuses
- `has_space()`: Check for available slots

## Related Decisions
- [ADR 0001: Entity System Design](0001-entity-system-design.md) - Warrior-Inventory composition
- [ADR 0004: UI Architecture Pattern](0004-ui-architecture-pattern.md) - Inventory UI implementation
