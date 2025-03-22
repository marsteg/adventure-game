import pygame
from inventory import *
from item import *
from room import *
from door import *
from rectshape import *
from constants import *


class AnswerBox(pygame.sprite.Sprite):
    _id_counter = 1
    containers = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - INVENTORY_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT)
        self.id = AnswerBox._id_counter
        AnswerBox._id_counter += 1
        self.state = None
        self.functions = []
        self.answers = {}

    def draw(self, screen):
        answerbox = pygame.draw.rect(screen, "blue", self.rect)
        screen.fill("blue", answerbox)
        #screen.blit(self.surface, self.rect)
        if len(self.answers) > 0:
            for answer in self.answers.values():
                screen.blit(answer.surface, answer.rect)
        
    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def add_answer(self, answer):
        self.answers[answer.answer] = answer

    def update(self, dt):
        pass
