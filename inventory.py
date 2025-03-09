import pygame
import random
from constants import *


class Inventory(pygame.sprite.Sprite):
    containers = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = pygame.Rect(0, SCREEN_HEIGHT-INVENTORY_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT)


    def draw(self, screen):
        inv = pygame.draw.rect(screen, "brown", self.rect)
        screen.fill("brown", inv)

    def update(self, dt):
        pass