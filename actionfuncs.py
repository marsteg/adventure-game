from inventory import *
from item import *
from room import *
from door import *
from rectshape import *

def LogText(text):
    print(text)

def ChangePicture(action, new_image, old_image, arg3=None):
    if old_image != None and action.state == new_image:
        action.imagepath = old_image
        action.state = old_image
        print("Action Name: ", action.name, " changed picture to: ", action.image)
        return
    print("Change Picture")
    action.imagepath = new_image
    action.state = new_image
    print("Action Name: ", action.name, " changed picture to: ", action.image)

def PlaySound(soundfile):
    print("Playing sound: ", soundfile)
    sound = pygame.mixer.Sound(soundfile)
    sound.play()

def UnlockDoor(action, door):
    if door.key != action:
        print("Wrong key")
        return
    print("Door unlocked: ", door.locked)
    #door.locked = False
    door.unlock(door.key)
    #door.image = pygame.image.load(door.open_image)
    #door.image = pygame.transform.scale(door.image, (door.rect.width, door.rect.height))
    print("Door position: ", door.position)

def AllowDestroy(item):
    item.allow_destroy = True
    print("Item Name: ", item.name, " can be destroyed")

    # Give item to the Player
def GiveItem(item, inventory):
    item.stash(inventory)
    print("Item Name: ", item.name, " added to inventory")
    print("Inventory items: ", inventory.items)

    # Take Item from the Player
def TakeItem(item, inventory):
    item.unstash(inventory)
    inventory.release_slots(item)
    if item in inventory.items:
        del inventory.items[item.name]
    item.allow_destroy = True
    print("Item Name: ", item.name, " removed from inventory")

def DestroyItem(item, inventory):
    item.kill(inventory, Room.rooms)
    print("Item ID: ", item.id, " destroyed")

def ActionChangeDialog(npc, dialog):
    npc.active_dialog = dialog
    print("NPC ID: ", npc.id, " dialog changed to: ", npc.dialog)