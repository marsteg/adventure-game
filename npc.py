from rectshape import *
from constants import *
from answer import *
from dialogfuncs import *
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
        #self.active_dialog = text
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
        if key != self.key:
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

    # talk should only ensure the NPC talks and trigger the answerbox rather than generate it
    def talk(self, room, inventory, dialogbox, answerbox):
        SPEECHFONT = pygame.font.Font(SPEECH_FONT, SPEECH_SIZE)
        print("NPC Talking: ", self.name)
        dialogbox.state = self
        dialogbox.room = room
        speaker = self.dialog[self.active_dialog]["speaker"]
        for npc in NPC.NPCs.values():
            if npc.name == speaker:
                speaker = npc
                break
        if isinstance(speaker, str):
            speaker = self
        print("NPC Talking: ", self.name, "dialog:", self.dialog[self.active_dialog]["line"])
        text = SPEECHFONT.render(self.dialog[self.active_dialog]["line"], True, speaker.speechcolor)
        #text = font.render(self.dialog[self.active_dialog]["line"], True, self.speechcolor)
        dialogbox.rect = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, 0)
        dialogbox.surface = text
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
                self.active_dialog = self.dialog[self.active_dialog]["exit"]["ExitDialog"]
                #dialogbox.state = None
                #ExitDialog(self.dialog[self.active_dialog]["exit"]["ExitDialog"], room, self, inventory, answerbox, dialogbox)
                return
        
        # done, answering.
        if "answers" in self.dialog[self.active_dialog]:
            # clear old answers:
            answerbox.answers = {}
            if self.dialog[self.active_dialog]["answers"] != None:
                answerbox.state = self.dialog[self.active_dialog]["answers"]
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
                                    func_args = (*v, room, self, inventory, answerbox, dialogbox)
                                else:
                                    func_args = (v, room, self, inventory, answerbox, dialogbox)
                                a.add_dialogfunction(func, *func_args)
                                print("funcs added: ", func, func_args)
                                print("Action added: ", action)
                                print("Function: ", func)
                                print("Arguments: ", v)
                                # add dialogfunction to trigger dialogbox (timer reset + state change)
                            else:
                                print(f"Function {k} not found.")
                        a.npc = self
