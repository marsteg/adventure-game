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

# unused
def UnlockDoor(action, door):
    if door.key != action:
        print("Wrong key")
        return
    print("Door unlocked: ", door.locked)
    door.locked = False
    #door.image = pygame.image.load(door.open_image)
    #door.image = pygame.transform.scale(door.image, (door.rect.width, door.rect.height))
    print("Door position: ", door.position)