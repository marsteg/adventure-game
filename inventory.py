import pygame
import random
from constants import *


class Inventory(pygame.sprite.Sprite):
    containers = []
    items = {}
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - INVENTORY_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT)


    def draw(self, screen, inventory):
        inv = pygame.draw.rect(screen, "brown", self.rect)
        screen.fill("brown", inv)
        for num, item in inventory.items.items():
            item.rect.topleft = (num * 10 + item.rect.width, SCREEN_HEIGHT - INVENTORY_HEIGHT + 5)
            item.position = pygame.Vector2(item.rect.topleft)
            item.draw(screen)

    def update(self, dt):
        pass
    
    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
