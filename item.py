from rectshape import *
from constants import *
from room import *

import random

class Item(RectShape):
    id_counter = 1
    containers = []
    items = {}
    def __init__(self, left, top, width, height, image, name, selfdestruct = False):
        super().__init__(left, top, width, height, image)  
        self.rotation = 0
        self.position = pygame.Vector2(left, top)
        self.original_position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.imagepath = image
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.name = name
        self.id = Item.id_counter
        Item.id_counter += 1
        self.selfdestruct = selfdestruct
        Item.items[self.name] = self
        self.stashed = False
        self.allow_destroy = False
        

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

    def kill(self, inventory, rooms):
        print("attempting Item destroy: ", self.name," on position: ", self.position, "selfdestruct: ", self.selfdestruct, "allow_destroy: ", self.allow_destroy)
        # how to destroy the item?
        # i would need to remove it from the inventory and the room
        if self.selfdestruct and self.allow_destroy:
            if self.name in inventory.items:
                if self == inventory.items[self.name]:
                    del inventory.items[self.name]
            for room in rooms.values():
                if self.name in room.items:
                    if self == room.items[self.name]:
                        del room.items[self.name]
                        inventory.release_slots(self)
                        print("Item removed from room: ", room.name)
                        pygame.sprite.Sprite.kill(self)
        else:
            self.stash(inventory)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    
    def move_ip(self, rel):
        self.rect.move_ip(rel)
        self.position = pygame.Vector2(self.rect.topleft)
        #return self.rect.move_ip(rel)
    
    def stash(self, inventory,room=None):
        inventory.release_slots(self)
        if self.stashed:
            # just reposition the item in the inventory
            pos = inventory.get_available_slots(self)
            print("old value: ", (self.id * (10 + self.rect.width), SCREEN_HEIGHT - INVENTORY_HEIGHT + 5))
            print("new value: ", pos)
            #self.rect.topleft = (self.id * (10 + self.rect.width), SCREEN_HEIGHT - INVENTORY_HEIGHT + 5)
            #self.position = pygame.Vector2(self.rect.topleft)
            self.rect.topleft = pos
            self.position = pygame.Vector2(pos)
            return
        if self.allow_destroy:
            print("Item Name: ", self.name, " can be destroyed")
            #self.kill(inventory, Room.rooms)
            return
        inventory.items[self.name] = self
        self.stashed = True
        if room != None:
            if self.name in room.items:
                if self == room.items[self.name]:
                    del room.items[self.name]
                    print("Item removed from room: ", room.name)
        # how to stash properly? inventroy slots?
        pos = inventory.get_available_slots(self)
        self.rect.topleft = (pos)
        self.position = pygame.Vector2(pos)
        #self.rect.topleft = (self.id * 10 + self.rect.width, SCREEN_HEIGHT - INVENTORY_HEIGHT + 5)
        #self.position = pygame.Vector2(self.rect.topleft)
        print("Item Name stashed: ", self.name)
        print("Item stashed: ", self.name)
        print("Inventory items: ", inventory.items)

    def unstash(self, inventory, pos):
        #del inventory.items[self.id]
        self.stashed = False
        inventory.release_slots(self)
        #self.position = self.original_position
        #self.rect.topleft = self.original_position
        print("Item unstashed: ", self.name)
        print("Inventory items: ", inventory.items)


        