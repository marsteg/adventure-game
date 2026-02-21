import pygame
import time

from rectshape import RectShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from dialogbox import DialogBox, VoiceManager


class Door(RectShape):
    _id_counter = 1
    containers = []

    def __init__(self, left, top, width, height, image, name, target_room, player_target_position, locked, key):
        super().__init__(left, top, width, height, image)
        self.rotation = 0
        self.id = Door._id_counter
        Door._id_counter += 1
        self.position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        if image == None:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        else:    
            self.image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        self.target_room = target_room
        self.player_target_position = player_target_position
        self.name = name
        self.locked = locked
        self.key = key
        self.functions = []

    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def action(self):
        for func, args, kwargs in self.functions:
            func(*args, **kwargs)
            print("Action Function triggered in position: ", self.position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        pass

    def unlock(self, key):
        if self.key is None:
            print("No key required")
            return
        if key != self.key:
            print("Wrong key")
            return
        print("Door unlocked: ", self.locked)
        self.locked = False
        key.allow_destroy = True
        self.action()
        sound = pygame.mixer.Sound("assets/sounds/actions/door_unlock.wav")
        pygame.mixer.Sound.play(sound)

    def add_description(self, description_text_locked, description_text_unlocked,
                        description_sound_locked, description_sound_unlocked):
        self.description_text_locked = description_text_locked
        self.description_text_unlocked = description_text_unlocked
        self.description_sound_locked = description_sound_locked
        self.description_sound_unlocked = description_sound_unlocked

    def speak_description(self):
        if self.locked:
            line = self.description_sound_locked
        else:
            line = self.description_sound_unlocked
        print(line)
        VoiceManager.play_voice(line)

    def talk_description(self, room):
        dialbox = DialogBox(room, time.time())
        #dialbox.state = self
        dialbox.room = room

        if self.locked:
            line = self.description_text_locked
        else:
            line = self.description_text_unlocked

        print("Door Describe Talking: ", self.name, "dialog:", line)
        # Store text for new renderer
        dialbox.dialog_text = line
        dialbox.speaker_name = ""

    def describe(self, room):
        print("Door right-clicked: ", self.name)
        self.speak_description()
        self.talk_description(room)
