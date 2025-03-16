from rectshape import *
from constants import *
from actionfuncs import *

class Answer(RectShape):
    _id_counter = 1
    containers = []
    def __init__(self, answer, top):
        SPEECHFONT = pygame.font.Font(SPEECH_FONT, SPEECH_SIZE)
        #self.id = Answer._id_counter
        #Answer._id_counter += 1
        self.surface = SPEECHFONT.render(answer, True, WHITE)
        self.left = 10
        self.height = SPEECH_SIZE
        self.top = (SCREEN_HEIGHT - INVENTORY_HEIGHT + 5) + (top * 25)
        self.width = self.surface.get_width()
        super().__init__(self.left, self.top, self.width, self.height, "image")
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.rect.topleft = (self.left, self.top)
        self.functions = []
        self.position = pygame.Vector2(self.left, self.top) 
        self.answer = answer
        
   
        
    def add_dialogfunction(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))
        
    def draw(self, screen):
        pass

    def update(self, dt):
        pass 

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    
    def action(self):
        for func, args, kwargs in self.functions:
            func(*args, **kwargs)
            print("Action Function triggered in position: ", self.position)