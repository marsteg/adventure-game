import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_HEIGHT, at_percentage_width


class Inventory(pygame.sprite.Sprite):
    containers = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - INVENTORY_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT)
        self.items = {}  # Instance variable, not class variable
        self.slots = {}  # Instance variable, not class variable
        self._init_slots()

    def _init_slots(self):
        """Initialize inventory slots."""
        for i in range(20):
            self.slots[i] = {
                "pos": (at_percentage_width(i * 5) + 5, SCREEN_HEIGHT - INVENTORY_HEIGHT + 5),
                "item": None
            }

    def draw(self, screen):
        inv = pygame.draw.rect(screen, "brown", self.rect)
        screen.fill("brown", inv)
        for item in self.items.values():
            item.draw(screen)

    def update(self, dt):
        pass

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def get_available_slots(self, item):
        """Find and assign an available slot for an item."""
        for slot in self.slots.values():
            if slot["item"] is None:
                slot["item"] = item
                return slot["pos"]
        return None

    def release_slots(self, item):
        """Release the slot occupied by an item."""
        for slot in self.slots.values():
            if slot["item"] == item:
                slot["item"] = None
                return
