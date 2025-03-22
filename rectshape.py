import pygame

# Base class for game objects
class RectShape(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height, image):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        #self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.image = image
     

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def kill(self, arg1, arg2):
        # sub-classes must override
        pass

    def collides_with(self, other):
        return self.rect.colliderect(other.rect)

    
    