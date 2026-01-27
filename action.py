import pygame
import time

from rectshape import RectShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SPEECH_FONT, SPEECH_SIZE, BLUE
from dialogbox import DialogBox


class Action(RectShape):
    _id_counter = 1
    containers = []
    _image_cache = {}  # Cache for loaded images

    def __init__(self, left, top, width, height, image, name, locked, key):
        super().__init__(left, top, width, height, image)
        self.rotation = 0
        self.id = Action._id_counter
        Action._id_counter += 1
        self.position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.imagepath = image
        self.name = name
        self.locked = locked
        self.state = ""
        self.key = key
        self.functions = []
        self._cached_image = None
        self._cached_imagepath = None
        self._load_image()

    def _load_image(self):
        """Load and cache the image. Only reload if path changed."""
        if self._cached_imagepath != self.imagepath:
            cache_key = (self.imagepath, self.width, self.height)
            if cache_key not in Action._image_cache:
                img = pygame.image.load(self.imagepath).convert_alpha()
                img = pygame.transform.scale(img, (self.width, self.height))
                Action._image_cache[cache_key] = img
            self._cached_image = Action._image_cache[cache_key]
            self._cached_imagepath = self.imagepath

    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def draw(self, screen):
        self._load_image()
        screen.blit(self._cached_image, self.rect)

    def shine(self, screen):
        shiner = pygame.Surface((self.rect.width, self.rect.height))
        shiner.fill((255, 255, 255))
        shiner.set_alpha(100)
        screen.blit(shiner, self.rect.topleft)

    def update(self, dt):
        pass

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def action(self):
        if self.locked:
            print("Action Object is locked")
            return
        for func, args, kwargs in self.functions:
            func(*args, **kwargs)
            print("Action Function triggered in position: ", self.position)

    def unlock(self, key, inventory):
        if self.key is None:
            print("No key required")
            return
        if key != self.key:
            print("Wrong key")
            return
        print("Action unlocked: ", self.locked)
        self.locked = False
        self.action()

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
        sound = pygame.mixer.Sound(line)
        pygame.mixer.Sound.play(sound)

    def talk_description(self, room):
        speech_font = pygame.font.Font(SPEECH_FONT, SPEECH_SIZE)
        dialbox = DialogBox(room, time.time())
        dialbox.state = self
        dialbox.room = room

        if self.locked:
            line = self.description_text_locked
        else:
            line = self.description_text_unlocked

        print("Action Describe Talking: ", self.name, "dialog:", line)
        text = speech_font.render(line, True, BLUE)
        dialbox.rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, 0)
        dialbox.surface = text
        # Store text for new renderer
        dialbox.dialog_text = line
        dialbox.speaker_name = ""

    def describe(self, room):
        print("Action right-clicked: ", self.name)
        self.speak_description()
        self.talk_description(room)
