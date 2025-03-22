from inventory import *
from item import *
from room import *
from answer import *
from constants import *
import time


def ResetAnswerBox(answerbox):
    answerbox.state = None
    answerbox.answers = {}
    print("Answerbox reset")

def ExitDialog(new_active_dialog, room, npc, inventory, answerbox, dialogbox):
    print("Exiting dialog: ", npc.name)
    npc.active_dialog = new_active_dialog
    answerbox.answers = {}
    answerbox.state = None
    dialogbox.state = None
    dialogbox.timer = time.time()
    print("Dialog exited")
    
def ChangeDialog(npcString, new_dialog, room, npc, inventory, answerbox, dialogbox):
    if npc.name == npcString:
        npc.active_dialog = new_dialog
        answerbox.state = npc.active_dialog
        dialogbox.state = npc
        dialogbox.timer = time.time()
        npc.talk(room, inventory, dialogbox, answerbox)
        print("Dialog changed to: ", new_dialog)
        return
    else:
        print("NPC not found")

def TakeItemString(itemString, failure_dialog, success_dialog, room, npc, inventory, answerbox, dialogbox):
    # go through the dict of all items and find the one with the same name
    # how should i get the inventory?
    for item in inventory.items.values():
        if item.name == itemString:
            TakeItem(item, inventory)
            AllowDestroy(item)
            DestroyItem(item, inventory)
            #del inventory.items[key]
            #value.stashed = False
            #value.allow_destroy = True
            print("Item ID: ", item.id, " removed from inventory")
            ChangeDialog(npc.name, success_dialog, room, npc, inventory, answerbox, dialogbox)
            return
    print("Item not found in inventory")
    ChangeDialog(npc.name, failure_dialog, room, npc, inventory, answerbox, dialogbox)

def UnlockNPC(npcString, room, npc, inventory, answerbox, dialogbox):
    for npc in room.npcs.values():
        if npc.name == npcString:
            npc.unlock(npc.key, inventory)
            print("NPC unlocked: ", npc.name)
            return
    print("NPC not found")
        