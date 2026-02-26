"""
Save/Load Menu System with 9 slots + 1 auto-save slot.
Displays thumbnails, timestamps, room names, and playtime.
"""

import pygame
import os
from datetime import datetime
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from save import GetSlotMetadata, get_slot_thumbnail_filename


# Colors matching the existing UI style
MENU_BG = (18, 18, 24)
SLOT_EMPTY_BG = (25, 25, 30, 200)
SLOT_FILLED_BG = (35, 35, 40, 235)
SLOT_HOVER_BORDER = (210, 175, 110)  # Golden accent
SLOT_NORMAL_BORDER = (60, 60, 70)
TEXT_PRIMARY = (255, 255, 255)
TEXT_SECONDARY = (150, 150, 160)
TEXT_AUTO_SAVE = (100, 200, 255)  # Light blue for auto-save


class SaveSlot:
    """Represents a single save slot card."""

    def __init__(self, slot_number, x, y, width, height):
        self.slot_number = slot_number
        self.rect = pygame.Rect(x, y, width, height)
        self.metadata = None
        self.hover = False
        self.thumbnail = None
        self.font_title = pygame.font.Font(None, 20)
        self.font_detail = pygame.font.Font(None, 14)
        self.font_small = pygame.font.Font(None, 12)

        # Load metadata and thumbnail
        self.refresh()

    def refresh(self):
        """Reload metadata and thumbnail from disk."""
        self.metadata = GetSlotMetadata(self.slot_number)

        # Load thumbnail if it exists
        thumbnail_path = get_slot_thumbnail_filename(self.slot_number)
        if os.path.exists(thumbnail_path):
            try:
                # Load and scale thumbnail to fit slot
                original = pygame.image.load(thumbnail_path)
                # Thumbnail area: leave space for text at bottom
                thumb_height = self.rect.height - 55
                thumb_width = self.rect.width - 10
                self.thumbnail = pygame.transform.scale(original, (thumb_width, thumb_height))
            except Exception as e:
                print(f"Error loading thumbnail for slot {self.slot_number}: {e}")
                self.thumbnail = None
        else:
            self.thumbnail = None

    def is_empty(self):
        """Check if this slot is empty."""
        return self.metadata is None

    def update(self, mouse_pos):
        """Update hover state."""
        self.hover = self.rect.collidepoint(mouse_pos)

    def format_playtime(self, seconds):
        """Format playtime seconds into readable string."""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}m"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"

    def format_timestamp(self, timestamp_str):
        """Format timestamp into compact display."""
        try:
            # Parse: "2026-02-26 14:32:15"
            dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            # Display: "Feb 26, 14:32"
            return dt.strftime("%b %d, %H:%M")
        except Exception:
            return timestamp_str

    def draw(self, surface, mode="save"):
        """Draw the slot card.

        Args:
            surface: Pygame surface to draw on
            mode: "save" or "load" - affects interaction hints
        """
        # Determine background color and border
        if self.is_empty():
            bg_color = SLOT_EMPTY_BG
        else:
            bg_color = SLOT_FILLED_BG

        border_color = SLOT_HOVER_BORDER if self.hover else SLOT_NORMAL_BORDER
        border_width = 2 if self.hover else 1

        # Draw background
        bg_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        bg_surface.fill(bg_color)
        surface.blit(bg_surface, self.rect.topleft)

        # Draw border
        pygame.draw.rect(surface, border_color, self.rect, border_width)

        # Draw slot number label (top-left corner)
        if self.slot_number == 0:
            slot_label = "AUTO-SAVE"
            label_color = TEXT_AUTO_SAVE
        else:
            slot_label = f"SLOT {self.slot_number}"
            label_color = TEXT_SECONDARY

        label_surface = self.font_small.render(slot_label, True, label_color)
        label_pos = (self.rect.left + 5, self.rect.top + 5)
        surface.blit(label_surface, label_pos)

        if self.is_empty():
            # Draw "Empty Slot" text in center
            empty_text = self.font_title.render("Empty Slot", True, TEXT_SECONDARY)
            empty_rect = empty_text.get_rect(center=self.rect.center)
            surface.blit(empty_text, empty_rect)

            # Draw dashed border effect for empty slots
            dash_length = 10
            dash_spacing = 5
            dash_color = (80, 80, 90)

            # Top and bottom
            for x in range(self.rect.left, self.rect.right, dash_length + dash_spacing):
                pygame.draw.line(surface, dash_color,
                               (x, self.rect.top),
                               (min(x + dash_length, self.rect.right), self.rect.top), 1)
                pygame.draw.line(surface, dash_color,
                               (x, self.rect.bottom),
                               (min(x + dash_length, self.rect.right), self.rect.bottom), 1)

        else:
            # Draw thumbnail if available
            if self.thumbnail:
                thumb_pos = (self.rect.left + 5, self.rect.top + 20)
                surface.blit(self.thumbnail, thumb_pos)
            else:
                # Draw placeholder for no thumbnail
                placeholder_rect = pygame.Rect(
                    self.rect.left + 5,
                    self.rect.top + 20,
                    self.rect.width - 10,
                    self.rect.height - 60
                )
                pygame.draw.rect(surface, (40, 40, 50), placeholder_rect)
                no_thumb_text = self.font_small.render("No Preview", True, TEXT_SECONDARY)
                no_thumb_rect = no_thumb_text.get_rect(center=placeholder_rect.center)
                surface.blit(no_thumb_text, no_thumb_rect)

            # Draw metadata at bottom
            bottom_y = self.rect.bottom - 35

            # Room name
            room_name = self.metadata.get("room_name", "Unknown")
            room_text = self.font_title.render(room_name, True, TEXT_PRIMARY)
            room_pos = (self.rect.left + 5, bottom_y)
            surface.blit(room_text, room_pos)

            # Timestamp
            timestamp = self.metadata.get("timestamp", "")
            if timestamp:
                formatted_time = self.format_timestamp(timestamp)
                time_text = self.font_detail.render(formatted_time, True, TEXT_SECONDARY)
                time_pos = (self.rect.left + 5, bottom_y + 16)
                surface.blit(time_text, time_pos)

            # Playtime (top-right)
            playtime = self.metadata.get("playtime_seconds", 0)
            if playtime > 0:
                playtime_str = self.format_playtime(playtime)
                playtime_text = self.font_small.render(playtime_str, True, TEXT_SECONDARY)
                playtime_pos = (self.rect.right - playtime_text.get_width() - 5, self.rect.top + 5)
                surface.blit(playtime_text, playtime_pos)


class SaveLoadMenu:
    """Menu for saving/loading with 9 slots + 1 auto-save slot."""

    def __init__(self, mode="save"):
        """Initialize the save/load menu.

        Args:
            mode: "save" or "load"
        """
        self.mode = mode
        self.slots = []
        self.confirm_action = None  # ("overwrite", slot_num) or ("delete", slot_num)

        # Success message display
        self.success_message = None
        self.success_timer = 0
        self.success_duration = 2.0  # Show for 2 seconds

        self.font_title = pygame.font.Font(None, 42)
        self.font_subtitle = pygame.font.Font(None, 18)
        self.font_hint = pygame.font.Font(None, 16)
        self.font_success = pygame.font.Font(None, 22)
        self.font_button = pygame.font.Font(None, 24)

        # Back to Game button
        btn_width = 180
        btn_height = 40
        btn_x = SCREEN_WIDTH // 2 - btn_width // 2
        btn_y = SCREEN_HEIGHT - 70
        self.back_button = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
        self.back_button_hover = False

        # Calculate grid layout
        # 10 slots total: 1 auto-save slot (top) + 9 regular slots (3x3 grid)

        # Auto-save slot at top (wider)
        auto_save_width = 320
        auto_save_height = 100
        auto_save_x = SCREEN_WIDTH // 2 - auto_save_width // 2
        auto_save_y = 90

        self.slots.append(SaveSlot(0, auto_save_x, auto_save_y, auto_save_width, auto_save_height))

        # 3x3 grid for slots 1-9 (smaller to fit on screen)
        slot_width = 190
        slot_height = 140
        cols = 3
        rows = 3
        spacing_x = 15
        spacing_y = 15

        grid_width = cols * slot_width + (cols - 1) * spacing_x
        grid_start_x = (SCREEN_WIDTH - grid_width) // 2
        grid_start_y = auto_save_y + auto_save_height + 20

        for i in range(9):
            slot_num = i + 1  # Slots 1-9
            col = i % cols
            row = i // cols

            x = grid_start_x + col * (slot_width + spacing_x)
            y = grid_start_y + row * (slot_height + spacing_y)

            self.slots.append(SaveSlot(slot_num, x, y, slot_width, slot_height))

    def refresh_slots(self):
        """Refresh all slot metadata and thumbnails."""
        for slot in self.slots:
            slot.refresh()

    def show_success(self, message):
        """Show a success message temporarily.

        Args:
            message: Success message to display
        """
        self.success_message = message
        self.success_timer = self.success_duration

    def update(self, mouse_pos, events, dt=0):
        """Handle input and return action.

        Args:
            mouse_pos: Mouse position
            events: Pygame events
            dt: Delta time in milliseconds

        Returns:
            tuple or str or None:
                ("save", slot_num) - Save to slot
                ("load", slot_num) - Load from slot
                ("delete", slot_num) - Delete slot
                "cancel" - Cancel/exit menu
                None - No action
        """
        # Update success message timer
        if self.success_timer > 0:
            self.success_timer -= dt / 1000.0  # Convert ms to seconds
            if self.success_timer <= 0:
                self.success_message = None

        # Update hover states
        for slot in self.slots:
            slot.update(mouse_pos)

        # Update back button hover
        self.back_button_hover = self.back_button.collidepoint(mouse_pos)

        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "cancel"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check back button first
                    if self.back_button_hover:
                        return "cancel"

                    for slot in self.slots:
                        if slot.hover:
                            if self.mode == "save":
                                # Save mode: can click any slot
                                if slot.is_empty():
                                    return ("save", slot.slot_number)
                                else:
                                    # Occupied slot: ask for overwrite confirmation
                                    self.confirm_action = ("overwrite", slot.slot_number)
                                    return ("confirm_overwrite", slot.slot_number)

                            elif self.mode == "load":
                                # Load mode: can only click occupied slots
                                if not slot.is_empty():
                                    return ("load", slot.slot_number)

                elif event.button == 3:  # Right click
                    for slot in self.slots:
                        if slot.hover and not slot.is_empty():
                            # Right-click on occupied slot: delete
                            self.confirm_action = ("delete", slot.slot_number)
                            return ("confirm_delete", slot.slot_number)

        return None

    def draw(self, surface):
        """Render the menu."""
        # Dark background
        surface.fill(MENU_BG)

        # Title
        if self.mode == "save":
            title_text = "SAVE GAME"
        else:
            title_text = "LOAD GAME"

        title = self.font_title.render(title_text, True, TEXT_PRIMARY)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
        surface.blit(title, title_rect)

        # Subtitle line
        line_y = title_rect.bottom + 8
        line_width = 80
        pygame.draw.line(surface, SLOT_NORMAL_BORDER,
                        (SCREEN_WIDTH // 2 - line_width, line_y),
                        (SCREEN_WIDTH // 2 + line_width, line_y), 1)

        # Draw all slots
        for slot in self.slots:
            slot.draw(surface, self.mode)

        # Draw "Back to Game" button
        self._draw_back_button(surface)

        # Instructions at bottom (moved up a bit to make room for button)
        if self.mode == "save":
            hint_text = "Left-click to save  |  Right-click to delete"
        else:
            hint_text = "Left-click to load  |  Right-click to delete"

        hint = self.font_hint.render(hint_text, True, TEXT_SECONDARY)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        surface.blit(hint, hint_rect)

        # Draw success message if active
        if self.success_message and self.success_timer > 0:
            # Fade effect based on remaining time
            alpha = min(255, int(self.success_timer * 255))

            # Green background box
            msg_width = 400
            msg_height = 50
            msg_x = SCREEN_WIDTH // 2 - msg_width // 2
            msg_y = SCREEN_HEIGHT // 2 - msg_height // 2

            success_bg = pygame.Surface((msg_width, msg_height), pygame.SRCALPHA)
            success_bg.fill((40, 120, 60, min(220, alpha)))  # Green with alpha
            surface.blit(success_bg, (msg_x, msg_y))

            # Border
            pygame.draw.rect(surface, (80, 200, 100, alpha),
                           pygame.Rect(msg_x, msg_y, msg_width, msg_height), 2)

            # Success text
            success_text = self.font_success.render(self.success_message, True, (255, 255, 255, alpha))
            text_rect = success_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            surface.blit(success_text, text_rect)

    def _draw_back_button(self, surface):
        """Draw the Back to Game button."""
        # Button background
        if self.back_button_hover:
            bg_color = (60, 60, 70)
            border_color = SLOT_HOVER_BORDER  # Golden
            text_color = TEXT_PRIMARY
        else:
            bg_color = (40, 40, 50)
            border_color = SLOT_NORMAL_BORDER
            text_color = TEXT_SECONDARY

        # Draw button background
        pygame.draw.rect(surface, bg_color, self.back_button)
        pygame.draw.rect(surface, border_color, self.back_button, 2 if self.back_button_hover else 1)

        # Draw button text
        text = self.font_button.render("Back to Game", True, text_color)
        text_rect = text.get_rect(center=self.back_button.center)
        surface.blit(text, text_rect)


class ConfirmDialog:
    """Simple confirmation dialog for overwrite/delete actions."""

    def __init__(self, action_type, slot_number):
        """Initialize confirmation dialog.

        Args:
            action_type: "overwrite" or "delete"
            slot_number: Slot number being acted upon
        """
        self.action_type = action_type
        self.slot_number = slot_number

        self.font_title = pygame.font.Font(None, 32)
        self.font_text = pygame.font.Font(None, 22)
        self.font_button = pygame.font.Font(None, 24)

        # Dialog dimensions
        self.width = 400
        self.height = 200
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT // 2 - self.height // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Buttons
        btn_width = 120
        btn_height = 40
        btn_spacing = 20
        btn_y = self.y + self.height - 60

        self.btn_confirm = pygame.Rect(
            self.x + self.width // 2 - btn_width - btn_spacing // 2,
            btn_y,
            btn_width,
            btn_height
        )

        self.btn_cancel = pygame.Rect(
            self.x + self.width // 2 + btn_spacing // 2,
            btn_y,
            btn_width,
            btn_height
        )

        self.hover_confirm = False
        self.hover_cancel = False

    def update(self, mouse_pos, events):
        """Handle input and return action.

        Returns:
            "confirm" - User confirmed
            "cancel" - User cancelled
            None - No action yet
        """
        # Update hover states
        self.hover_confirm = self.btn_confirm.collidepoint(mouse_pos)
        self.hover_cancel = self.btn_cancel.collidepoint(mouse_pos)

        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "cancel"
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return "confirm"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.hover_confirm:
                        return "confirm"
                    elif self.hover_cancel:
                        return "cancel"

        return None

    def draw(self, surface):
        """Render the confirmation dialog."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Dialog box
        dialog_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        dialog_surface.fill((30, 30, 35, 250))
        pygame.draw.rect(dialog_surface, SLOT_HOVER_BORDER,
                        pygame.Rect(0, 0, self.width, self.height), 2)
        surface.blit(dialog_surface, (self.x, self.y))

        # Title
        if self.action_type == "overwrite":
            title_text = "Overwrite Save?"
            message_text = f"Overwrite existing save in Slot {self.slot_number}?"
        else:  # delete
            title_text = "Delete Save?"
            message_text = f"Permanently delete save in Slot {self.slot_number}?"

        title = self.font_title.render(title_text, True, TEXT_PRIMARY)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, self.y + 40))
        surface.blit(title, title_rect)

        # Message
        message = self.font_text.render(message_text, True, TEXT_SECONDARY)
        message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, self.y + 90))
        surface.blit(message, message_rect)

        # Buttons
        self._draw_button(surface, self.btn_confirm, "Confirm", self.hover_confirm, True)
        self._draw_button(surface, self.btn_cancel, "Cancel", self.hover_cancel, False)

    def _draw_button(self, surface, rect, text, hover, is_confirm):
        """Draw a button."""
        # Button background
        if hover:
            bg_color = (60, 60, 70)
            border_color = SLOT_HOVER_BORDER
        else:
            bg_color = (40, 40, 50)
            border_color = SLOT_NORMAL_BORDER

        pygame.draw.rect(surface, bg_color, rect)
        pygame.draw.rect(surface, border_color, rect, 2 if hover else 1)

        # Button text
        text_color = TEXT_PRIMARY if hover else TEXT_SECONDARY
        text_surface = self.font_button.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
