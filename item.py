from rectshape import *
from constants import *

import random

class Item(RectShape):
    _id_counter = 1
    containers = []
    def __init__(self, left, top, width, height, image):
        super().__init__(left, top, width, height, image)  
        self.rotation = 0
        self.id = Item._id_counter
        Item._id_counter += 1
        self.position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.stashed = False
        

    def draw(self, screen):
        pygame.draw.rect(screen, "purple", self.rect)
        screen.blit(self.image, self.rect)

    def update(self, dt):
        pass

    def kill(self):
        print("Item destroyed: ", self.id," on position: ", self.position)
        pygame.sprite.Sprite.kill(self) 

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    
    def move_ip(self, rel):
        return self.rect.move_ip(rel)
    
    def stash(self,inventory):
        inventory.items[self.id] = self
        self.stashed = True
        print("Item ID stashed: ", self.id)
        print("Inventory items: ", inventory.items)

    def unstash(self,inventory):
        del inventory.items[self.id]
        self.stashed = False
        print("Item ID stashed: ", self.id)
        print("Inventory items: ", inventory.items)