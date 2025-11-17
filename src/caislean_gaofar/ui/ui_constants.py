"""UI constants for layout values and visual styling.

This module consolidates all UI-related magic numbers and layout constants
from the renderer classes, documenting their rationale and usage.
"""


class UIConstants:
    """Constants for UI layout, spacing, and visual styling."""

    # ===== HUD Panel Constants =====
    # Reasoning: These define the layout structure of the HUD panels on the right side
    HUD_PANEL_PADDING = 10  # Space between HUD edge and panels
    HUD_PANEL_MARGIN = 20  # Inner margin within panels
    HUD_PANEL_WIDTH_OFFSET = 20  # Offset from HUD width for panel sizing

    # Health Panel
    HEALTH_PANEL_HEIGHT = 80
    HEALTH_PANEL_Y = 10
    HEALTH_BAR_HEIGHT = 24
    HEALTH_BAR_Y_OFFSET = 38  # Position within panel
    HEALTH_BAR_MARGIN = 40  # Margins within bar area

    # Potion Panel
    POTION_PANEL_HEIGHT = 70
    POTION_PANEL_Y = 100
    POTION_ICON_SIZE = 40
    POTION_ICON_OFFSET = 15

    # Portal Panel
    PORTAL_PANEL_HEIGHT = 70
    PORTAL_PANEL_Y = 180
    PORTAL_ICON_SIZE = 40
    PORTAL_ICON_OFFSET = 15

    # Currency Panel
    CURRENCY_PANEL_HEIGHT = 60
    CURRENCY_PANEL_Y = 260
    CURRENCY_COIN_RADIUS = 15

    # Attack Panel
    ATTACK_PANEL_HEIGHT = 60
    ATTACK_PANEL_Y = 330

    # Defense Panel
    DEFENSE_PANEL_HEIGHT = 60
    DEFENSE_PANEL_Y = 400

    # XP Panel
    XP_PANEL_HEIGHT = 60
    XP_PANEL_Y = 390
    XP_BAR_HEIGHT = 18
    XP_BAR_Y_OFFSET = 30

    # Inventory Panel
    INVENTORY_PANEL_HEIGHT = 60
    INVENTORY_PANEL_Y = 470

    # Skills Panel
    SKILLS_PANEL_HEIGHT = 60
    SKILLS_PANEL_Y = 530

    # ===== Shop Panel Constants =====
    # Reasoning: These define the shop UI layout and sizing
    SHOP_PANEL_WIDTH = 700
    SHOP_PANEL_HEIGHT = 550
    SHOP_PANEL_PADDING = 20
    SHOP_TAB_HEIGHT = 50
    SHOP_ITEM_HEIGHT = 65
    SHOP_LIST_HEIGHT = 310
    SHOP_ITEM_PADDING = 8
    SHOP_BUTTON_WIDTH = 200
    SHOP_BUTTON_HEIGHT = 40

    # Shop Scrollbar
    SHOP_SCROLLBAR_WIDTH = 12
    SHOP_SCROLLBAR_MARGIN = 5
    SHOP_SCROLLBAR_MIN_THUMB = 30

    # Shop Dialog
    SHOP_DIALOG_WIDTH = 400
    SHOP_DIALOG_HEIGHT = 150
    SHOP_DIALOG_BUTTON_WIDTH = 100
    SHOP_DIALOG_BUTTON_HEIGHT = 35
    SHOP_DIALOG_BUTTON_SPACING = 10
    SHOP_DIALOG_BUTTON_MARGIN = 20

    # ===== Common UI Element Constants =====
    # Reasoning: Reusable values for common UI patterns

    # Borders and Decorations
    BORDER_WIDTH_THICK = 3
    BORDER_WIDTH_THIN = 2
    BORDER_WIDTH_MINIMAL = 1
    ORNATE_BORDER_OFFSET = 6  # Distance between outer and inner border
    ORNATE_CORNER_RADIUS = 3  # Radius of corner decorations

    # Text and Shadows
    TEXT_SHADOW_OFFSET = 2  # Offset for drop shadows
    TEXT_SHADOW_OFFSET_SMALL = 1  # Smaller shadow offset
    TEXT_PADDING = 10  # Padding around text in boxes

    # Font Sizes
    FONT_SIZE_LARGE = 74  # Game over screen
    FONT_SIZE_TITLE = 48  # Shop title
    FONT_SIZE_SUBTITLE = 36  # Gold count, stats
    FONT_SIZE_NORMAL = 32  # Warnings
    FONT_SIZE_MEDIUM = 28  # Health text
    FONT_SIZE_SMALL = 24  # Panel titles
    FONT_SIZE_TINY = 22  # XP panel level
    FONT_SIZE_INFO = 20  # Potion/portal titles
    FONT_SIZE_DETAIL = 18  # XP text, descriptions
    FONT_SIZE_HINT = 16  # Control hints

    # ===== World Renderer Constants =====
    # Reasoning: Constants for world object rendering

    # Dungeon Entrance Icons
    ENTRANCE_ICON_CIRCLE_OFFSET = 2  # Background circle offset
    ENTRANCE_ICON_NAME_OFFSET = 25  # Y offset for dungeon name text
    ENTRANCE_ICON_TEXT_BG_PADDING = 3  # Padding for text background

    # Cave Entrance
    CAVE_ARCH_X_FRACTION = 1 / 6  # X position as fraction of tile size
    CAVE_ARCH_Y_FRACTION = 1 / 3  # Y position as fraction of tile size
    CAVE_ARCH_WIDTH_FRACTION = 2 / 3  # Width as fraction of tile size
    CAVE_ARCH_HEIGHT_FRACTION = 2 / 3  # Height as fraction of tile size
    CAVE_INNER_X_FRACTION = 1 / 4  # Inner cave X position
    CAVE_INNER_Y_FRACTION = 1 / 2  # Inner cave Y position
    CAVE_INNER_WIDTH_FRACTION = 1 / 2  # Inner cave width
    CAVE_INNER_HEIGHT_FRACTION = 1 / 3  # Inner cave height
    CAVE_ROCK_RADIUS_FRACTION = 1 / 7  # Rock decoration radius

    # Castle Entrance
    CASTLE_GATE_X_FRACTION = 1 / 6
    CASTLE_GATE_Y_FRACTION = 1 / 4
    CASTLE_GATE_WIDTH_FRACTION = 2 / 3
    CASTLE_GATE_HEIGHT_FRACTION = 3 / 4
    CASTLE_OPENING_X_FRACTION = 1 / 3
    CASTLE_OPENING_Y_FRACTION = 1 / 2
    CASTLE_OPENING_WIDTH_FRACTION = 1 / 3
    CASTLE_OPENING_HEIGHT_FRACTION = 1 / 2
    CASTLE_BATTLEMENT_WIDTH_FRACTION = 1 / 6
    CASTLE_BATTLEMENT_Y_FRACTION = 1 / 8
    CASTLE_BATTLEMENT_HEIGHT_FRACTION = 1 / 8

    # Generic Dungeon Entrance
    DUNGEON_GLOW_RADIUS_FRACTION = 1 / 3
    DUNGEON_PORTAL_RADIUS_FRACTION = 1 / 4
    DUNGEON_CENTER_RADIUS_FRACTION = 1 / 6
    DUNGEON_GLOW_WIDTH = 2

    # Shop Building
    SHOP_BUILDING_ROOF_Y_FRACTION = 1 / 3  # Roof position
    SHOP_BUILDING_ROOF_TOP_FRACTION = 1 / 2  # Roof peak position
    SHOP_DOOR_WIDTH_FRACTION = 1 / 4
    SHOP_DOOR_HEIGHT_FRACTION = 1 / 3
    SHOP_WINDOW_SIZE_FRACTION = 1 / 6
    SHOP_WINDOW_LEFT_X_FRACTION = 1 / 6
    SHOP_WINDOW_RIGHT_X_FRACTION = 2 / 3
    SHOP_WINDOW_Y_FRACTION = 1 / 2
    SHOP_SIGN_SIZE_FRACTION = 1 / 5
    SHOP_SIGN_Y_FRACTION = 1 / 2
    SHOP_SIGN_BORDER_WIDTH = 2
    SHOP_INTERACTION_DISTANCE = 1  # Grid tiles
    SHOP_TEXT_Y_OFFSET = 20

    # Message Display
    MESSAGE_Y_OFFSET = 40  # From bottom of screen
    MESSAGE_BG_ALPHA = 200  # Background transparency

    # ===== Visual Effect Constants =====
    # Reasoning: Constants for animations and visual feedback

    # Critical Health Warning
    CRITICAL_HEALTH_ALPHA_BASE = 80  # Base alpha for pulsing effect
    CRITICAL_HEALTH_PULSE_DIVISOR = 200  # Timer divisor for pulse speed
    CRITICAL_HEALTH_VIGNETTE_WIDTH = 50  # Width of vignette edges
    CRITICAL_HEALTH_TEXT_Y = 30  # Y offset from bottom
    CRITICAL_HEALTH_BLINK_RATE = 500  # Milliseconds for text blink

    # Potion Glow Effect
    POTION_GLOW_ALPHA = 128  # Max alpha for glow
    POTION_GLOW_RADIUS_OFFSET = 10  # Additional radius for glow
    POTION_GLOW_OFFSET = 5  # Position offset for glow

    # Skill Badge
    SKILL_BADGE_RADIUS = 8
    SKILL_BADGE_X_OFFSET = 30
    SKILL_BADGE_Y_OFFSET = 5

    # ===== Color Constants =====
    # Reasoning: UI-specific colors not in main config

    # HUD Colors (Medieval/Fantasy Theme)
    WOOD_COLOR = (101, 67, 33)  # Dark brown wood
    WOOD_BORDER = (65, 43, 21)  # Darker wood border
    ORNATE_GOLD = (218, 165, 32)  # Ornate golden color
    HEALTH_GREEN = (76, 187, 23)  # Vibrant health green
    HEALTH_YELLOW = (220, 220, 50)  # Warning health yellow
    HEALTH_RED = (220, 50, 50)  # Low health red
    HEALTH_CRITICAL = (139, 0, 0)  # Critical health dark red
    TEXT_COLOR = (255, 248, 220)  # Cornsilk for readable text

    # Shop Colors
    SHOP_LIST_BG_COLOR = (30, 30, 40)
    SHOP_ITEM_BG_COLOR = (50, 50, 70)
    SHOP_ITEM_HOVER_COLOR = (70, 70, 110)
    SHOP_ITEM_DESC_COLOR = (200, 200, 200)
    SHOP_STAT_COLOR = (150, 200, 150)
    SHOP_QUANTITY_COLOR = (150, 200, 255)
    SHOP_BUTTON_DISABLED_BG = (50, 50, 50)
    SHOP_BUTTON_DISABLED_TEXT = (100, 100, 100)
    SHOP_SCROLLBAR_TRACK_COLOR = (40, 40, 50)
    SHOP_SCROLLBAR_THUMB_COLOR = (100, 100, 120)
    SHOP_DIALOG_BG_COLOR = (40, 40, 60)
    SHOP_DIALOG_BG_ALPHA = 250
    SHOP_NO_BUTTON_COLOR = (100, 30, 30)
    SHOP_NO_BUTTON_HOVER = (150, 50, 50)
    SHOP_INSTRUCTION_COLOR = (180, 180, 180)
    SHOP_SCROLL_HINT_COLOR = (150, 150, 150)

    # Potion Colors
    POTION_RED = (200, 50, 50)
    POTION_HIGHLIGHT = (255, 100, 100)
    POTION_CORK = (139, 69, 19)
    POTION_GLOW_COLOR = (100, 255, 100)

    # Portal Colors
    PORTAL_OUTER = (138, 43, 226)
    PORTAL_MIDDLE = (186, 85, 211)
    PORTAL_INNER = (255, 255, 255)

    # Building Colors
    BUILDING_COLOR = (139, 90, 43)  # Brown
    ROOF_COLOR = (160, 82, 45)  # Saddle brown
    DOOR_COLOR = (101, 67, 33)  # Dark brown
    WINDOW_COLOR = (135, 206, 235)  # Sky blue

    # Dungeon Entrance Colors
    CAVE_COLOR = (60, 40, 20)  # Very dark brown
    CAVE_INNER_COLOR = (20, 15, 10)  # Nearly black
    CAVE_ROCK_COLOR = (120, 100, 70)  # Lighter brown
    CAVE_BG_COLOR = (200, 180, 140)  # Light tan background
    CAVE_BG_DARK = (30, 30, 30)

    CASTLE_STONE_COLOR = (140, 130, 120)  # Light stone grey
    CASTLE_DARK_STONE = (60, 55, 50)  # Dark stone
    CASTLE_BG_COLOR = (180, 180, 180)  # Light grey background
    CASTLE_BG_DARK = (30, 30, 30)

    DUNGEON_COLOR = (180, 120, 240)  # Bright purple
    DUNGEON_GLOW_COLOR = (220, 180, 255)  # Light purple glow
    DUNGEON_CENTER_COLOR = (30, 10, 50)  # Dark center
    DUNGEON_BG_COLOR = (220, 220, 250)  # Very light purple
    DUNGEON_BG_DARK = (30, 30, 30)

    # Icon Colors
    SWORD_COLOR = (192, 192, 192)  # Silver
    SWORD_HANDLE_COLOR = (139, 69, 19)  # Brown
    SHIELD_COLOR = (128, 128, 128)  # Grey
    SHIELD_BORDER_COLOR = (64, 64, 64)  # Dark grey
    GOLD_COIN_COLOR = (218, 165, 32)  # Gold
    GOLD_COIN_DARK = (184, 134, 11)  # Darker gold
    BAG_COLOR = (101, 67, 33)  # Brown
    BAG_BORDER = (65, 43, 21)  # Dark brown
    BAG_FLAP_COLOR = (139, 90, 43)  # Lighter brown
    BOOK_COLOR = (139, 69, 19)  # Brown
    BOOK_BORDER = (101, 50, 0)  # Darker brown
    BOOK_PAGES_COLOR = (255, 248, 220)  # Cream

    # Health Thresholds (for color changes)
    HEALTH_THRESHOLD_HIGH = 0.5  # Above this: green
    HEALTH_THRESHOLD_MED = 0.25  # Above this: yellow, below: red
