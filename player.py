from rectshape import *
from constants import *


class Player(pygame.sprite.Sprite):
    _id_counter = 1
    containers = []
    def __init__(self, left, top, width, height, image, name):
        super().__init__()  
        self.rotation = 0
        self.pos = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.name = name
        #self.set_target((0, 0))
        self.speed = 10
        self.target = self.pos

    def set_target(self, pos):
        px, py = pos
        newpos = px - self.rect.width // 2, py - self.rect.height 
        self.target = pygame.Vector2(newpos)

    def draw(self, screen):
        #pygame.draw.rect(screen, "purple", self.rect)
        screen.blit(self.image, self.rect)

    def update(self, dt):
        move = self.target - self.pos
        move_length = move.length()

        if move_length < self.speed:
            self.pos = self.target
        elif move_length != 0:
            move.normalize_ip()
            move = move * self.speed
            self.pos += move

        self.rect.topleft = list(int(v) for v in self.pos)   

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
        
