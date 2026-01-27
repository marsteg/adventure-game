import pygame
import time

from rectshape import RectShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SPEECH_FONT, SPEECH_SIZE, BLUE
from dialogbox import DialogBox


class Item(RectShape):
    _id_counter = 1
    containers = []
    items = {}

    def __init__(self, left, top, width, height, image, name, self_destruct=False):
        super().__init__(left, top, width, height, image)
        self.rotation = 0
        self.position = pygame.Vector2(left, top)
        self.original_position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.imagepath = image
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.name = name
        self.id = Item._id_counter
        Item._id_counter += 1
        self.self_destruct = self_destruct
        Item.items[self.name] = self
        self.functions = []
        self.stashed = False
        self.allow_destroy = False
        self.combinable_items = []
        self.combifunctions = []

    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def action(self):
        for func, args, kwargs in self.functions:
            func(*args, **kwargs)
            print("Item Action Function triggered in position: ", self.position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def add_combifunction(self, func, *args, **kwargs):
        self.combifunctions.append((func, args, kwargs))

    def combiaction(self):
        for func, args, kwargs in self.combifunctions:
            func(*args, **kwargs)
            print("Item combiAction Function triggered in position: ", self.position)

    def update(self, dt):
        pass

    def kill(self, inventory, rooms):
        print(f"Attempting Item destroy: {self.name} on position: {self.position}, "
              f"self_destruct: {self.self_destruct}, allow_destroy: {self.allow_destroy}")

        if self.self_destruct and self.allow_destroy:
            if self.name in inventory.items:
                if self == inventory.items[self.name]:
                    del inventory.items[self.name]
            for room in rooms.values():
                if self.name in room.items:
                    if self == room.items[self.name]:
                        del room.items[self.name]
                        inventory.release_slots(self)
                        print("Item removed from room: ", room.name)
                        pygame.sprite.Sprite.kill(self)
        else:
            self.stash(inventory)

    def move_ip(self, rel):
        self.rect.move_ip(rel)
        self.position = pygame.Vector2(self.rect.topleft)

    def stash(self, inventory, room=None):
        inventory.release_slots(self)
        if self.stashed:
            # Just reposition the item in the inventory
            pos = inventory.get_available_slots(self)
            if pos:
                self.rect.topleft = pos
                self.position = pygame.Vector2(pos)
            return

        if self.allow_destroy and self.self_destruct:
            print(f"Item {self.name} is self-destructable")
            self.unstash(inventory)
            return

        inventory.items[self.name] = self
        self.stashed = True

        if room is not None and self.name in room.items:
            if self == room.items[self.name]:
                del room.items[self.name]
                print("Item removed from room: ", room.name)

        pos = inventory.get_available_slots(self)
        if pos:
            self.rect.topleft = pos
            self.position = pygame.Vector2(pos)
        print(f"Item stashed: {self.name}")

    def unstash(self, inventory):
        self.stashed = False
        inventory.release_slots(self)
        print(f"Item unstashed: {self.name}")

    def add_description(self, description_text, description_sound):
        self.description_sound = description_sound
        self.description_text = description_text

    def speak_description(self):
        print(self.description_sound)
        sound = pygame.mixer.Sound(self.description_sound)
        pygame.mixer.Sound.play(sound)

    def talk_description(self, room):
        speech_font = pygame.font.Font(SPEECH_FONT, SPEECH_SIZE)
        dialbox = DialogBox(room, time.time())
        dialbox.state = self
        dialbox.room = room

        print("Item Describe Talking: ", self.name, "dialog:", self.description_text)
        text = speech_font.render(self.description_text, True, BLUE)
        dialbox.rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, 0)
        dialbox.surface = text
        # Store text for new renderer
        dialbox.dialog_text = self.description_text
        dialbox.speaker_name = ""

    def describe(self, room):
        print("Item right-clicked: ", self.name)
        self.speak_description()
        self.talk_description(room)

    def add_combination(self, other):
        if not isinstance(other, Item):
            print("Cannot combine with non-item object.")
            return
        if self.name == other.name:
            print(f"Will not attempt to combine the same item: {self.name}")
            return
        self.combinable_items.append(other)
        other.combinable_items.append(self)
        print(f"Added combination: {self.name} with {other.name}")

    def combine(self, other):
        if not isinstance(other, Item):
            print("Cannot combine with non-item object.")
            return
        if self.name == other.name:
            print(f"Will not attempt to combine the same item: {self.name}")
            return
        print(f"Items attempted to combine: {self.name} and {other.name}")
        if other not in self.combinable_items:
            print(f"{other.name} is not combinable with {self.name}.")
            return
        print(f"Combining {self.name} with {other.name}.")
        self.combiaction()
        other.combiaction()
        print(f"Combined {self.name} with {other.name}.")
