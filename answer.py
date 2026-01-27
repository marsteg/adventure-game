import pygame

from rectshape import RectShape
from constants import SCREEN_HEIGHT, INVENTORY_HEIGHT, SPEECH_FONT, SPEECH_SIZE, WHITE


class Answer(RectShape):
    """Represents a clickable dialog answer option."""
    _id_counter = 1
    containers = []

    def __init__(self, answer, index):
        speech_font = pygame.font.Font(SPEECH_FONT, SPEECH_SIZE)
        self.surface = speech_font.render(answer, True, WHITE)

        self.left = 10
        self.height = SPEECH_SIZE
        self.top = (SCREEN_HEIGHT - INVENTORY_HEIGHT + 5) + (index * 25)
        self.width = self.surface.get_width()

        super().__init__(self.left, self.top, self.width, self.height, "image")

        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.functions = []
        self.position = pygame.Vector2(self.left, self.top)
        self.answer = answer
        self.npc = None

    def add_dialogfunction(self, func, *args, **kwargs):
        """Add a function to be called when this answer is selected."""
        self.functions.append((func, args, kwargs))

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

    def action(self):
        """Execute all registered functions for this answer."""
        for func, args, kwargs in self.functions:
            func(*args, **kwargs)
            print(f"Answer action triggered: {self.answer}")
