import pygame
import random
from constants import *


class DialogBox(pygame.sprite.Sprite):
    containers = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        #self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, 0)
        self.timer = 0
        self.state = None
        self.rects = []

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
    
    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
