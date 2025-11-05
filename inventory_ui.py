import pygame
from inventory import Inventory
from item import ItemType
import config


class InventoryUI:
    """UI overlay for displaying and managing inventory"""

    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 20)

        # UI positioning
        self.panel_width = 500
        self.panel_height = 400
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

        self.selected_slot = None  # (slot_type, index)

    def draw(self, screen: pygame.Surface, inventory: Inventory):
        """Draw the inventory overlay"""
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Center the panel
        panel_x = (screen_width - self.panel_width) // 2
        panel_y = (screen_height - self.panel_height) // 2

        # Draw semi-transparent background
        overlay = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        overlay.fill(self.bg_color)
        screen.blit(overlay, (panel_x, panel_y))

        # Draw border
        pygame.draw.rect(screen, self.slot_border_color,
                        (panel_x, panel_y, self.panel_width, self.panel_height), 2)

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

    def _draw_equipment_section(self, screen: pygame.Surface, inventory: Inventory,
                                panel_x: int, start_y: int):
        """Draw weapon and armor equipment slots"""
        # Weapon slot
        weapon_x = panel_x + self.padding
        weapon_y = start_y

        is_selected = self.selected_slot == ('weapon', 0)
        self._draw_slot(screen, weapon_x, weapon_y, "WEAPON", inventory.weapon_slot,
                       is_equipped=True, is_selected=is_selected)

        # Armor slot
        armor_x = weapon_x + self.slot_size + self.slot_margin * 3
        armor_y = start_y

        is_selected = self.selected_slot == ('armor', 0)
        self._draw_slot(screen, armor_x, armor_y, "ARMOR", inventory.armor_slot,
                       is_equipped=True, is_selected=is_selected)

    def _draw_backpack_section(self, screen: pygame.Surface, inventory: Inventory,
                              panel_x: int, start_y: int):
        """Draw backpack slots"""
        # Backpack label
        label = self.font.render("BACKPACK", True, self.text_color)
        screen.blit(label, (panel_x + self.padding, start_y - 25))

        # Draw 3 backpack slots
        for i in range(3):
            slot_x = panel_x + self.padding + i * (self.slot_size + self.slot_margin)
            slot_y = start_y

            is_selected = self.selected_slot == ('backpack', i)
            self._draw_slot(screen, slot_x, slot_y, f"SLOT {i+1}",
                           inventory.backpack_slots[i], is_selected=is_selected)

    def _draw_slot(self, screen: pygame.Surface, x: int, y: int, label: str,
                   item, is_equipped: bool = False, is_selected: bool = False):
        """Draw a single inventory slot"""
        # Determine slot color
        if is_equipped:
            slot_bg = self.equipped_slot_color
        else:
            slot_bg = self.slot_color

        # Draw slot background
        pygame.draw.rect(screen, slot_bg, (x, y, self.slot_size, self.slot_size))

        # Draw border (highlighted if selected)
        border_color = self.selected_color if is_selected else self.slot_border_color
        border_width = 3 if is_selected else 2
        pygame.draw.rect(screen, border_color, (x, y, self.slot_size, self.slot_size),
                        border_width)

        # Draw label
        label_text = self.small_font.render(label, True, self.text_color)
        label_x = x + (self.slot_size - label_text.get_width()) // 2
        screen.blit(label_text, (label_x, y + 5))

        # Draw item if present
        if item:
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
            stat_text = self.small_font.render(f"+{item.attack_bonus} ATK", True, (255, 100, 100))
            stat_x = x + (self.slot_size - stat_text.get_width()) // 2
            screen.blit(stat_text, (stat_x, stats_y))

        if item.defense_bonus > 0:
            stat_text = self.small_font.render(f"+{item.defense_bonus} DEF", True, (100, 100, 255))
            stat_x = x + (self.slot_size - stat_text.get_width()) // 2
            screen.blit(stat_text, (stat_x, stats_y))

    def _draw_instructions(self, screen: pygame.Surface, panel_x: int, panel_y: int):
        """Draw control instructions"""
        instructions = [
            "I - Close Inventory",
            "1-5 - Select Slot",
            "E - Equip from Backpack",
            "X - Drop Item"
        ]

        y_offset = self.panel_height - 80
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, (200, 200, 200))
            screen.blit(text, (panel_x + self.padding, panel_y + y_offset + i * 18))

    def handle_input(self, event: pygame.event.Event, inventory: Inventory, game=None) -> bool:
        """
        Handle input events for inventory management.

        Args:
            event: The pygame event to handle
            inventory: The inventory to manage
            game: The game instance (needed for dropping items)

        Returns:
            True if the event was handled.
        """
        if event.type != pygame.KEYDOWN:
            return False

        # Select slots with number keys
        if event.key == pygame.K_1:
            self.selected_slot = ('weapon', 0)
            return True
        elif event.key == pygame.K_2:
            self.selected_slot = ('armor', 0)
            return True
        elif event.key == pygame.K_3:
            self.selected_slot = ('backpack', 0)
            return True
        elif event.key == pygame.K_4:
            self.selected_slot = ('backpack', 1)
            return True
        elif event.key == pygame.K_5:
            self.selected_slot = ('backpack', 2)
            return True

        # Equip item from backpack
        elif event.key == pygame.K_e:
            if self.selected_slot and self.selected_slot[0] == 'backpack':
                inventory.equip_from_backpack(self.selected_slot[1])
                return True

        # Drop/remove item
        elif event.key == pygame.K_x:
            if self.selected_slot and game:
                slot_type, index = self.selected_slot
                item = inventory.remove_item_from_slot(slot_type, index)
                if item:
                    # Drop the item at the warrior's position
                    game.drop_item(item, game.warrior.grid_x, game.warrior.grid_y)
                    return True

        return False
