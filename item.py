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

    def shine(self, screen):
        shiner = pygame.Surface((self.rect.width, self.rect.height))
        shiner.fill((255, 255, 255))
        shiner.set_alpha(100)
        screen.blit(shiner, self.rect.topleft)

    def update(self, dt):
        pass

    def kill(self):
        print("Item destroyed: ", self.id," on position: ", self.position)
        pygame.sprite.Sprite.kill(self) 

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    
    def move_ip(self, rel):
        self.rect.move_ip(rel)
        self.position = pygame.Vector2(self.rect.topleft)
        if self.position.y <= 0:
            self.position.y = 0
        if self.position.x <= 0:
            self.position.x = 0
        if self.position.y > SCREEN_HEIGHT - INVENTORY_HEIGHT:
            self.position.y = SCREEN_HEIGHT - INVENTORY_HEIGHT
        if self.position.x > SCREEN_WIDTH - self.rect.width:
            self.position.x = SCREEN_WIDTH - self.rect.width
        #return self.rect.move_ip(rel)
    
    def stash(self, inventory):
        inventory.items[self.id] = self
        self.stashed = True
        # how to stash properly? inventroy slots?
        self.rect.topleft = (self.id * 10 + self.rect.width, SCREEN_HEIGHT - INVENTORY_HEIGHT + 5)
        self.position = pygame.Vector2(self.rect.topleft)
        print("Item ID stashed: ", self.id)
        print("Inventory items: ", inventory.items)

    def unstash(self, inventory, pos):
        del inventory.items[self.id]
        self.stashed = False
        print("Item ID unstashed: ", self.id)
        print("Inventory items: ", inventory.items)