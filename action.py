from rectshape import *
from constants import *
from actionfuncs import *
import time

class Action(RectShape):
    _id_counter = 1
    containers = []
    def __init__(self, left, top, width, height, image, name, locked, key):
        super().__init__(left, top, width, height, image)  
        self.rotation = 0
        self.id = Action._id_counter
        Action._id_counter += 1
        self.position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.imagepath = image
        #self.image = pygame.image.load(self.imagepath)
        #self.image = pygame.transform.scale(self.image, (width, height))
        self.name = name
        self.locked = locked
        self.state = ""
        self.key = key
        self.functions = []
        
        
    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def draw(self, screen):
        pygame.draw.rect(screen, "green", self.rect)
        self.image = pygame.image.load(self.imagepath)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        screen.blit(self.image, self.rect)

    def shine(self, screen):
        shiner = pygame.Surface((self.rect.width, self.rect.height))
        shiner.fill((255, 255, 255))
        shiner.set_alpha(100)
        screen.blit(shiner, self.rect.topleft)

    def update(self, dt):
        pass # check for "locked" condition?

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
        if self.key == None:
            print("No key required")
            return
        if key != self.key:
            print("Wrong key")
            return
        print("Door unlocked: ", self.locked)
        self.locked = False
        self.action()
        #key.stash(inventory)

    def add_description(self, description_text_locked, description_text_unlocked, description_sound_locked, description_sound_unlocked):
        self.description_text_locked = description_text_locked
        self.description_text_unlocked = description_text_unlocked
        self.description_sound_locked = description_sound_locked
        self.description_sound_unlocked = description_sound_unlocked


    def speak_description(self):
        if self.locked:
            line = self.description_sound_locked
            print(line)
            sound = pygame.mixer.Sound(line)
            pygame.mixer.Sound.play(sound)
        else:
            line = self.description_sound_unlocked
            print(line)
            sound = pygame.mixer.Sound(line)
            pygame.mixer.Sound.play(sound)

    def talk_description(self, room):
        SPEECHFONT = pygame.font.Font(SPEECH_FONT, SPEECH_SIZE)
        #dialogbox.state = self
        #dialogbox.room = room
        dialbox = DialogBox(room, time.time())
        dialbox.state = self
        dialbox.room = room
        if self.locked:
            line = self.description_text_locked
            print("Action Describe Talking: ", self.name, "dialog:", line)
            text = SPEECHFONT.render(line, True, BLUE)
            #i shouldn't re-adjust the rect but rather use a player's or narrator's dialogbox
            dialbox.rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, 0)
            dialbox.surface = text
        else:
            line = self.description_text_unlocked
            print("Action Describe Talking: ", self.name, "dialog:", line)
            text = SPEECHFONT.render(line, True, BLUE)
            #i shouldn't re-adjust the rect but rather use a player's or narrator's dialogbox
            dialbox.rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, 0)
            dialbox.surface = text

    def describe(self, room):
        print("Action right-clicked: ", self.name)
        self.speak_description()
        self.talk_description(room)
