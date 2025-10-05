from rectshape import *
from constants import *

def load_image(path, width, height):
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (width, height))
    image.set_colorkey(WHITE)
    image.convert_alpha()
    return image

class Player(pygame.sprite.Sprite):
    _id_counter = 1
    containers = []
    def __init__(self, left, top, width, height, image, name):
        super().__init__()  
        self.rotation = 0
        self.pos = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        #self.defaultimage = pygame.image.load(image).convert_alpha()
        #self.defaultimage = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (width, height))
        self.defaultimage = load_image(image, width, height)
        self.name = name
        #self.set_target((0, 0))
        self.speed = 5
        self.target = self.pos
        self.rightsprites = []
        self.leftsprites = []
        self.current_sprite = 0
        self.rightsprites.append(load_image("assets/player/walking/right0.png", width, height))
        self.rightsprites.append(load_image("assets/player/walking/right1.png", width, height))
        self.rightsprites.append(load_image("assets/player/walking/right2.png", width, height))
        self.rightsprites.append(load_image("assets/player/walking/right3.png", width, height))
        self.rightsprites.append(load_image("assets/player/walking/right4.png", width, height))
        self.rightsprites.append(load_image("assets/player/walking/right5.png", width, height))
        self.leftsprites.append(load_image("assets/player/walking/left0.png", width, height))
        self.leftsprites.append(load_image("assets/player/walking/left1.png", width, height))
        self.leftsprites.append(load_image("assets/player/walking/left2.png", width, height))
        self.leftsprites.append(load_image("assets/player/walking/left3.png", width, height))
        self.leftsprites.append(load_image("assets/player/walking/left4.png", width, height))
        self.leftsprites.append(load_image("assets/player/walking/left5.png", width, height))
        self.image = self.rightsprites[self.current_sprite]

    def set_target(self, pos):
        px, py = pos
        newpos = px - self.rect.width // 2, py - self.rect.height 
        self.target = pygame.Vector2(newpos)

    def clear_target(self):
        self.target = self.pos

    def draw(self, screen):
        #pygame.draw.rect(screen, "purple", self.rect)
        screen.blit(self.image, self.rect)

    def update(self, dt):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.rightsprites):
            self.current_sprite = 0
        if self.target == self.pos:
            self.image = self.defaultimage
        elif self.target[0] > self.pos[0]:
            self.image = self.rightsprites[int(self.current_sprite)]
        elif self.target[0] < self.pos[0]:
            self.image = self.leftsprites[int(self.current_sprite)]
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
        
