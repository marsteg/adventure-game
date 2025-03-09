import pygame
import random
from constants import *


class Room(pygame.sprite.Sprite):
    _id_counter = 1
    containers = []
    edges = [
        (pygame.Vector2(0, -1), lambda x: pygame.Vector2(x, 0)),
        (pygame.Vector2(1, 0), lambda y: pygame.Vector2(SCREEN_WIDTH, y)),
        (pygame.Vector2(0, 1), lambda x: pygame.Vector2(x, SCREEN_HEIGHT)),
        (pygame.Vector2(-1, 0), lambda y: pygame.Vector2(0, y))
    ]

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT-INVENTORY_HEIGHT)
        self.spawn_timer = 0.0
        self.id = Room._id_counter
        Room._id_counter += 1
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT-INVENTORY_HEIGHT))
        self.doors = []
        self.items = []
        

    def draw(self, screen):
        pygame.draw.rect(screen, "purple", self.rect)
        screen.blit(self.image, self.rect)
        for door in self.doors:
            door.draw(screen)
        for item in self.items:
            item.draw(screen)

    def spawn(self, radius, position, velocity):
        pass # sub-classes must override - could be useful for minigame style rooms
        #asteroid = Asteroid(position.x, position.y, radius)
        #print("spawning asteroid ", asteroid.id, " at position: ", position)
        #asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        pass