import pygame
import random
from constants import *


class Room(pygame.sprite.Sprite):
    _id_counter = 1
    containers = []
    rooms = {}
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
        self.doors = {}
        self.items = {}
        self.actions = {}
        self.npcs = {}
        Room.rooms[self.id] = self
        

    def draw(self, screen, inventory, dialogbox):
        pygame.draw.rect(screen, "purple", self.rect)
        screen.blit(self.image, self.rect)
        inventory.draw(screen, inventory)
        for door in self.doors.values():
            door.draw(screen)
        for action in self.actions.values():
            action.draw(screen)
        for npc in self.npcs.values():
            npc.draw(screen)
        for item in self.items.values():
            item.draw(screen)
        for inventory_item in inventory.items.values():
            inventory_item.draw(screen)
        if dialogbox.state != None:
            dialogbox.draw(screen)
        
    def shine(self, screen):
        for item in self.items.values():
            item.shine(screen)
        for door in self.doors.values():
            door.shine(screen)
        for action in self.actions.values():
            action.shine(screen)
        for npc in self.npcs.values():
            npc.shine(screen)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def spawn(self, radius, position, velocity):
        pass # sub-classes must override - could be useful for minigame style rooms
        #asteroid = Asteroid(position.x, position.y, radius)
        #print("spawning asteroid ", asteroid.id, " at position: ", position)
        #asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        pass