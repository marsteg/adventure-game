from constants import *
from room import *
from door import *
from action import *
from npc import *
from item import *
import pygame
import time


class QueuedInteraction:
    def __init__(self, target, action_callable, args=(), description=""):
        self.target = target
        self.action_callable = action_callable
        self.args = args
        self.description = description
