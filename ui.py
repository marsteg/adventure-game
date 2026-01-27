"""
UI Module - Point-and-Click Adventure Style
Inspired by classics like Edna bricht aus, Deponia, Monkey Island
"""

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_HEIGHT


class Colors:
    """Muted, cinematic color palette."""
    PANEL_BG = (12, 12, 15, 235)
    SLOT_BG = (25, 25, 30, 200)
    SLOT_HOVER = (45, 45, 55)
    TEXT = (235, 230, 225)
    TEXT_DIM = (150, 145, 140)
    TEXT_HIGHLIGHT = (255, 252, 245)
    ACCENT = (210, 175, 110)
    DIALOG_BG = (18, 18, 22, 245)


def draw_rounded_rect(surface, color, rect, radius=8):
    """Draw a rounded rectangle with alpha support."""
    x, y, w, h = int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3])
    if w <= 0 or h <= 0:
        return
    if len(color) == 4:
        temp = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(temp, color, (0, 0, w, h), border_radius=min(radius, h//2, w//2))
        surface.blit(temp, (x, y))
    else:
        pygame.draw.rect(surface, color, (x, y, w, h), border_radius=min(radius, h//2, w//2))


class DialogRenderer:
    """Renders dialog boxes - positioned in upper area of screen."""

    def __init__(self):
        self.font = None
        self.font_name = None

    def _ensure_fonts(self):
        if self.font is None:
            self.font = pygame.font.Font(None, 24)
            self.font_name = pygame.font.Font(None, 18)

    def _wrap_text(self, text, max_width):
        self._ensure_fonts()
        words = text.split(' ')
        lines = []
        current = ""
        for word in words:
            test = current + " " + word if current else word
            if self.font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def render_dialog_box(self, surface, text, speaker_name="", speaker_color=None,
                          position=None, width=520, portrait=None):
        self._ensure_fonts()

        padding = 18
        wrapped = self._wrap_text(text, width - padding * 2)
        line_h = self.font.get_linesize() + 2
        text_h = len(wrapped) * line_h
        name_h = 22 if speaker_name else 0
        box_h = text_h + name_h + padding * 2

        # Position in middle-upper area - away from inventory
        if position is None:
            x = (SCREEN_WIDTH - width) // 2
            y = 80  # Fixed position near top
        else:
            x, y = position

        # Background
        draw_rounded_rect(surface, Colors.DIALOG_BG, (x, y, width, box_h), radius=6)
        pygame.draw.line(surface, Colors.ACCENT, (x + 12, y + 2), (x + width - 12, y + 2), 1)

        # Speaker name
        text_y = y + padding
        if speaker_name:
            color = speaker_color if speaker_color else Colors.ACCENT
            name_surf = self.font_name.render(speaker_name.upper(), True, color)
            surface.blit(name_surf, (x + padding, y + padding - 2))
            text_y += name_h

        # Dialog text
        for line in wrapped:
            line_surf = self.font.render(line, True, Colors.TEXT)
            surface.blit(line_surf, (x + padding, text_y))
            text_y += line_h

        return box_h  # Return height for answer positioning


class AnswerRenderer:
    """Renders dialog choices - positioned below dialog box."""

    def __init__(self):
        self.font = None

    def _ensure_font(self):
        if self.font is None:
            self.font = pygame.font.Font(None, 21)

    def render_answers(self, surface, answers, rect, hover_pos=None):
        self._ensure_font()

        if not answers:
            return []

        option_h = 30
        spacing = 4
        padding = 14
        total_h = len(answers) * (option_h + spacing) + padding * 2 - spacing
        width = 520

        # Position below dialog (around y=200)
        x = (SCREEN_WIDTH - width) // 2
        y = 200

        # Background
        draw_rounded_rect(surface, Colors.DIALOG_BG, (x, y, width, total_h), radius=6)

        answer_rects = []
        for i, answer in enumerate(answers):
            opt_y = y + padding + i * (option_h + spacing)
            opt_rect = pygame.Rect(x + padding, opt_y, width - padding * 2, option_h)

            is_hover = hover_pos and opt_rect.collidepoint(hover_pos)

            if is_hover:
                draw_rounded_rect(surface, (255, 255, 255, 20), opt_rect, radius=4)

            prefix = "› " if is_hover else "  "
            answer_text = answer if isinstance(answer, str) else answer.answer
            text_color = Colors.TEXT_HIGHLIGHT if is_hover else Colors.TEXT_DIM
            text_surf = self.font.render(f"{prefix}{answer_text}", True, text_color)
            surface.blit(text_surf, (opt_rect.x + 10, opt_rect.y + 6))

            answer_rects.append(opt_rect)

        return answer_rects


class InventoryRenderer:
    """Renders inventory - slim bottom bar."""

    def __init__(self):
        self.slot_size = 42
        self.slot_padding = 6

    def render(self, surface, items, rect, hover_pos=None, dragged_item=None):
        # Bar background
        bar_height = INVENTORY_HEIGHT
        bar_y = SCREEN_HEIGHT - bar_height
        draw_rounded_rect(surface, Colors.PANEL_BG, (0, bar_y, SCREEN_WIDTH, bar_height), radius=0)
        pygame.draw.line(surface, (35, 35, 40), (0, bar_y), (SCREEN_WIDTH, bar_y), 1)

        # Get items to display
        item_list = list(items.values()) if isinstance(items, dict) else items
        display_items = [i for i in item_list if i != dragged_item]

        if not display_items:
            return

        # Center items
        total_w = len(display_items) * (self.slot_size + self.slot_padding) - self.slot_padding
        start_x = (SCREEN_WIDTH - total_w) // 2
        slot_y = bar_y + (bar_height - self.slot_size) // 2

        for idx, item in enumerate(display_items):
            slot_x = start_x + idx * (self.slot_size + self.slot_padding)
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)

            is_hover = hover_pos and slot_rect.collidepoint(hover_pos)

            if is_hover:
                draw_rounded_rect(surface, Colors.SLOT_HOVER, slot_rect, radius=5)
                pygame.draw.rect(surface, Colors.ACCENT, slot_rect, 1, border_radius=5)
            else:
                draw_rounded_rect(surface, Colors.SLOT_BG, slot_rect, radius=5)

            item.rect = slot_rect.copy()

            if hasattr(item, 'image') and item.image:
                img_size = self.slot_size - 6
                scaled = pygame.transform.scale(item.image, (img_size, img_size))
                surface.blit(scaled, (slot_x + 3, slot_y + 3))


class TooltipRenderer:
    """Renders item name tooltips."""

    def __init__(self):
        self.font = None

    def _ensure_font(self):
        if self.font is None:
            self.font = pygame.font.Font(None, 19)

    def render(self, surface, text, position):
        self._ensure_font()

        padding = 7
        text_surf = self.font.render(text, True, Colors.TEXT)
        w = text_surf.get_width() + padding * 2
        h = text_surf.get_height() + padding * 2

        x = position[0] - w // 2
        y = position[1] - h - 12

        x = max(5, min(x, SCREEN_WIDTH - w - 5))
        y = max(5, y)

        draw_rounded_rect(surface, Colors.DIALOG_BG, (x, y, w, h), radius=4)
        surface.blit(text_surf, (x + padding, y + padding))


class TransitionEffect:
    """Screen fade transitions."""

    def __init__(self):
        self.active = False
        self.progress = 1.0
        self.fade_in = True
        self.speed = 0.05
        self.callback = None

    def start_fade(self, fade_in=True, callback=None):
        self.active = True
        self.fade_in = fade_in
        self.progress = 0.0 if fade_in else 1.0
        self.callback = callback

    def update(self):
        if not self.active:
            return
        if self.fade_in:
            self.progress += self.speed
            if self.progress >= 1.0:
                self.progress = 1.0
                self.active = False
                if self.callback:
                    self.callback()
        else:
            self.progress -= self.speed
            if self.progress <= 0.0:
                self.progress = 0.0
                self.active = False
                if self.callback:
                    self.callback()

    def render(self, surface):
        if not self.active and self.progress == 1.0:
            return
        alpha = int(255 * (1.0 - self.progress))
        if alpha > 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            surface.blit(overlay, (0, 0))


# Lazy initialization
_dialog_renderer = None
_answer_renderer = None
_inventory_renderer = None
_tooltip_renderer = None
_transition = None


def _ensure_initialized():
    global _dialog_renderer, _answer_renderer, _inventory_renderer, _tooltip_renderer, _transition
    if _dialog_renderer is None:
        _dialog_renderer = DialogRenderer()
        _answer_renderer = AnswerRenderer()
        _inventory_renderer = InventoryRenderer()
        _tooltip_renderer = TooltipRenderer()
        _transition = TransitionEffect()


class LazyRenderer:
    def __init__(self, getter):
        self._getter = getter

    def __getattr__(self, name):
        _ensure_initialized()
        return getattr(self._getter(), name)


dialog_renderer = LazyRenderer(lambda: _dialog_renderer)
answer_renderer = LazyRenderer(lambda: _answer_renderer)
inventory_renderer = LazyRenderer(lambda: _inventory_renderer)
tooltip_renderer = LazyRenderer(lambda: _tooltip_renderer)
transition = LazyRenderer(lambda: _transition)
