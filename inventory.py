import pygame
import random
from constants import *


class Inventory(pygame.sprite.Sprite):
    containers = []
    items = {}
    slot = {}
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - INVENTORY_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT)
        self.init_slots()

    def draw(self, screen):
        inv = pygame.draw.rect(screen, "brown", self.rect)
        screen.fill("brown", inv)
        for item in self.items.values():
            item.draw(screen)

    def update(self, dt):
        pass
    
    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    
    def init_slots(self):
        for i in range(0, 19):
            Inventory.slot[i] = {"pos": (at_percentage_width(i*5)+5, SCREEN_HEIGHT - INVENTORY_HEIGHT + 5), "item": None}
        
    def get_available_slots(self, item):
        for slot in Inventory.slot.values():
            if slot["item"] == None:
                slot["item"] = item
                return slot["pos"] 
        return None
    
    def release_slots(self, item):
        for slot in Inventory.slot.values():
            if slot["item"] == item:
                slot["item"] = None
                return
        return None
        
