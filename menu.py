"""
Main Menu System - Clean, minimal design.
"""

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class MenuButton:
    """Simple, elegant menu button."""

    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hover = False
        self.font = None

    def _ensure_font(self):
        if self.font is None:
            self.font = pygame.font.Font(None, 26)

    def update(self, mouse_pos, clicked=False):
        self.hover = self.rect.collidepoint(mouse_pos)
        if clicked and self.hover and self.action:
            return self.action
        return None

    def draw(self, surface):
        self._ensure_font()

        # Simple underline style for hover
        text_color = (255, 255, 255) if self.hover else (180, 180, 190)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        # Underline on hover
        if self.hover:
            underline_y = text_rect.bottom + 2
            pygame.draw.line(surface, (255, 255, 255),
                           (text_rect.left, underline_y),
                           (text_rect.right, underline_y), 1)


class MainMenu:
    """Minimal main menu."""

    def __init__(self):
        self.font_title = None
        self.font_small = None

        # Button setup
        btn_width = 200
        btn_height = 40
        btn_x = SCREEN_WIDTH // 2 - btn_width // 2
        start_y = SCREEN_HEIGHT // 2 + 20
        spacing = 50

        self.buttons = [
            MenuButton(btn_x, start_y, btn_width, btn_height, "Start Game", "start"),
            MenuButton(btn_x, start_y + spacing, btn_width, btn_height, "Quit", "quit"),
        ]

    def _ensure_fonts(self):
        if self.font_title is None:
            self.font_title = pygame.font.Font(None, 52)
            self.font_small = pygame.font.Font(None, 18)

    def update(self, mouse_pos, clicked):
        for button in self.buttons:
            action = button.update(mouse_pos, clicked)
            if action:
                if action == "start":
                    return "start_game"
                elif action == "quit":
                    return "quit"
        return None

    def draw(self, surface):
        self._ensure_fonts()

        # Solid dark background
        surface.fill((18, 18, 24))

        # Title
        title_text = "Adventure Game"
        title = self.font_title.render(title_text, True, (255, 255, 255))
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
        version = self.font_small.render("v1.0", True, (60, 60, 70))
        surface.blit(version, (SCREEN_WIDTH - 40, SCREEN_HEIGHT - 25))
