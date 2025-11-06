import pygame
from inventory import Inventory
from typing import Tuple


class InventoryUI:
    """UI overlay for displaying and managing inventory"""

    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 20)
        self.tooltip_font = pygame.font.Font(None, 18)

        # UI positioning
        self.panel_width = 500
        self.panel_height = 500
        self.padding = 20
        self.slot_size = 80
        self.slot_margin = 10

        # Colors
        self.bg_color = (40, 40, 50, 230)  # Dark semi-transparent
        self.slot_color = (60, 60, 70)
        self.slot_border_color = (100, 100, 120)
        self.equipped_slot_color = (80, 60, 40)
        self.text_color = (255, 255, 255)
        self.selected_color = (255, 200, 0)
        self.hover_color = (150, 150, 170)
        self.full_color = (200, 50, 50)

        self.selected_slot = None  # (slot_type, index)
        self.hovered_slot = None  # (slot_type, index)

        # Drag and drop state
        self.dragging_item = None  # Item being dragged
        self.dragging_from = None  # (slot_type, index) where drag started
        self.drag_offset = (0, 0)  # Offset from mouse to item position

        # Context menu state
        self.context_menu_slot = None  # (slot_type, index) for context menu
        self.context_menu_pos = None  # (x, y) position

        # Slot rects for mouse detection (updated each frame)
        self.slot_rects = {}  # {(slot_type, index): pygame.Rect}

    def draw(self, screen: pygame.Surface, inventory: Inventory):
        """Draw the inventory overlay"""
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Clear slot rects for this frame
        self.slot_rects = {}

        # Update hovered slot based on mouse position
        mouse_pos = pygame.mouse.get_pos()
        self._update_hovered_slot(mouse_pos)

        # Center the panel
        panel_x = (screen_width - self.panel_width) // 2
        panel_y = (screen_height - self.panel_height) // 2

        # Draw semi-transparent background
        overlay = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        overlay.fill(self.bg_color)
        screen.blit(overlay, (panel_x, panel_y))

        # Draw border
        pygame.draw.rect(
            screen,
            self.slot_border_color,
            (panel_x, panel_y, self.panel_width, self.panel_height),
            2,
        )

        # Draw title
        title_text = self.title_font.render("INVENTORY", True, self.text_color)
        title_x = panel_x + (self.panel_width - title_text.get_width()) // 2
        screen.blit(title_text, (title_x, panel_y + 10))

        # Starting position for slots
        current_y = panel_y + 60

        # Draw equipment slots (weapon and armor)
        self._draw_equipment_section(screen, inventory, panel_x, current_y)

        # Draw backpack slots
        current_y += 140
        self._draw_backpack_section(screen, inventory, panel_x, current_y)

        # Draw instructions
        self._draw_instructions(screen, panel_x, panel_y)

        # Draw tooltip if hovering over an item
        if self.hovered_slot and not self.dragging_item:
            self._draw_tooltip(screen, inventory, mouse_pos)

        # Draw context menu if active
        if self.context_menu_slot and self.context_menu_pos:
            self._draw_context_menu(screen, inventory)

        # Draw dragged item (on top of everything)
        if self.dragging_item:
            self._draw_dragged_item(screen, mouse_pos)

    def _draw_equipment_section(
        self, screen: pygame.Surface, inventory: Inventory, panel_x: int, start_y: int
    ):
        """Draw weapon and armor equipment slots"""
        # Weapon slot
        weapon_x = panel_x + self.padding
        weapon_y = start_y

        is_selected = self.selected_slot == ("weapon", 0)
        is_hovered = self.hovered_slot == ("weapon", 0)
        self._draw_slot(
            screen,
            weapon_x,
            weapon_y,
            "WEAPON",
            inventory.weapon_slot,
            ("weapon", 0),
            is_equipped=True,
            is_selected=is_selected,
            is_hovered=is_hovered,
        )

        # Armor slot
        armor_x = weapon_x + self.slot_size + self.slot_margin * 3
        armor_y = start_y

        is_selected = self.selected_slot == ("armor", 0)
        is_hovered = self.hovered_slot == ("armor", 0)
        self._draw_slot(
            screen,
            armor_x,
            armor_y,
            "ARMOR",
            inventory.armor_slot,
            ("armor", 0),
            is_equipped=True,
            is_selected=is_selected,
            is_hovered=is_hovered,
        )

    def _draw_backpack_section(
        self, screen: pygame.Surface, inventory: Inventory, panel_x: int, start_y: int
    ):
        """Draw backpack slots"""
        # Backpack label
        label = self.font.render("BACKPACK", True, self.text_color)
        screen.blit(label, (panel_x + self.padding, start_y - 25))

        # Draw 5 backpack slots (first row: 3 slots, second row: 2 slots)
        for i in range(5):
            if i < 3:
                # First row
                slot_x = (
                    panel_x + self.padding + i * (self.slot_size + self.slot_margin)
                )
                slot_y = start_y
            else:
                # Second row (centered)
                slot_x = (
                    panel_x
                    + self.padding
                    + (i - 3) * (self.slot_size + self.slot_margin)
                    + (self.slot_size + self.slot_margin) // 2
                )
                slot_y = start_y + self.slot_size + self.slot_margin

            is_selected = self.selected_slot == ("backpack", i)
            is_hovered = self.hovered_slot == ("backpack", i)
            self._draw_slot(
                screen,
                slot_x,
                slot_y,
                f"SLOT {i + 1}",
                inventory.backpack_slots[i],
                ("backpack", i),
                is_selected=is_selected,
                is_hovered=is_hovered,
            )

    def _draw_slot(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        label: str,
        item,
        slot_id: Tuple[str, int],
        is_equipped: bool = False,
        is_selected: bool = False,
        is_hovered: bool = False,
    ):
        """Draw a single inventory slot"""
        # Store rect for mouse detection
        rect = pygame.Rect(x, y, self.slot_size, self.slot_size)
        self.slot_rects[slot_id] = rect

        # Determine slot color
        if is_equipped:
            slot_bg = self.equipped_slot_color
        else:
            slot_bg = self.slot_color

        # Draw slot background
        pygame.draw.rect(screen, slot_bg, rect)

        # Draw border (highlighted if selected or hovered)
        if is_selected:
            border_color = self.selected_color
            border_width = 3
        elif is_hovered:
            border_color = self.hover_color
            border_width = 3
        else:
            border_color = self.slot_border_color
            border_width = 2

        pygame.draw.rect(screen, border_color, rect, border_width)

        # Draw label
        label_text = self.small_font.render(label, True, self.text_color)
        label_x = x + (self.slot_size - label_text.get_width()) // 2
        screen.blit(label_text, (label_x, y + 5))

        # Draw item if present (and not being dragged from this slot)
        if item and self.dragging_from != slot_id:
            self._draw_item_in_slot(screen, x, y, item)

    def _draw_item_in_slot(self, screen: pygame.Surface, x: int, y: int, item):
        """Draw item information in a slot"""
        # Draw item name (abbreviated if too long)
        name = item.name
        if len(name) > 10:
            name = name[:8] + ".."

        name_text = self.small_font.render(name, True, self.text_color)
        name_x = x + (self.slot_size - name_text.get_width()) // 2
        screen.blit(name_text, (name_x, y + 30))

        # Draw stats
        stats_y = y + 50
        if item.attack_bonus > 0:
            stat_text = self.small_font.render(
                f"+{item.attack_bonus} ATK", True, (255, 100, 100)
            )
            stat_x = x + (self.slot_size - stat_text.get_width()) // 2
            screen.blit(stat_text, (stat_x, stats_y))

        if item.defense_bonus > 0:
            stat_text = self.small_font.render(
                f"+{item.defense_bonus} DEF", True, (100, 100, 255)
            )
            stat_x = x + (self.slot_size - stat_text.get_width()) // 2
            screen.blit(stat_text, (stat_x, stats_y))

    def _draw_instructions(self, screen: pygame.Surface, panel_x: int, panel_y: int):
        """Draw control instructions"""
        instructions = [
            "Left Click - Select/Move Item",
            "Drag & Drop - Move Items",
            "Right Click - Item Menu",
            "Hover - Show Details",
        ]

        y_offset = self.panel_height - 80
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, (200, 200, 200))
            screen.blit(text, (panel_x + self.padding, panel_y + y_offset + i * 18))

    def handle_input(self, event: pygame.event.Event, inventory: Inventory) -> bool:
        """
        Handle input events for inventory management.
        Returns True if the event was handled.
        """
        # Handle mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                return self._handle_left_click(event.pos, inventory)
            elif event.button == 3:  # Right click
                return self._handle_right_click(event.pos, inventory)

        # Handle mouse button up
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left release
                return self._handle_left_release(event.pos, inventory)

        # Keep keyboard support for accessibility
        elif event.type == pygame.KEYDOWN:
            # Select slots with number keys
            if event.key == pygame.K_1:
                self.selected_slot = ("weapon", 0)
                return True
            elif event.key == pygame.K_2:
                self.selected_slot = ("armor", 0)
                return True
            elif event.key == pygame.K_3:
                self.selected_slot = ("backpack", 0)
                return True
            elif event.key == pygame.K_4:
                self.selected_slot = ("backpack", 1)
                return True
            elif event.key == pygame.K_5:
                self.selected_slot = ("backpack", 2)
                return True
            elif event.key == pygame.K_6:
                self.selected_slot = ("backpack", 3)
                return True
            elif event.key == pygame.K_7:
                self.selected_slot = ("backpack", 4)
                return True

            # Equip item from backpack
            elif event.key == pygame.K_e:
                if self.selected_slot and self.selected_slot[0] == "backpack":
                    inventory.equip_from_backpack(self.selected_slot[1])
                    return True

            # Drop/remove item
            elif event.key == pygame.K_x:
                if self.selected_slot:
                    slot_type, index = self.selected_slot
                    inventory.remove_item_from_slot(slot_type, index)
                    return True

        return False

    def _update_hovered_slot(self, mouse_pos: Tuple[int, int]):
        """Update which slot is currently being hovered over"""
        self.hovered_slot = None
        for slot_id, rect in self.slot_rects.items():
            if rect.collidepoint(mouse_pos):
                self.hovered_slot = slot_id
                break

    def _handle_left_click(
        self, mouse_pos: Tuple[int, int], inventory: Inventory
    ) -> bool:
        """Handle left mouse button click"""
        # Close context menu if clicking outside it
        if self.context_menu_slot:
            if not self._is_pos_in_context_menu(mouse_pos):
                self.context_menu_slot = None
                self.context_menu_pos = None
                return True

        # Check if clicking on a slot
        clicked_slot = None
        for slot_id, rect in self.slot_rects.items():
            if rect.collidepoint(mouse_pos):
                clicked_slot = slot_id
                break

        if clicked_slot:
            # Get the item in this slot
            slot_type, slot_index = clicked_slot
            item = self._get_item_from_slot(inventory, slot_type, slot_index)

            if item:
                # Start dragging
                self.dragging_item = item
                self.dragging_from = clicked_slot
                # Calculate offset from mouse to slot center
                rect = self.slot_rects[clicked_slot]
                self.drag_offset = (
                    rect.centerx - mouse_pos[0],
                    rect.centery - mouse_pos[1],
                )
            else:
                # Select empty slot
                self.selected_slot = clicked_slot

            return True

        return False

    def _handle_left_release(
        self, mouse_pos: Tuple[int, int], inventory: Inventory
    ) -> bool:
        """Handle left mouse button release (end of drag or click)"""
        if self.dragging_item:
            # Find which slot we're over
            target_slot = None
            for slot_id, rect in self.slot_rects.items():
                if rect.collidepoint(mouse_pos):
                    target_slot = slot_id
                    break

            if target_slot and target_slot != self.dragging_from:
                # Try to move/swap items
                self._move_item(inventory, self.dragging_from, target_slot)

            # Clear drag state
            self.dragging_item = None
            self.dragging_from = None
            self.drag_offset = (0, 0)
            return True

        return False

    def _handle_right_click(
        self, mouse_pos: Tuple[int, int], inventory: Inventory
    ) -> bool:
        """Handle right mouse button click"""
        # Check if clicking on a slot with an item
        for slot_id, rect in self.slot_rects.items():
            if rect.collidepoint(mouse_pos):
                slot_type, slot_index = slot_id
                item = self._get_item_from_slot(inventory, slot_type, slot_index)
                if item:
                    # Open context menu
                    self.context_menu_slot = slot_id
                    self.context_menu_pos = mouse_pos
                    return True

        return False

    def _get_item_from_slot(
        self, inventory: Inventory, slot_type: str, slot_index: int
    ):
        """Get the item from a specific slot"""
        if slot_type == "weapon":
            return inventory.weapon_slot
        elif slot_type == "armor":
            return inventory.armor_slot
        elif slot_type == "backpack":
            return inventory.backpack_slots[slot_index]
        return None

    def _move_item(
        self,
        inventory: Inventory,
        from_slot: Tuple[str, int],
        to_slot: Tuple[str, int],
    ):
        """Move or swap items between slots"""
        from_type, from_index = from_slot
        to_type, to_index = to_slot

        # Get items
        from_item = inventory.remove_item_from_slot(from_type, from_index)
        to_item = inventory.remove_item_from_slot(to_type, to_index)

        if from_item is None:
            return  # Nothing to move

        # Try to place from_item in to_slot
        success = self._place_item_in_slot(inventory, from_item, to_type, to_index)

        # If successful and there was an item in to_slot, move it to from_slot
        if success and to_item:
            self._place_item_in_slot(inventory, to_item, from_type, from_index)
        elif not success:
            # Couldn't place item, put it back
            self._place_item_in_slot(inventory, from_item, from_type, from_index)
            if to_item:
                self._place_item_in_slot(inventory, to_item, to_type, to_index)

    def _place_item_in_slot(
        self, inventory: Inventory, item, slot_type: str, slot_index: int
    ) -> bool:
        """Place an item in a specific slot, returns True if successful"""
        if slot_type == "weapon":
            from item import ItemType

            if item.item_type == ItemType.WEAPON or inventory.weapon_slot is None:
                inventory.weapon_slot = item
                return True
        elif slot_type == "armor":
            from item import ItemType

            if item.item_type == ItemType.ARMOR or inventory.armor_slot is None:
                inventory.armor_slot = item
                return True
        elif slot_type == "backpack":
            inventory.backpack_slots[slot_index] = item
            return True
        return False

    def _draw_tooltip(
        self, screen: pygame.Surface, inventory: Inventory, mouse_pos: Tuple[int, int]
    ):
        """Draw tooltip showing item details"""
        if not self.hovered_slot:
            return

        slot_type, slot_index = self.hovered_slot
        item = self._get_item_from_slot(inventory, slot_type, slot_index)

        if not item:
            return

        # Tooltip content
        lines = [
            f"Name: {item.name}",
            f"Type: {item.item_type.value.capitalize()}",
        ]

        if item.description:
            lines.append(f"Description: {item.description}")

        if item.attack_bonus > 0:
            lines.append(f"Attack: +{item.attack_bonus}")
        if item.defense_bonus > 0:
            lines.append(f"Defense: +{item.defense_bonus}")
        if item.health_bonus > 0:
            lines.append(f"Health: +{item.health_bonus}")

        # Calculate tooltip size
        padding = 10
        line_height = 20
        max_width = max(self.tooltip_font.size(line)[0] for line in lines)
        tooltip_width = max_width + padding * 2
        tooltip_height = len(lines) * line_height + padding * 2

        # Position tooltip near mouse, but keep on screen
        tooltip_x = mouse_pos[0] + 15
        tooltip_y = mouse_pos[1] + 15

        screen_width = screen.get_width()
        screen_height = screen.get_height()

        if tooltip_x + tooltip_width > screen_width:
            tooltip_x = mouse_pos[0] - tooltip_width - 15
        if tooltip_y + tooltip_height > screen_height:
            tooltip_y = mouse_pos[1] - tooltip_height - 15

        # Draw tooltip background
        tooltip_surface = pygame.Surface(
            (tooltip_width, tooltip_height), pygame.SRCALPHA
        )
        tooltip_surface.fill((30, 30, 40, 240))
        pygame.draw.rect(
            tooltip_surface, (150, 150, 170), (0, 0, tooltip_width, tooltip_height), 2
        )
        screen.blit(tooltip_surface, (tooltip_x, tooltip_y))

        # Draw tooltip text
        for i, line in enumerate(lines):
            text = self.tooltip_font.render(line, True, self.text_color)
            screen.blit(
                text, (tooltip_x + padding, tooltip_y + padding + i * line_height)
            )

    def _draw_context_menu(self, screen: pygame.Surface, inventory: Inventory):
        """Draw right-click context menu"""
        if not self.context_menu_slot or not self.context_menu_pos:
            return

        slot_type, slot_index = self.context_menu_slot
        item = self._get_item_from_slot(inventory, slot_type, slot_index)

        if not item:
            self.context_menu_slot = None
            return

        # Menu options based on slot type
        options = []
        if slot_type == "backpack":
            from item import ItemType

            if item.item_type in [ItemType.WEAPON, ItemType.ARMOR]:
                options.append("Equip")
        options.append("Drop")
        options.append("Inspect")

        # Menu dimensions
        menu_width = 120
        menu_item_height = 30
        menu_height = len(options) * menu_item_height

        menu_x, menu_y = self.context_menu_pos

        # Keep menu on screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        if menu_x + menu_width > screen_width:
            menu_x = screen_width - menu_width
        if menu_y + menu_height > screen_height:
            menu_y = screen_height - menu_height

        # Draw menu background
        menu_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        menu_surface.fill((40, 40, 50, 250))
        pygame.draw.rect(
            menu_surface, (100, 100, 120), (0, 0, menu_width, menu_height), 2
        )
        screen.blit(menu_surface, (menu_x, menu_y))

        # Draw menu options
        mouse_pos = pygame.mouse.get_pos()
        for i, option in enumerate(options):
            option_y = menu_y + i * menu_item_height
            option_rect = pygame.Rect(menu_x, option_y, menu_width, menu_item_height)

            # Highlight if hovering
            if option_rect.collidepoint(mouse_pos):
                highlight = pygame.Surface(
                    (menu_width - 4, menu_item_height - 4), pygame.SRCALPHA
                )
                highlight.fill((80, 80, 100, 200))
                screen.blit(highlight, (menu_x + 2, option_y + 2))

                # Handle click
                if pygame.mouse.get_pressed()[0]:
                    self._execute_context_menu_action(option, inventory)
                    self.context_menu_slot = None
                    self.context_menu_pos = None

            # Draw text
            text = self.font.render(option, True, self.text_color)
            text_x = menu_x + (menu_width - text.get_width()) // 2
            text_y = option_y + (menu_item_height - text.get_height()) // 2
            screen.blit(text, (text_x, text_y))

    def _execute_context_menu_action(self, action: str, inventory: Inventory):
        """Execute the selected context menu action"""
        if not self.context_menu_slot:
            return

        slot_type, slot_index = self.context_menu_slot

        if action == "Equip":
            if slot_type == "backpack":
                inventory.equip_from_backpack(slot_index)
        elif action == "Drop":
            inventory.remove_item_from_slot(slot_type, slot_index)
        elif action == "Inspect":
            # Select the slot to show it's being inspected
            self.selected_slot = self.context_menu_slot

    def _draw_dragged_item(self, screen: pygame.Surface, mouse_pos: Tuple[int, int]):
        """Draw the item being dragged"""
        if not self.dragging_item:
            return

        # Calculate position with offset
        x = mouse_pos[0] + self.drag_offset[0] - self.slot_size // 2
        y = mouse_pos[1] + self.drag_offset[1] - self.slot_size // 2

        # Draw semi-transparent slot
        drag_surface = pygame.Surface((self.slot_size, self.slot_size), pygame.SRCALPHA)
        drag_surface.fill((60, 60, 70, 200))
        pygame.draw.rect(
            drag_surface,
            self.selected_color,
            (0, 0, self.slot_size, self.slot_size),
            3,
        )
        screen.blit(drag_surface, (x, y))

        # Draw item info
        self._draw_item_in_slot(screen, x, y, self.dragging_item)

    def _is_pos_in_context_menu(self, pos: Tuple[int, int]) -> bool:
        """Check if a position is inside the context menu"""
        if not self.context_menu_pos:
            return False

        menu_width = 120
        menu_item_height = 30

        # Count menu items
        if self.context_menu_slot:
            slot_type, _ = self.context_menu_slot
            num_options = 3 if slot_type == "backpack" else 2
            menu_height = num_options * menu_item_height

            menu_x, menu_y = self.context_menu_pos
            menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
            return menu_rect.collidepoint(pos)

        return False
