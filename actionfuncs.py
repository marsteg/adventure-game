"""Action functions that can be triggered by game objects."""

import pygame

from room import Room


def LogText(text):
    """Log text to the console."""
    print(text)


def ChangePicture(action, new_image, old_image, _unused=None):
    """Toggle an action's image between two states."""
    if old_image is not None and action.state == new_image:
        action.imagepath = old_image
        action.state = old_image
    else:
        action.imagepath = new_image
        action.state = new_image
    print(f"Action '{action.name}' changed picture to: {action.imagepath}")

def ChangeRoomPicture(room, new_image):
    """Toggle a room's background image between two states."""
    if room.imagepath is new_image:
        return  # No change needed
    else:
        room.imagepath = new_image
        room.state = new_image
    print(f"Room '{room.name}' changed picture to: {room.imagepath}")


def PlaySound(soundfile):
    """Play a sound effect."""
    print(f"Playing sound: {soundfile}")
    sound = pygame.mixer.Sound(soundfile)
    sound.play()


def UnlockDoor(action, door):
    """Unlock a door using an action as the key."""
    if door.key != action:
        print("Wrong key")
        return
    print(f"Door unlocking (was locked: {door.locked})")
    door.unlock(door.key)
    print(f"Door position: {door.position}")


def AllowDestroy(item):
    """Mark an item as destroyable."""
    item.allow_destroy = True
    print(f"Item '{item.name}' can now be destroyed")


def GiveItem(item, inventory):
    """Give an item to the player's inventory."""
    item.stash(inventory)
    print(f"Item '{item.name}' added to inventory")


def TakeItem(item, inventory):
    """Take an item from the player's inventory."""
    item.unstash(inventory)
    inventory.release_slots(item)
    if item.name in inventory.items:
        del inventory.items[item.name]
    item.allow_destroy = True
    print(f"Item '{item.name}' removed from inventory")


def DestroyItem(item, inventory):
    """Destroy an item completely."""
    item.kill(inventory, Room.rooms)
    print(f"Item '{item.name}' (ID: {item.id}) destroyed")


def ActionChangeDialog(npc, dialog):
    """Change an NPC's active dialog state."""
    npc.active_dialog = dialog
    print(f"NPC '{npc.name}' (ID: {npc.id}) dialog changed to: {dialog}")
