"""State management for inventory UI."""

from typing import Optional, Tuple
import pygame


class InventoryState:
    """Manages the state of the inventory UI."""

    def __init__(self):
        """Initialize inventory UI state."""
        # Selection state
        self.selected_slot: Optional[Tuple[str, int]] = None  # (slot_type, index)
        self.hovered_slot: Optional[Tuple[str, int]] = None  # (slot_type, index)

        # Drag and drop state
        self.dragging_item = None  # Item being dragged
        self.dragging_from: Optional[Tuple[str, int]] = None  # (slot_type, index)
        self.drag_offset: Tuple[int, int] = (0, 0)  # Offset from mouse to item

        # Context menu state
        self.context_menu_slot: Optional[Tuple[str, int]] = None  # (slot_type, index)
        self.context_menu_pos: Optional[Tuple[int, int]] = None  # (x, y) position

        # Slot rects for mouse detection (updated each frame)
        self.slot_rects: dict = {}  # {(slot_type, index): pygame.Rect}

    def clear_slot_rects(self):
        """Clear slot rectangles for a new frame."""
        self.slot_rects = {}

    def update_hovered_slot(self, mouse_pos: Tuple[int, int]):
        """Update which slot is currently being hovered over."""
        self.hovered_slot = None
        for slot_id, rect in self.slot_rects.items():
            if rect.collidepoint(mouse_pos):
                self.hovered_slot = slot_id
                break

    def start_drag(self, item, slot_id: Tuple[str, int], drag_offset: Tuple[int, int]):
        """Start dragging an item."""
        self.dragging_item = item
        self.dragging_from = slot_id
        self.drag_offset = drag_offset

    def end_drag(self):
        """End dragging."""
        self.dragging_item = None
        self.dragging_from = None
        self.drag_offset = (0, 0)

    def open_context_menu(self, slot_id: Tuple[str, int], pos: Tuple[int, int]):
        """Open context menu for a slot."""
        self.context_menu_slot = slot_id
        self.context_menu_pos = pos

    def close_context_menu(self):
        """Close the context menu."""
        self.context_menu_slot = None
        self.context_menu_pos = None

    def is_dragging(self) -> bool:
        """Check if currently dragging an item."""
        return self.dragging_item is not None

    def has_context_menu(self) -> bool:
        """Check if context menu is open."""
        return self.context_menu_slot is not None
