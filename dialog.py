import pygame
import random
from constants import *


class Dialog(None):
    _id_counter = 1
    def __init__(self):
        self.id = Dialog._id_counter
        Dialog._id_counter += 1
        self.state = None
        self.functions = []
        
        
    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def update(self, dt):
        pass


class SpeechLine(None):
    _id_counter = 1
    def __init__(self, text, duration, speaker, next_line):
        self.id = SpeechLine._id_counter
        SpeechLine._id_counter += 1
        self.text = text
        self.duration = duration
        self.speaker = speaker
        self.color = speaker.speechcolor
        self.position = speaker.rect.topleft
        self.next_line = next_line

    def draw(self, screen):
        pass

    def update(self, dt):
        pass
    

class AnswerLines(None):
    _id_counter = 1
    def __init__(self, text, duration, speaker, next_line):
        self.id = AnswerLines._id_counter
        AnswerLines._id_counter += 1
        self.answers = []
        self.functions = []  
        
    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def draw(self, screen):
        pass

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