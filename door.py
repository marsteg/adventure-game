from rectshape import *
from constants import *

class Door(RectShape):
    _id_counter = 1
    containers = []
    def __init__(self, left, top, width, height, image, name, target_room, locked, key):
        super().__init__(left, top, width, height, image)  
        self.rotation = 0
        self.id = Door._id_counter
        Door._id_counter += 1
        self.position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.target_room = target_room
        self.name = name
        self.locked = locked
        self.key = key
        

    def draw(self, screen):
        pygame.draw.rect(screen, "purple", self.rect)
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
    
    def unlock(self, key, inventory):
        if key != self.key:
            print("Wrong key")
            return
        print("Door unlocked: ", self.locked)
        self.locked = False
        key.allow_destroy = True
        #key.stash(inventory)
    