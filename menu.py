"""
Main Menu System - Clean, minimal design.
"""

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from save import GetMostRecentSlot


class MenuButton:
    """Simple, elegant menu button."""

    def __init__(self, x, y, width, height, text, action=None, enabled=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hover = False
        self.enabled = enabled
        self.font = pygame.font.Font(None, 26)


    def update(self, mouse_pos, clicked=False):
        if not self.enabled:
            self.hover = False
            return None
        self.hover = self.rect.collidepoint(mouse_pos)
        if clicked and self.hover and self.action:
            return self.action
        return None

    def draw(self, surface):
        # Simple underline style for hover
        if not self.enabled:
            text_color = (80, 80, 90)  # Disabled/grayed out
        elif self.hover:
            text_color = (255, 255, 255)
        else:
            text_color = (180, 180, 190)

        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        # Underline on hover (only if enabled)
        if self.hover and self.enabled:
            underline_y = text_rect.bottom + 2
            pygame.draw.line(surface, (255, 255, 255),
                           (text_rect.left, underline_y),
                           (text_rect.right, underline_y), 1)


class MainMenu:
    """Minimal main menu with Continue and Load Game options."""

    def __init__(self, title_text, in_game=False):
        """Initialize main menu.

        Args:
            title_text: Game title to display
            in_game: True if menu opened from gameplay (ESC), False if at startup
        """
        self.font_title = pygame.font.Font(None, 52)
        self.font_small = pygame.font.Font(None, 18)
        self.title_text = title_text
        self.in_game = in_game

        # Check if there's a recent save for Continue button
        self.most_recent_slot = GetMostRecentSlot()
        self.has_saves = self.most_recent_slot is not None

        # Button setup
        btn_width = 200
        btn_height = 40
        btn_x = SCREEN_WIDTH // 2 - btn_width // 2
        start_y = SCREEN_HEIGHT // 2 + 20
        spacing = 50

        # Different buttons based on context
        if in_game:
            # In-game menu (ESC pressed during gameplay)
            self.buttons = [
                MenuButton(btn_x, start_y, btn_width, btn_height, "Back to Game", "resume"),
                MenuButton(btn_x, start_y + spacing, btn_width, btn_height, "Save Game", "save"),
                MenuButton(btn_x, start_y + spacing * 2, btn_width, btn_height, "Load Game", "load"),
                MenuButton(btn_x, start_y + spacing * 3, btn_width, btn_height, "Quit to Menu", "quit_to_menu"),
            ]
        else:
            # Startup menu
            self.buttons = [
                MenuButton(btn_x, start_y, btn_width, btn_height, "Continue", "continue", enabled=self.has_saves),
                MenuButton(btn_x, start_y + spacing, btn_width, btn_height, "New Game", "start"),
                MenuButton(btn_x, start_y + spacing * 2, btn_width, btn_height, "Load Game", "load"),
                MenuButton(btn_x, start_y + spacing * 3, btn_width, btn_height, "Quit", "quit"),
            ]


    def update(self, mouse_pos, clicked, events=None):
        """Update menu state and handle input.

        Args:
            mouse_pos: Current mouse position
            clicked: Whether mouse was clicked
            events: Optional pygame events list for ESC key handling

        Returns:
            Action string or tuple
        """
        # Handle ESC key to close menu when in-game
        if self.in_game and events:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "resume"

        for button in self.buttons:
            action = button.update(mouse_pos, clicked)
            if action:
                if action == "continue":
                    return ("continue", self.most_recent_slot)
                elif action == "start":
                    return "start_game"
                elif action == "load":
                    return "load_game"
                elif action == "resume":
                    return "resume"
                elif action == "save":
                    return "save_game"
                elif action == "quit_to_menu":
                    return "quit_to_menu"
                elif action == "quit":
                    return "quit"
        return None

    def draw(self, surface):
        # Solid dark background
        surface.fill((18, 18, 24))

        # Title
        title = self.font_title.render(self.title_text, True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        surface.blit(title, title_rect)

        # Simple line under title
        line_y = title_rect.bottom + 15
        line_width = 80
        pygame.draw.line(surface, (60, 60, 70),
                        (SCREEN_WIDTH // 2 - line_width, line_y),
                        (SCREEN_WIDTH // 2 + line_width, line_y), 1)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

        # Version - bottom right, very subtle
        version = self.font_small.render("v2.0", True, (60, 60, 70))
        surface.blit(version, (SCREEN_WIDTH - 40, SCREEN_HEIGHT - 25))
