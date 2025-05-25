from rectshape import *
from constants import *
from room import *
import time

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
        self.timer = 0
        self.id = Item.id_counter
        Item.id_counter += 1
        self.selfdestruct = selfdestruct
        Item.items[self.name] = self
        self.functions = []
        self.stashed = False
        self.allow_destroy = False
        self.combinable_items = []
        self.combifunctions = []
        
    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def action(self):
        for func, args, kwargs in self.functions:
            func(*args, **kwargs)
            print("Item Action Function triggered in position: ", self.position)

    def draw(self, screen):
        pygame.draw.rect(screen, "purple", self.rect)
        screen.blit(self.image, self.rect)

    def add_combifunction(self, func, *args, **kwargs):
        self.combifunctions.append((func, args, kwargs))

    def combiaction(self):
        for func, args, kwargs in self.combifunctions:
            func(*args, **kwargs)
            print("Item combiAction Function triggered in position: ", self.position)

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
    
    def stash(self, inventory, room=None):
        inventory.release_slots(self)
        if self.stashed:
            # just reposition the item in the inventory
            pos = inventory.get_available_slots(self)
            self.rect.topleft = pos
            self.position = pygame.Vector2(pos)
            return
        if self.allow_destroy:
            print("Item Name: ", self.name, " could be destroyed")
            if self.selfdestruct:
                print("Item Name: ", self.name, " is selfdestructable")
                self.unstash(inventory)
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
        print("Item Name stashed: ", self.name)
        print("Item stashed: ", self.name)
        print("Inventory items: ", inventory.items)

    def unstash(self, inventory):
        #del inventory.items[self.id]
        self.stashed = False
        inventory.release_slots(self)
        #self.position = self.original_position
        #self.rect.topleft = self.original_position
        print("Item unstashed: ", self.name)
        print("Inventory items: ", inventory.items)

    def add_description(self, description_text, description_sound):
        self.description_sound = description_sound
        self.description_text = description_text

    def speak_description(self):
        line = self.description_sound
        print(line)
        sound = pygame.mixer.Sound(line)
        pygame.mixer.Sound.play(sound)

    def talk_description(self, room):
        SPEECHFONT = pygame.font.Font(SPEECH_FONT, SPEECH_SIZE)
        #dialogbox.state = self
        #dialogbox.room = room
        dialbox = DialogBox(room, time.time())
        dialbox.state = self
        dialbox.room = room
        line = self.description_text
        print("Item Describe Talking: ", self.name, "dialog:", line)
        text = SPEECHFONT.render(line, True, BLUE)
        #i shouldn't re-adjust the rect but rather use a player's or narrator's dialogbox
        #dialogbox.rect = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, 0)
        #dialogbox.surface = text
        dialbox.rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, 0)
        dialbox.surface = text

    def describe(self, room):
        print("Item right-clicked: ", self.name)
        self.speak_description()
        self.talk_description(room)

    def add_combination(self, other):
        if not isinstance(other, Item):
            print("Cannot combine with non-item object.")
            return
        if self.name == other.name:
            print("will not attempt to combine the same item: " + self.name + other.name)
            raise ValueError("Cannot combine the same item.")
            return
        self.combinable_items.append(other)
        other.combinable_items.append(self)
        print(f"Added combination: {self.name} with {other.name}")

    def combine(self, other):
        if not isinstance(other, Item):
            print("Cannot combine with non-item object.")
            return
        if self.name == other.name:
            print("will not attempt to combine the same item: " + self.name + " " +  other.name)
            return
        print("Items attmpted to combine:" + self.name + " and " + other.name)
        if other not in self.combinable_items:
            print(f"{other.name} is not combinable with {self.name}.")
            return
        self.combiaction()
        other.combiaction()
        print(f"Combined {self.name} with {other.name}.")
        
    