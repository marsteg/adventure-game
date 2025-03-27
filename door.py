from rectshape import *
from constants import *
from dialogbox import *
import time

class Door(RectShape):
    _id_counter = 1
    containers = []
    def __init__(self, left, top, width, height, image, name, target_room, locked, key):
        super().__init__(left, top, width, height, image)  
        self.rotation = 0
        self.id = Door._id_counter
        Door._id_counter += 1
        self.position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.target_room = target_room
        self.name = name
        self.timer = 0
        self.locked = locked
        self.key = key
        

    def draw(self, screen):
        pygame.draw.rect(screen, "purple", self.rect)
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
    
    def unlock(self, key):
        if self.key == None:
            print("No key required")
            return
        if key != self.key:
            print("Wrong key")
            return
        print("Door unlocked: ", self.locked)
        self.locked = False
        key.allow_destroy = True
        sound = pygame.mixer.Sound("assets/sounds/actions/door_unlock.wav")
        pygame.mixer.Sound.play(sound)
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
            print("Door Describe Talking: ", self.name, "dialog:", line)
            text = SPEECHFONT.render(line, True, BLUE)
            #i shouldn't re-adjust the rect but rather use a player's or narrator's dialogbox
            dialbox.rect = pygame.Rect(SCREEN_WIDTH // 5, SCREEN_HEIGHT // 5, SCREEN_WIDTH // 2, 0)
            dialbox.surface = text
        else:
            line = self.description_text_unlocked
            print("Door Describe Talking: ", self.name, "dialog:", line)
            text = SPEECHFONT.render(line, True, BLUE)
            #i shouldn't re-adjust the rect but rather use a player's or narrator's dialogbox
            dialbox.rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, 0)
            dialbox.surface = text

    def describe(self, room):
        print("Action right-clicked: ", self.name)
        self.speak_description()
        self.talk_description(room)
