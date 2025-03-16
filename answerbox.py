import pygame
from inventory import *
from item import *
from room import *
from door import *
from rectshape import *
from constants import *


class AnswerBox(pygame.sprite.Sprite):
    _id_counter = 1
    containers = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - INVENTORY_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT)
        self.id = AnswerBox._id_counter
        AnswerBox._id_counter += 1
        self.state = None
        self.functions = []
        self.answers = {}

    def draw(self, screen):
        answerbox = pygame.draw.rect(screen, "blue", self.rect)
        screen.fill("blue", answerbox)
        #screen.blit(self.surface, self.rect)
        if len(self.answers) > 0:
            for answer in self.answers.values():
                screen.blit(answer.surface, answer.rect)
        
    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def add_answer(self, answer):
        self.answers[answer.answer] = answer

    def update(self, dt):
        pass

'''
- NPCs
	- actual conversations
		- text currently stays 3 seconds - clicking should skip to the next line
        - text should be positioned relative to the character speaking
		- each line of speech should have a configurable talking time (and a default value)
		- active dialog (dialog state of NPC) answers could change based on:
			- specific replies chosen (should execute actionfunc)
			- actions executed (actionfunc to change actve dialog of npc)
        - Speech Lines are objects themselves
            - Speech Lines have:
                - text
                - duration
                - speaker (NPC or player)
                - color
                - position
                - trigger next answer lines
            - Answer Lines are objects themselves
                - Answer Lines have:
                    - text
                    - actionfuncs
                    - trigger next speech line or exit dialog
		- dialogs should be objects themselves
			- dialogs have:
                - a "state" of the current dialog
				- can change the state of the current "dialog" of an NPC (trigger change to next one (via actionfunc?))
				- Answer Lines:
                    - List of answers which need to trigger speech lines and actions if desired
				- should make the rest of the screen unclickable"
			- NPC needs a state of the current active dialog
	
'''