import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_HEIGHT


class AnswerBox(pygame.sprite.Sprite):
    """Container for dialog answer options."""
    _id_counter = 1
    containers = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - INVENTORY_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT)
        self.id = AnswerBox._id_counter
        AnswerBox._id_counter += 1
        self.state = None
        self.room = None
        self.answers = {}

    def draw(self, screen):
        pygame.draw.rect(screen, "blue", self.rect)
        for answer in self.answers.values():
            screen.blit(answer.surface, answer.rect)

    def add_answer(self, answer):
        """Add an answer option to this box."""
        self.answers[answer.answer] = answer

    def update(self, dt):
        pass
