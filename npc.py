from rectshape import *
from constants import *
from answer import *
from dialogfuncs import *
from actionfuncs import *
import yaml


class NPC(RectShape):
    _id_counter = 1
    containers = []
    NPCs = {}
    def __init__(self, left, top, width, height, image, name, locked, key, speechcolor, dialogfile):
        super().__init__(left, top, width, height, image)  
        self.rotation = 0
        self.id = NPC._id_counter
        NPC._id_counter += 1
        self.position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.name = name
        self.functions = []
        self.locked = locked
        self.key = key
        self.active_dialog = "start"
        self.dialogfile = dialogfile
        self.dialog = self.load_dialog()
        self.speechcolor = speechcolor
        NPC.NPCs[self.id] = self
        
    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def draw(self, screen):
        #pygame.draw.rect(screen, "purple", self.rect)
        screen.blit(self.image, self.rect)

    def update(self, dt):
        pass # check for "locked" condition?

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    
    def action(self):
        if self.locked:
            print("NPC is locked")
            return
        for func, args, kwargs in self.functions:
            func(*args, **kwargs)
            print("Action Function triggered in position: ", self.position)
    
    def unlock(self, key, inventory):
        if self.key == None:
            print("No key required")
            return
        if key.name != self.key.name:
            print("Wrong key")
            return
        print("NPC unlocked: ", self.locked)
        self.locked = False
        key.allow_destroy = True
        self.action()

    def shine(self, screen):
        shiner = pygame.Surface((self.rect.width, self.rect.height))
        shiner.fill((255, 255, 255))
        shiner.set_alpha(100)
        screen.blit(shiner, self.rect.topleft)

    def load_dialog(self):
        with open(self.dialogfile, 'r') as file:
            dialog = yaml.safe_load(file)
            print("Dialog loaded: ", dialog)
            return dialog
        
    def shutup(self):
        self.active_dialog = "bye"

    def speak(self):
        voiceline = pygame.mixer.Sound(self.dialog[self.active_dialog]["sound"])
        pygame.mixer.Sound.play(voiceline)

    def speak_description(self):
        if self.locked:
            line = self.dialog["description"]["locked"]["sound"]
            print(line)
            sound = pygame.mixer.Sound(line)
            pygame.mixer.Sound.play(sound)
        else:
            line = self.dialog["description"]["unlocked"]["sound"]
            print(line)
            sound = pygame.mixer.Sound(line)
            pygame.mixer.Sound.play(sound)

    def talk_description(self, room):
        SPEECHFONT = pygame.font.Font(SPEECH_FONT, SPEECH_SIZE)
        dialbox = DialogBox(room, time.time())
        dialbox.state = self
        dialbox.room = room
        if self.locked:
            line = self.dialog["description"]["locked"]["line"]
            print("Describe Talking: ", self.name, "dialog:", line)
            text = SPEECHFONT.render(line, True, BLUE)
            #i shouldn't re-adjust the rect but rather use a player's or narrator's dialogbox
            dialbox.rect = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, 0)
            dialbox.surface = text
            print("Dialogbox worked")
        else:
            line = self.dialog["description"]["unlocked"]["line"]
            print("Describe Talking: ", self.name, "dialog:", line)
            text = SPEECHFONT.render(line, True, BLUE)
            #i shouldn't re-adjust the rect but rather use a player's or narrator's dialogbox
            dialbox.rect = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, 0)
            dialbox.surface = text
            print("Dialogbox worked")

    def describe(self, room):
        print("NPC right-clicked: ", self.name)
        self.speak_description()
        self.talk_description(room)

    # talk should only ensure the NPC talks and trigger an own dialogbox rather than using a shared one
    def talk(self, room, inventory, answerbox):
        self.timer = time.time()
        SPEECHFONT = pygame.font.Font(SPEECH_FONT, SPEECH_SIZE)
        print("NPC Talking: ", self.name)
        dialbox = DialogBox(room, time.time())
        dialbox.state = self
        dialbox.room = room
        self.speak()
        # cater for the case where the speaker is another NPC
        speaker = self.dialog[self.active_dialog]["speaker"]
        for npc in room.npcs.values():
            if npc.name == speaker:
                speaker = npc
                break
        if isinstance(speaker, str):
            speaker = self
        print("NPC Talking: ", self.name, "dialog:", self.dialog[self.active_dialog]["line"])
        text = SPEECHFONT.render(self.dialog[self.active_dialog]["line"], True, speaker.speechcolor)
        #i shouldn't re-adjust the rect but rather use a position relative to the speaker
        if SCREEN_WIDTH // 2 < speaker.rect.left:
            dialbox.rect = pygame.Rect(speaker.rect.left - SCREEN_WIDTH // 3, speaker.rect.top + at_percentage_height(5), SCREEN_WIDTH // 2, 0)
        else:
            dialbox.rect = pygame.Rect(speaker.rect.left + SCREEN_WIDTH // 3, speaker.rect.top + at_percentage_height(5), SCREEN_WIDTH // 2, 0)
        dialbox.surface = text
        # check if the dialog unlocks something
        if "unlock" in self.dialog[self.active_dialog]:
            print("Unlocking is in yaml")
            if self.dialog[self.active_dialog]["unlock"] == True:
                print("calling unlock function")
                self.unlock(self.key, inventory)
        # check if dialog has an exit
        if "exit" in self.dialog[self.active_dialog]:
            if "ExitDialog" in self.dialog[self.active_dialog]["exit"]:
                answerbox.answers = {}
                answerbox.state = None
                answerbox.room = None
                self.active_dialog = self.dialog[self.active_dialog]["exit"]["ExitDialog"]
                return
        
        # done, talking; building answers now.
        if "answers" in self.dialog[self.active_dialog]:
            # clear old answers:
            answerbox.answers = {}
            if self.dialog[self.active_dialog]["answers"] != None:
                answerbox.state = self.dialog[self.active_dialog]["answers"]
                answerbox.room = room
            # generate answerboxes
            if len(self.dialog[self.active_dialog]["answers"]) > 0:
                for i, answer in enumerate(self.dialog[self.active_dialog]["answers"]):
                    a = Answer(answer["line"], i)
                    answerbox.add_answer(a)
                    for num, action in enumerate(self.dialog[self.active_dialog]["answers"][i]["actionfuncs"]):
                        for k,v in action.items():
                            func = globals().get(k)
                            if func:
                                if isinstance(v, list):
                                    #func_args = (*v, room, self, inventory, answerbox, dialogbox)
                                    func_args = (*v, room, self, inventory, answerbox)
                                else:
                                    func_args = (v, room, self, inventory, answerbox)
                                    #func_args = (v, room, self, inventory, answerbox, dialogbox)
                                a.add_dialogfunction(func, *func_args)
                                print("funcs added: ", func, func_args)
                                print("Action added: ", action)
                                print("Function: ", func)
                                print("Arguments: ", v)
                            else:
                                print(f"Function {k} not found.")
                        a.npc = self
