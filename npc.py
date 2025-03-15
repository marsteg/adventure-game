from rectshape import *
from constants import *

class NPC(RectShape):
    _id_counter = 1
    containers = []
    NPCs = {}
    def __init__(self, left, top, width, height, image, name, locked, key, text):
        super().__init__(left, top, width, height, image)  
        self.rotation = 0
        self.id = NPC._id_counter
        NPC._id_counter += 1
        self.position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.name = name
        self.functions = []
        self.locked = locked
        self.key = key
        self.active_dialog = text
        NPC.NPCs[self.id] = self
        
    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def draw(self, screen):
        #pygame.draw.rect(screen, "purple", self.rect)
        screen.blit(self.image, self.rect)

    def update(self, dt):
        pass # check for "locked" condition?

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    
    def action(self):
        if self.locked:
            print("NPC is locked")
            return
        for func, args, kwargs in self.functions:
            func(*args, **kwargs)
            print("Action Function triggered in position: ", self.position)
    
    def unlock(self, key, inventory):
        if key != self.key:
            print("Wrong key")
            return
        print("NPC unlocked: ", self.locked)
        self.locked = False
        key.allow_destroy = True
        self.action()

    def talk(self, dialog):
        print("NPC Talking: ", self.name)
        dialog.state = self
        font = pygame.font.Font('freesansbold.ttf', 25)
        text = font.render(self.active_dialog, True, (255,255,255))
        dialog.surface = text

    