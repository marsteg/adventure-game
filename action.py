from rectshape import *
from constants import *
from actionfuncs import *

class Action(RectShape):
    _id_counter = 1
    containers = []
    def __init__(self, left, top, width, height, image, name, locked, key):
        super().__init__(left, top, width, height, image)  
        self.rotation = 0
        self.id = Action._id_counter
        Action._id_counter += 1
        self.position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.imagepath = image
        #self.image = pygame.image.load(self.imagepath)
        #self.image = pygame.transform.scale(self.image, (width, height))
        self.name = name
        self.locked = locked
        self.state = ""
        self.key = key
        self.functions = []
        
        
    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def draw(self, screen):
        pygame.draw.rect(screen, "green", self.rect)
        self.image = pygame.image.load(self.imagepath)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        screen.blit(self.image, self.rect)

    def shine(self, screen):
        shiner = pygame.Surface((self.rect.width, self.rect.height))
        shiner.fill((255, 255, 255))
        shiner.set_alpha(100)
        screen.blit(shiner, self.rect.topleft)

    def update(self, dt):
        pass # check for "locked" condition?

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    
    def action(self):
        if self.locked:
            print("Button is locked")
            return
        for func, args, kwargs in self.functions:
            func(*args, **kwargs)
            print("Action Function triggered in position: ", self.position)
        
    def unlock(self, key, inventory):
        if key != self.key:
            print("Wrong key")
            return
        print("Door unlocked: ", self.locked)
        self.locked = False
        self.action()
        #key.stash(inventory)