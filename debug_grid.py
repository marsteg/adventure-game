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

    def draw(self, screen, mouse_pos=None, player_pos=None):
        """Draw the grid overlay.

        Args:
            screen: pygame screen surface
            mouse_pos: current mouse position tuple (x, y)
            player_pos: current player position tuple (x, y) - optional
        """
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

            # Calculate percentages for mouse position
            percent_x = (x / SCREEN_WIDTH) * 100
            percent_y = (y / playable_height) * 100

            # Calculate spawn position if player feet were at mouse cursor
            player_width = 50
            player_height = 75
            spawn_from_mouse_x = x - player_width // 2
            spawn_from_mouse_y = y - player_height
            spawn_percent_x = (spawn_from_mouse_x / SCREEN_WIDTH) * 100
            spawn_percent_y = (spawn_from_mouse_y / playable_height) * 100

            # Draw crosshair
            pygame.draw.line(screen, GREEN, (x - 15, y), (x + 15, y), 2)
            pygame.draw.line(screen, GREEN, (x, y - 15), (x, y + 15), 2)
            pygame.draw.circle(screen, GREEN, mouse_pos, 5, 2)

            # Create info text
            info_lines = [
                f"Mouse (Feet): ({x}, {y})",
                f"Percentage: ({percent_x:.1f}%, {percent_y:.1f}%)",
                f"",
                f"Spawn if feet here: ({spawn_from_mouse_x}, {spawn_from_mouse_y})",
                f"Percentage: ({spawn_percent_x:.1f}%, {spawn_percent_y:.1f}%)",
                f"",
                f"at_percentage_width({spawn_percent_x:.1f})",
                f"at_percentage_height({spawn_percent_y:.1f})"
            ]

            # Draw info box
            box_width = 320
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
                if "Spawn if feet here" in line:
                    color = (0, 255, 255)  # Cyan for spawn position
                elif "at_percentage" in line:
                    color = YELLOW
                else:
                    color = WHITE
                text = self.hover_info_font.render(line, True, color)
                screen.blit(text, (box_x + 10, box_y + 5 + i * 22))

        # Draw player position indicator
        if player_pos:
            # player_pos is the feet position (center-bottom)
            feet_x, feet_y = int(player_pos[0]), int(player_pos[1])

            # Only draw if player is in playable area
            if 0 <= feet_x < SCREEN_WIDTH and 0 <= feet_y < playable_height:
                # Calculate percentages for feet
                feet_percent_x = (feet_x / SCREEN_WIDTH) * 100
                feet_percent_y = (feet_y / playable_height) * 100

                # Draw feet marker (blue circle with cross)
                from constants import BLUE
                pygame.draw.circle(screen, BLUE, (feet_x, feet_y), 8, 3)
                pygame.draw.line(screen, BLUE, (feet_x - 12, feet_y), (feet_x + 12, feet_y), 3)
                pygame.draw.line(screen, BLUE, (feet_x, feet_y - 12), (feet_x, feet_y + 12), 3)

                # Draw label for feet position
                feet_label = f"FEET ({feet_x}, {feet_y})"
                feet_label_surf = self.font_large.render(feet_label, True, BLUE)
                feet_label_rect = feet_label_surf.get_rect()

                # Position label above feet marker
                feet_label_x = max(5, min(feet_x - feet_label_rect.width // 2, SCREEN_WIDTH - feet_label_rect.width - 5))
                feet_label_y = max(5, feet_y - 25)

                # Background for label
                feet_label_bg = pygame.Surface((feet_label_rect.width + 6, feet_label_rect.height + 4), pygame.SRCALPHA)
                feet_label_bg.fill((0, 0, 0, 200))
                screen.blit(feet_label_bg, (feet_label_x - 3, feet_label_y - 2))

                # Border
                pygame.draw.rect(screen, BLUE, (feet_label_x - 3, feet_label_y - 2, feet_label_rect.width + 6, feet_label_rect.height + 4), 1)

                # Label text
                screen.blit(feet_label_surf, (feet_label_x, feet_label_y))

                # Calculate spawn point (top-left) from feet position
                # Assuming player size from main.py: width=50, height=75
                player_width = 50
                player_height = 75
                spawn_x = feet_x - player_width // 2
                spawn_y = feet_y - player_height

                # Draw spawn point marker (cyan square)
                from constants import PURPLE
                spawn_color = (0, 255, 255)  # Cyan
                pygame.draw.rect(screen, spawn_color, (spawn_x - 4, spawn_y - 4, 8, 8), 2)
                pygame.draw.line(screen, spawn_color, (spawn_x - 8, spawn_y), (spawn_x + 8, spawn_y), 2)
                pygame.draw.line(screen, spawn_color, (spawn_x, spawn_y - 8), (spawn_x, spawn_y + 8), 2)

                # Draw line connecting spawn to feet
                pygame.draw.line(screen, (100, 100, 255), (spawn_x, spawn_y), (feet_x, feet_y), 1)

                # Draw label for spawn position
                spawn_label = f"SPAWN ({spawn_x}, {spawn_y})"
                spawn_label_surf = self.font.render(spawn_label, True, spawn_color)
                spawn_label_rect = spawn_label_surf.get_rect()

                # Position label above spawn marker
                spawn_label_x = max(5, min(spawn_x - spawn_label_rect.width // 2, SCREEN_WIDTH - spawn_label_rect.width - 5))
                spawn_label_y = max(5, spawn_y - 20)

                # Background for label
                spawn_label_bg = pygame.Surface((spawn_label_rect.width + 4, spawn_label_rect.height + 2), pygame.SRCALPHA)
                spawn_label_bg.fill((0, 0, 0, 200))
                screen.blit(spawn_label_bg, (spawn_label_x - 2, spawn_label_y - 1))

                # Border
                pygame.draw.rect(screen, spawn_color, (spawn_label_x - 2, spawn_label_y - 1, spawn_label_rect.width + 4, spawn_label_rect.height + 2), 1)

                # Label text
                screen.blit(spawn_label_surf, (spawn_label_x, spawn_label_y))

                # Draw player info box in top-right corner
                spawn_percent_x = (spawn_x / SCREEN_WIDTH) * 100
                spawn_percent_y = (spawn_y / playable_height) * 100

                player_info_lines = [
                    "PLAYER POSITION:",
                    f"Spawn: ({spawn_x}, {spawn_y})",
                    f"       ({spawn_percent_x:.1f}%, {spawn_percent_y:.1f}%)",
                    f"Feet:  ({feet_x}, {feet_y})",
                    f"       ({feet_percent_x:.1f}%, {feet_percent_y:.1f}%)",
                ]

                info_box_width = 250
                info_box_height = len(player_info_lines) * 20 + 10
                info_box_x = SCREEN_WIDTH - info_box_width - 10
                info_box_y = 10

                # Background
                player_info_bg = pygame.Surface((info_box_width, info_box_height), pygame.SRCALPHA)
                player_info_bg.fill((0, 0, 0, 200))
                screen.blit(player_info_bg, (info_box_x, info_box_y))

                # Border
                pygame.draw.rect(screen, BLUE, (info_box_x, info_box_y, info_box_width, info_box_height), 2)

                # Text
                for i, line in enumerate(player_info_lines):
                    if i == 0:
                        color = BLUE
                    elif "Spawn" in line:
                        color = spawn_color
                    elif "Feet" in line:
                        color = BLUE
                    else:
                        color = WHITE
                    text = self.font_large.render(line, True, color)
                    screen.blit(text, (info_box_x + 10, info_box_y + 5 + i * 20))

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
