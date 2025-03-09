from rectshape import *
from constants import *

class Door(RectShape):
    _id_counter = 1
    containers = []
    def __init__(self, left, top, width, height, image, target_room, locked):
        super().__init__(left, top, width, height, image)  
        self.rotation = 0
        self.id = Door._id_counter
        Door._id_counter += 1
        self.position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.target_room = target_room
        self.locked = False
        

    def draw(self, screen):
        pygame.draw.rect(screen, "purple", self.rect)
        screen.blit(self.image, self.rect)

    def update(self, dt):
        pass # check for "locked" condition?

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    