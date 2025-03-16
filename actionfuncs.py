from inventory import *
from item import *
from room import *
from door import *
from rectshape import *

def LogText(text):
    print(text)

def ChangePicture(action, new_image, old_image, arg3=None):
    if old_image != None and action.state == new_image:
        action.image = pygame.image.load(old_image)
        action.image = pygame.transform.scale(action.image, (action.rect.width, action.rect.height))
        action.state = old_image
        print("Item ID: ", action.id, " changed picture to: ", action.image)
        return
    print("Change Picture")
    action.image = pygame.image.load(new_image)
    action.image = pygame.transform.scale(action.image, (action.rect.width, action.rect.height))
    action.state = new_image
    print("Item ID: ", action.id, " changed picture to: ", action.image)

def UnlockDoor(action, door):
    if door.key != action:
        print("Wrong key")
        return
    print("Door unlocked: ", door.locked)
    door.locked = False
    #door.image = pygame.image.load(door.open_image)
    #door.image = pygame.transform.scale(door.image, (door.rect.width, door.rect.height))
    print("Door position: ", door.position)

def AllowDestroy(item):
    item.allow_destroy = True
    print("Item ID: ", item.id, " can be destroyed")

    # Give item to the Player
def GiveItem(item, inventory):
    inventory.items[item.id] = item
    item.stash(inventory)
    print("Item ID: ", item.id, " added to inventory")
    print("Inventory items: ", inventory.items)

    # Take Item from the Player
def TakeItem(item, inventory):
    del inventory.items[item.id]
    item.stashed = False
    item.allow_destroy = True
    print("Item ID: ", item.id, " removed from inventory")

# unused
def DestroyItem(item, inventory, rooms):
    item.kill(inventory, rooms)
    print("Item ID: ", item.id, " destroyed")

