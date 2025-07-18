import pygame
import random
from constants import *
from dialogbox import *


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

    def __init__(self, image, name, music):
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
        self.name = name
        self.music = music
        Room.rooms[self.name] = self
        

    def draw(self, screen, inventory, answerbox):
        pygame.draw.rect(screen, "purple", self.rect)
        screen.blit(self.image, self.rect)
        
        for door in self.doors.values():
            door.draw(screen)
        for action in self.actions.values():
            action.draw(screen)
        for npc in self.npcs.values():
            npc.draw(screen)
        for item in self.items.values():
            item.draw(screen)
        for dialogbox in DialogBox.dialogboxes:
            if dialogbox.room == self:
                dialogbox.draw(screen)
        inventory.draw(screen)
        if answerbox.state != None:
            answerbox.draw(screen)
        else:
            for inventory_item in inventory.items.values():
                inventory_item.draw(screen)

    def play(self):
        print("Playing music: ", self.music)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.set_volume(BACKGROUND_VOLUME)
        pygame.mixer.music.play(-1,0.0)
        
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

    def update(self, dt):
        self.spawn_timer += dt
        pass