"""Game constants and configuration."""

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
INVENTORY_HEIGHT = 54  # Slim bar at bottom
FPS = 60

# Interaction settings
INTERACTION_DISTANCE = 80

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240)

# Font settings (now handled by ui.py renderers)
# SPEECH_SIZE and SPEECH_FONT removed - no longer needed

# Audio settings
BACKGROUND_VOLUME = 0.1


def at_percentage_width(percentage):
    """Calculate a position as percentage of screen width."""
    return SCREEN_WIDTH * percentage / 100


def at_percentage_height(percentage):
    """Calculate a position as percentage of playable screen height (excluding inventory)."""
    return (SCREEN_HEIGHT - INVENTORY_HEIGHT) * percentage / 100
