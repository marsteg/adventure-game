import pygame
import random
from constants import *


class DialogBox(pygame.sprite.Sprite):
    containers = []
    room = None
    dialogboxes = []
    def __init__(self, room, time):
        pygame.sprite.Sprite.__init__(self, self.containers)
        #self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, 0)
        self.timer = time
        self.state = None
        self.rects = []
        self.room = room
        DialogBox.dialogboxes.append(self)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
    
    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    
    def kill(self):
        DialogBox.dialogboxes.remove(self)
        pygame.sprite.Sprite.kill(self)
        print("DialogBox removed")
