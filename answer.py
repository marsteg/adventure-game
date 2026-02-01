import pygame

from rectshape import RectShape
from constants import SCREEN_HEIGHT, INVENTORY_HEIGHT


class Answer(RectShape):
    """Represents a clickable dialog answer option."""
    _id_counter = 1
    containers = []

    def __init__(self, answer, index):
        # Position and size now handled by AnswerRenderer
        self.left = 10
        self.height = 30  # Standard height for answer options
        self.top = (SCREEN_HEIGHT - INVENTORY_HEIGHT + 5) + (index * 25)
        self.width = 200  # Default width, will be set by renderer

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
