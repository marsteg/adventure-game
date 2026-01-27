"""
Asset Generator - Creates placeholder game assets programmatically.
All assets are generated with transparent backgrounds.
"""

import pygame
import os
import math


def ensure_dir(path):
    """Ensure a directory exists."""
    os.makedirs(os.path.dirname(path), exist_ok=True)


def create_transparent_surface(width, height):
    """Create a transparent surface."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    return surface


def draw_rounded_rect(surface, color, rect, radius):
    """Draw a rounded rectangle."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def add_highlight(surface, rect, intensity=30):
    """Add a subtle highlight to the top of an object."""
    x, y, w, h = rect
    highlight = create_transparent_surface(w, h // 3)
    for i in range(h // 3):
        alpha = int(intensity * (1 - i / (h // 3)))
        pygame.draw.line(highlight, (255, 255, 255, alpha), (0, i), (w, i))
    surface.blit(highlight, (x, y))


def add_shadow(surface, rect, intensity=50):
    """Add a subtle shadow to the bottom of an object."""
    x, y, w, h = rect
    shadow_height = h // 4
    for i in range(shadow_height):
        alpha = int(intensity * i / shadow_height)
        pygame.draw.line(surface, (0, 0, 0, alpha), (x, y + h - shadow_height + i), (x + w, y + h - shadow_height + i))


# ============ ITEM GENERATORS ============

def generate_key_item(width=50, height=50, color=(255, 215, 0)):
    """Generate a shiny key."""
    surface = create_transparent_surface(width, height)

    # Key body
    cx, cy = width // 2, height // 2

    # Key head (circle)
    head_radius = min(width, height) // 4
    pygame.draw.circle(surface, color, (cx - 5, cy - 8), head_radius)
    pygame.draw.circle(surface, (color[0] * 0.7, color[1] * 0.7, color[2] * 0.7), (cx - 5, cy - 8), head_radius - 3)
    pygame.draw.circle(surface, color, (cx - 5, cy - 8), head_radius - 6)

    # Key shaft
    shaft_width = 6
    pygame.draw.rect(surface, color, (cx - shaft_width // 2, cy, shaft_width, height // 2 - 5))

    # Key teeth
    tooth_y = cy + height // 3
    pygame.draw.rect(surface, color, (cx, tooth_y, 8, 4))
    pygame.draw.rect(surface, color, (cx, tooth_y + 8, 6, 4))

    # Highlight
    pygame.draw.circle(surface, (255, 255, 255, 100), (cx - 8, cy - 12), 4)

    return surface


def generate_potion_item(width=50, height=50, color=(100, 200, 255)):
    """Generate a potion bottle."""
    surface = create_transparent_surface(width, height)

    cx, cy = width // 2, height // 2

    # Bottle body
    body_width = width // 2
    body_height = height // 2
    body_rect = (cx - body_width // 2, cy, body_width, body_height)
    pygame.draw.ellipse(surface, color, body_rect)

    # Bottle neck
    neck_width = body_width // 3
    pygame.draw.rect(surface, (200, 200, 200), (cx - neck_width // 2, cy - 10, neck_width, 15))

    # Cork
    cork_width = neck_width + 4
    pygame.draw.ellipse(surface, (139, 90, 43), (cx - cork_width // 2, cy - 15, cork_width, 10))

    # Liquid highlight
    pygame.draw.ellipse(surface, (255, 255, 255, 80), (cx - body_width // 4, cy + 5, body_width // 3, body_height // 3))

    # Glass shine
    pygame.draw.arc(surface, (255, 255, 255, 100), body_rect, 0.5, 2.0, 2)

    return surface


def generate_book_item(width=50, height=50, color=(139, 69, 19)):
    """Generate a book."""
    surface = create_transparent_surface(width, height)

    # Book cover
    cover_rect = (8, 5, width - 16, height - 10)
    pygame.draw.rect(surface, color, cover_rect, border_radius=3)

    # Pages
    pages_rect = (10, 8, width - 22, height - 16)
    pygame.draw.rect(surface, (255, 250, 240), pages_rect)

    # Page lines
    for i in range(3):
        y = 15 + i * 8
        pygame.draw.line(surface, (200, 200, 200), (14, y), (width - 18, y))

    # Spine
    pygame.draw.rect(surface, (color[0] * 0.7, color[1] * 0.7, color[2] * 0.7), (5, 5, 5, height - 10), border_radius=2)

    # Decoration
    pygame.draw.rect(surface, (255, 215, 0), (12, height // 2 - 3, width - 28, 6), border_radius=2)

    return surface


def generate_scroll_item(width=50, height=50):
    """Generate a scroll."""
    surface = create_transparent_surface(width, height)

    # Paper color
    paper = (255, 248, 220)
    roll = (210, 180, 140)

    # Main scroll body
    pygame.draw.rect(surface, paper, (10, 12, width - 20, height - 24))

    # Top roll
    pygame.draw.ellipse(surface, roll, (5, 5, width - 10, 16))
    pygame.draw.ellipse(surface, (roll[0] * 0.8, roll[1] * 0.8, roll[2] * 0.8), (8, 8, width - 16, 10))

    # Bottom roll
    pygame.draw.ellipse(surface, roll, (5, height - 21, width - 10, 16))
    pygame.draw.ellipse(surface, (roll[0] * 0.8, roll[1] * 0.8, roll[2] * 0.8), (8, height - 18, width - 16, 10))

    # Text lines
    for i in range(3):
        y = 20 + i * 7
        pygame.draw.line(surface, (100, 100, 100), (15, y), (width - 15, y))

    return surface


def generate_gem_item(width=50, height=50, color=(255, 0, 100)):
    """Generate a sparkling gem."""
    surface = create_transparent_surface(width, height)

    cx, cy = width // 2, height // 2

    # Gem shape (hexagon-ish)
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 90)
        r = min(width, height) // 3
        x = cx + int(r * math.cos(angle))
        y = cy + int(r * math.sin(angle) * 0.8)
        points.append((x, y))

    # Main gem
    pygame.draw.polygon(surface, color, points)

    # Facets (lighter)
    lighter = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
    pygame.draw.polygon(surface, lighter, [points[0], points[1], (cx, cy)])
    pygame.draw.polygon(surface, lighter, [points[5], points[0], (cx, cy)])

    # Sparkle
    pygame.draw.circle(surface, (255, 255, 255, 200), (cx - 5, cy - 5), 3)
    pygame.draw.circle(surface, (255, 255, 255, 150), (cx + 3, cy - 8), 2)

    return surface


def generate_herb_item(width=50, height=50, color=(34, 139, 34)):
    """Generate an herb/plant."""
    surface = create_transparent_surface(width, height)

    cx = width // 2

    # Stem
    pygame.draw.line(surface, (34, 100, 34), (cx, height - 5), (cx, height // 3), 3)

    # Leaves
    leaf_color = color

    # Left leaf
    points = [(cx - 3, height // 2), (cx - 15, height // 3), (cx - 5, height // 4), (cx - 3, height // 2 - 5)]
    pygame.draw.polygon(surface, leaf_color, points)

    # Right leaf
    points = [(cx + 3, height // 2), (cx + 15, height // 3), (cx + 5, height // 4), (cx + 3, height // 2 - 5)]
    pygame.draw.polygon(surface, leaf_color, points)

    # Top leaves
    points = [(cx, height // 4), (cx - 10, 10), (cx, 5), (cx + 10, 10)]
    pygame.draw.polygon(surface, leaf_color, points)

    # Vein lines
    pygame.draw.line(surface, (20, 80, 20), (cx - 8, height // 3), (cx - 3, height // 2 - 5), 1)
    pygame.draw.line(surface, (20, 80, 20), (cx + 8, height // 3), (cx + 3, height // 2 - 5), 1)

    return surface


# ============ NPC GENERATORS ============

def generate_character_sprite(width=150, height=160, skin_color=(255, 220, 185),
                              hair_color=(50, 30, 20), clothes_color=(70, 130, 180), name=""):
    """Generate a simple character sprite."""
    surface = create_transparent_surface(width, height)

    cx = width // 2

    # Body
    body_top = height // 3
    body_rect = (cx - 25, body_top + 30, 50, 60)
    pygame.draw.ellipse(surface, clothes_color, body_rect)

    # Arms
    pygame.draw.ellipse(surface, clothes_color, (cx - 40, body_top + 35, 20, 45))
    pygame.draw.ellipse(surface, clothes_color, (cx + 20, body_top + 35, 20, 45))

    # Hands
    pygame.draw.circle(surface, skin_color, (cx - 30, body_top + 75), 8)
    pygame.draw.circle(surface, skin_color, (cx + 30, body_top + 75), 8)

    # Head
    head_y = body_top - 5
    pygame.draw.ellipse(surface, skin_color, (cx - 22, head_y, 44, 50))

    # Hair
    pygame.draw.ellipse(surface, hair_color, (cx - 25, head_y - 5, 50, 30))

    # Eyes
    eye_y = head_y + 20
    pygame.draw.ellipse(surface, (255, 255, 255), (cx - 12, eye_y, 10, 12))
    pygame.draw.ellipse(surface, (255, 255, 255), (cx + 2, eye_y, 10, 12))
    pygame.draw.circle(surface, (50, 50, 50), (cx - 7, eye_y + 6), 4)
    pygame.draw.circle(surface, (50, 50, 50), (cx + 7, eye_y + 6), 4)

    # Smile
    pygame.draw.arc(surface, (150, 100, 100), (cx - 8, eye_y + 12, 16, 10), 3.14, 0, 2)

    # Legs
    pygame.draw.rect(surface, (50, 50, 70), (cx - 18, body_top + 85, 14, 35))
    pygame.draw.rect(surface, (50, 50, 70), (cx + 4, body_top + 85, 14, 35))

    # Feet
    pygame.draw.ellipse(surface, (80, 50, 30), (cx - 22, height - 25, 20, 12))
    pygame.draw.ellipse(surface, (80, 50, 30), (cx + 2, height - 25, 20, 12))

    return surface


def generate_creature_sprite(width=80, height=90, base_color=(100, 150, 100), name=""):
    """Generate a creature/monster sprite."""
    surface = create_transparent_surface(width, height)

    cx, cy = width // 2, height // 2

    # Body (blob shape)
    pygame.draw.ellipse(surface, base_color, (10, 20, width - 20, height - 30))

    # Lighter belly
    lighter = (min(255, base_color[0] + 40), min(255, base_color[1] + 40), min(255, base_color[2] + 40))
    pygame.draw.ellipse(surface, lighter, (20, 35, width - 40, height - 55))

    # Eyes
    eye_y = cy - 5
    pygame.draw.ellipse(surface, (255, 255, 255), (cx - 18, eye_y, 16, 20))
    pygame.draw.ellipse(surface, (255, 255, 255), (cx + 2, eye_y, 16, 20))
    pygame.draw.circle(surface, (30, 30, 30), (cx - 10, eye_y + 10), 5)
    pygame.draw.circle(surface, (30, 30, 30), (cx + 10, eye_y + 10), 5)

    # Eye shine
    pygame.draw.circle(surface, (255, 255, 255), (cx - 12, eye_y + 7), 2)
    pygame.draw.circle(surface, (255, 255, 255), (cx + 8, eye_y + 7), 2)

    # Mouth
    pygame.draw.arc(surface, (50, 50, 50), (cx - 12, cy + 10, 24, 15), 3.14, 0, 2)

    # Little feet
    pygame.draw.ellipse(surface, base_color, (15, height - 20, 20, 15))
    pygame.draw.ellipse(surface, base_color, (width - 35, height - 20, 20, 15))

    return surface


# ============ BUTTON/ACTION GENERATORS ============

def generate_button(width=50, height=50, color=(200, 50, 50), pressed=False):
    """Generate a push button."""
    surface = create_transparent_surface(width, height)

    # Base
    base_color = (80, 80, 90)
    pygame.draw.ellipse(surface, base_color, (5, height - 20, width - 10, 20))

    # Button body
    button_height = height - 25 if not pressed else height - 30
    pygame.draw.ellipse(surface, color, (8, 10, width - 16, button_height))

    # Highlight
    lighter = (min(255, color[0] + 60), min(255, color[1] + 60), min(255, color[2] + 60))
    pygame.draw.ellipse(surface, lighter, (12, 12, width - 28, button_height // 3))

    # Shadow on button
    darker = (color[0] * 0.6, color[1] * 0.6, color[2] * 0.6)
    pygame.draw.arc(surface, darker, (8, 10, width - 16, button_height), 3.5, 6.0, 3)

    return surface


def generate_lever(width=50, height=80, activated=False):
    """Generate a lever."""
    surface = create_transparent_surface(width, height)

    cx = width // 2

    # Base
    pygame.draw.rect(surface, (100, 100, 110), (cx - 15, height - 25, 30, 20), border_radius=5)
    pygame.draw.ellipse(surface, (80, 80, 90), (cx - 18, height - 20, 36, 15))

    # Lever arm
    if activated:
        # Pointing right
        pygame.draw.line(surface, (150, 150, 160), (cx, height - 25), (cx + 20, 15), 6)
        pygame.draw.circle(surface, (200, 50, 50), (cx + 20, 15), 10)
    else:
        # Pointing left
        pygame.draw.line(surface, (150, 150, 160), (cx, height - 25), (cx - 20, 15), 6)
        pygame.draw.circle(surface, (50, 200, 50), (cx - 20, 15), 10)

    # Pivot point
    pygame.draw.circle(surface, (60, 60, 70), (cx, height - 25), 8)

    return surface


# ============ DOOR GENERATORS ============

def generate_door(width=100, height=200, color=(139, 90, 43), locked=False):
    """Generate a door."""
    surface = create_transparent_surface(width, height)

    # Door frame
    frame_color = (80, 50, 30)
    pygame.draw.rect(surface, frame_color, (0, 0, width, height), border_radius=5)

    # Door body
    pygame.draw.rect(surface, color, (8, 8, width - 16, height - 16), border_radius=3)

    # Panels
    panel_color = (color[0] * 0.85, color[1] * 0.85, color[2] * 0.85)
    pygame.draw.rect(surface, panel_color, (15, 20, width - 30, 60), border_radius=3)
    pygame.draw.rect(surface, panel_color, (15, 100, width - 30, 80), border_radius=3)

    # Handle
    handle_y = height // 2
    pygame.draw.circle(surface, (255, 215, 0), (width - 25, handle_y), 8)
    pygame.draw.circle(surface, (200, 170, 0), (width - 25, handle_y), 5)

    # Keyhole if locked
    if locked:
        pygame.draw.ellipse(surface, (30, 30, 30), (width - 30, handle_y + 15, 10, 15))
        # Lock indicator
        pygame.draw.circle(surface, (255, 50, 50), (width - 25, handle_y - 15), 5)

    # Wood grain lines
    for i in range(3):
        y = 30 + i * 50
        pygame.draw.line(surface, (color[0] * 0.9, color[1] * 0.9, color[2] * 0.9),
                        (20, y), (width - 20, y + 10), 1)

    return surface


# ============ MENU BUTTON GENERATOR ============

def generate_menu_button(width=200, height=50, text="Button", font_size=24):
    """Generate a styled menu button."""
    pygame.font.init()
    surface = create_transparent_surface(width, height)

    # Gradient background
    for i in range(height):
        ratio = i / height
        r = int(70 + 30 * (1 - ratio))
        g = int(130 + 30 * (1 - ratio))
        b = int(180 + 30 * (1 - ratio))
        pygame.draw.line(surface, (r, g, b), (0, i), (width, i))

    # Round the corners by masking
    mask = create_transparent_surface(width, height)
    pygame.draw.rect(mask, (255, 255, 255), (0, 0, width, height), border_radius=10)

    final = create_transparent_surface(width, height)
    final.blit(surface, (0, 0))
    final.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Border
    pygame.draw.rect(final, (100, 180, 230), (0, 0, width, height), 2, border_radius=10)

    # Highlight at top
    pygame.draw.line(final, (255, 255, 255, 80), (10, 3), (width - 10, 3), 1)

    # Text
    try:
        font = pygame.font.Font(None, font_size)
    except:
        font = pygame.font.SysFont('arial', font_size - 4)

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    final.blit(text_surface, text_rect)

    return final


# ============ BACKGROUND GENERATORS ============

def generate_room_background(width, height, theme="forest"):
    """Generate a simple room background."""
    surface = pygame.Surface((width, height))

    if theme == "forest":
        # Sky gradient
        for y in range(height // 2):
            ratio = y / (height // 2)
            r = int(135 + 50 * ratio)
            g = int(206 + 30 * ratio)
            b = int(235 + 20 * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

        # Ground
        pygame.draw.rect(surface, (34, 139, 34), (0, height // 2, width, height // 2))

        # Trees in background
        for x in range(0, width, 100):
            tree_height = 150 + (x % 50)
            pygame.draw.rect(surface, (101, 67, 33), (x + 40, height // 2 - tree_height + 50, 20, tree_height))
            pygame.draw.circle(surface, (34, 100, 34), (x + 50, height // 2 - tree_height + 50), 40)
            pygame.draw.circle(surface, (50, 120, 50), (x + 50, height // 2 - tree_height + 30), 30)

    elif theme == "dungeon":
        # Dark stone walls
        surface.fill((40, 35, 45))

        # Stone pattern
        for y in range(0, height, 40):
            offset = 20 if (y // 40) % 2 else 0
            for x in range(-20 + offset, width, 60):
                pygame.draw.rect(surface, (50, 45, 55), (x, y, 58, 38), border_radius=2)
                pygame.draw.rect(surface, (35, 30, 40), (x, y, 58, 38), 2, border_radius=2)

        # Torches
        for x in [100, width - 100]:
            pygame.draw.rect(surface, (80, 60, 40), (x - 5, 100, 10, 30))
            pygame.draw.circle(surface, (255, 150, 50), (x, 95), 15)
            pygame.draw.circle(surface, (255, 200, 100), (x, 90), 8)

    elif theme == "beach":
        # Sky
        for y in range(height // 2):
            ratio = y / (height // 2)
            pygame.draw.line(surface, (int(135 + 100 * ratio), int(200 + 55 * ratio), 255), (0, y), (width, y))

        # Water
        for y in range(height // 2, int(height * 0.7)):
            ratio = (y - height // 2) / (height * 0.2)
            pygame.draw.line(surface, (int(65 + 30 * ratio), int(105 + 50 * ratio), int(225 - 30 * ratio)), (0, y), (width, y))

        # Sand
        pygame.draw.rect(surface, (238, 214, 175), (0, int(height * 0.7), width, int(height * 0.3)))

        # Sun
        pygame.draw.circle(surface, (255, 255, 200), (width - 100, 80), 50)

    else:  # indoor/office
        # Floor
        surface.fill((180, 160, 140))

        # Wall
        pygame.draw.rect(surface, (220, 210, 200), (0, 0, width, height // 2))

        # Baseboard
        pygame.draw.rect(surface, (100, 80, 60), (0, height // 2 - 10, width, 20))

    return surface


def save_asset(surface, path):
    """Save a surface as a PNG with transparency."""
    ensure_dir(path)
    pygame.image.save(surface, path)
    print(f"Saved: {path}")


def generate_all_assets():
    """Generate all placeholder assets for the game."""
    pygame.init()

    # Items
    items = {
        "assets/items/key_gold.png": generate_key_item(50, 50, (255, 215, 0)),
        "assets/items/key_silver.png": generate_key_item(50, 50, (192, 192, 192)),
        "assets/items/potion_blue.png": generate_potion_item(50, 50, (100, 150, 255)),
        "assets/items/potion_red.png": generate_potion_item(50, 50, (255, 100, 100)),
        "assets/items/potion_green.png": generate_potion_item(50, 50, (100, 255, 100)),
        "assets/items/book_brown.png": generate_book_item(50, 50, (139, 69, 19)),
        "assets/items/book_red.png": generate_book_item(50, 50, (180, 50, 50)),
        "assets/items/scroll.png": generate_scroll_item(50, 50),
        "assets/items/gem_red.png": generate_gem_item(50, 50, (220, 20, 60)),
        "assets/items/gem_blue.png": generate_gem_item(50, 50, (30, 144, 255)),
        "assets/items/gem_green.png": generate_gem_item(50, 50, (50, 205, 50)),
        "assets/items/herb_green.png": generate_herb_item(50, 50, (34, 139, 34)),
        "assets/items/herb_purple.png": generate_herb_item(50, 50, (148, 0, 211)),
    }

    # Actions/Buttons
    actions = {
        "assets/actions/button_red.png": generate_button(50, 50, (200, 50, 50)),
        "assets/actions/button_red_pressed.png": generate_button(50, 50, (200, 50, 50), pressed=True),
        "assets/actions/button_green.png": generate_button(50, 50, (50, 200, 50)),
        "assets/actions/button_blue.png": generate_button(50, 50, (50, 100, 200)),
        "assets/actions/lever_off.png": generate_lever(50, 80, activated=False),
        "assets/actions/lever_on.png": generate_lever(50, 80, activated=True),
    }

    # Doors
    doors = {
        "assets/doors/door_wood.png": generate_door(100, 200, (139, 90, 43)),
        "assets/doors/door_wood_locked.png": generate_door(100, 200, (139, 90, 43), locked=True),
        "assets/doors/door_dark.png": generate_door(100, 200, (60, 40, 30)),
        "assets/doors/door_dark_locked.png": generate_door(100, 200, (60, 40, 30), locked=True),
    }

    # NPCs
    npcs = {
        "assets/npcs/villager_male.png": generate_character_sprite(150, 160,
            skin_color=(255, 220, 185), hair_color=(50, 30, 20), clothes_color=(70, 130, 180)),
        "assets/npcs/villager_female.png": generate_character_sprite(150, 160,
            skin_color=(255, 220, 185), hair_color=(150, 100, 50), clothes_color=(180, 100, 150)),
        "assets/npcs/wizard.png": generate_character_sprite(150, 160,
            skin_color=(255, 220, 185), hair_color=(200, 200, 200), clothes_color=(80, 50, 120)),
        "assets/npcs/creature_green.png": generate_creature_sprite(80, 90, (100, 180, 100)),
        "assets/npcs/creature_blue.png": generate_creature_sprite(80, 90, (100, 150, 200)),
        "assets/npcs/creature_purple.png": generate_creature_sprite(80, 90, (150, 100, 180)),
    }

    # Menu buttons
    menu = {
        "assets/menu/btn_start.png": generate_menu_button(250, 60, "Start Game", 28),
        "assets/menu/btn_continue.png": generate_menu_button(250, 60, "Continue", 28),
        "assets/menu/btn_settings.png": generate_menu_button(250, 60, "Settings", 28),
        "assets/menu/btn_quit.png": generate_menu_button(250, 60, "Quit", 28),
        "assets/menu/btn_back.png": generate_menu_button(150, 45, "Back", 22),
    }

    # Save all
    all_assets = {**items, **actions, **doors, **npcs, **menu}

    for path, surface in all_assets.items():
        save_asset(surface, path)

    print(f"\nGenerated {len(all_assets)} assets!")
    return all_assets


if __name__ == "__main__":
    generate_all_assets()
    pygame.quit()
