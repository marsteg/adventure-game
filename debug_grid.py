"""Debug grid overlay for positioning game objects."""

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_HEIGHT, WHITE, GREEN, YELLOW, RED

class DebugGrid:
    """Shows a grid overlay with coordinates and percentage markers."""

    def __init__(self):
        self.enabled = False
        self.show_percentages = True
        self.show_coordinates = True
        self.grid_spacing = 50  # pixels between grid lines
        self.font = None
        self.font_large = None
        self.hover_info_font = None

    def _init_fonts(self):
        """Initialize fonts lazily when first needed."""
        if self.font is None:
            self.font = pygame.font.Font(None, 16)
            self.font_large = pygame.font.Font(None, 20)
            self.hover_info_font = pygame.font.Font(None, 24)

    def toggle(self):
        """Toggle grid visibility."""
        self.enabled = not self.enabled
        return self.enabled

    def draw(self, screen, mouse_pos=None):
        """Draw the grid overlay."""
        if not self.enabled:
            return

        # Initialize fonts if not done yet
        self._init_fonts()

        playable_height = SCREEN_HEIGHT - INVENTORY_HEIGHT

        # Draw vertical grid lines
        for x in range(0, SCREEN_WIDTH, self.grid_spacing):
            # Main grid line
            pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, playable_height), 1)

            # Every 100 pixels, draw a thicker line and label
            if x % 100 == 0:
                pygame.draw.line(screen, (150, 150, 150), (x, 0), (x, playable_height), 2)

                if self.show_coordinates:
                    label = self.font.render(str(x), True, WHITE)
                    screen.blit(label, (x + 2, 2))

        # Draw horizontal grid lines
        for y in range(0, playable_height, self.grid_spacing):
            # Main grid line
            pygame.draw.line(screen, (100, 100, 100), (0, y), (SCREEN_WIDTH, y), 1)

            # Every 100 pixels, draw a thicker line and label
            if y % 100 == 0:
                pygame.draw.line(screen, (150, 150, 150), (0, y), (SCREEN_WIDTH, y), 2)

                if self.show_coordinates:
                    label = self.font.render(str(y), True, WHITE)
                    screen.blit(label, (2, y + 2))

        # Draw percentage markers at 10% intervals
        if self.show_percentages:
            for percent_x in range(0, 101, 10):
                x = int(SCREEN_WIDTH * percent_x / 100)
                pygame.draw.line(screen, YELLOW, (x, 0), (x, 20), 2)
                label = self.font_large.render(f"{percent_x}%", True, YELLOW)
                screen.blit(label, (x - 15, 22))

            for percent_y in range(0, 101, 10):
                y = int(playable_height * percent_y / 100)
                pygame.draw.line(screen, YELLOW, (0, y), (20, y), 2)
                label = self.font_large.render(f"{percent_y}%", True, YELLOW)
                screen.blit(label, (22, y - 8))

        # Draw inventory boundary
        pygame.draw.line(screen, RED, (0, playable_height), (SCREEN_WIDTH, playable_height), 3)
        boundary_label = self.font_large.render("INVENTORY BOUNDARY", True, RED)
        screen.blit(boundary_label, (SCREEN_WIDTH // 2 - 80, playable_height - 25))

        # Draw mouse position info
        if mouse_pos and 0 <= mouse_pos[0] < SCREEN_WIDTH and 0 <= mouse_pos[1] < playable_height:
            x, y = mouse_pos

            # Calculate percentages
            percent_x = (x / SCREEN_WIDTH) * 100
            percent_y = (y / playable_height) * 100

            # Draw crosshair
            pygame.draw.line(screen, GREEN, (x - 15, y), (x + 15, y), 2)
            pygame.draw.line(screen, GREEN, (x, y - 15), (x, y + 15), 2)
            pygame.draw.circle(screen, GREEN, mouse_pos, 5, 2)

            # Create info text
            info_lines = [
                f"Position: ({x}, {y})",
                f"Percentage: ({percent_x:.1f}%, {percent_y:.1f}%)",
                f"",
                f"at_percentage_width({percent_x:.1f})",
                f"at_percentage_height({percent_y:.1f})"
            ]

            # Draw info box
            box_width = 280
            box_height = len(info_lines) * 22 + 10
            box_x = min(x + 20, SCREEN_WIDTH - box_width - 10)
            box_y = min(y + 20, playable_height - box_height - 10)

            # Semi-transparent background
            info_bg = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            info_bg.fill((0, 0, 0, 200))
            screen.blit(info_bg, (box_x, box_y))

            # Border
            pygame.draw.rect(screen, GREEN, (box_x, box_y, box_width, box_height), 2)

            # Text
            for i, line in enumerate(info_lines):
                color = YELLOW if "at_percentage" in line else WHITE
                text = self.hover_info_font.render(line, True, color)
                screen.blit(text, (box_x + 10, box_y + 5 + i * 22))

        # Draw help text
        help_lines = [
            "GRID MODE - Press G to toggle",
            "Click anywhere to see position & percentage",
        ]
        help_y = playable_height - 50
        for i, line in enumerate(help_lines):
            text = self.font.render(line, True, WHITE)
            text_rect = text.get_rect()
            # Background
            bg = pygame.Surface((text_rect.width + 10, text_rect.height + 4), pygame.SRCALPHA)
            bg.fill((0, 0, 0, 180))
            screen.blit(bg, (5, help_y + i * 18))
            screen.blit(text, (10, help_y + 2 + i * 18))

# Global instance
debug_grid = DebugGrid()
