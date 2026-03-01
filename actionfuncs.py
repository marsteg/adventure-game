"""Action functions that can be triggered by game objects."""

import pygame

from room import Room
from textcutscene import TextCutscene


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

def UnlockAction(key_action, unlocked_action):
    """Unlock an action using another action as the key."""
    if unlocked_action.key != key_action:
        print("Wrong key for this action")
        return
    print(f"Action unlocking (was locked: {unlocked_action.locked})")
    unlocked_action.unlock(key_action)
    print(f"Action position: {unlocked_action.position}")

def UnlockNPC(key, npc):
    """Unlock an NPC using an action as the key."""
    if npc.key != key:
        print("Wrong key for this NPC")
        return
    print(f"NPC unlocking (was locked: {npc.locked})")
    npc.unlock(key)  # NPCs don't use inventory, so we pass None
    print(f"NPC position: {npc.position}")

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

def ActionChangeDescription(action, new_desc, new_sound=None):
    """Change an action's unlocked description text and optionally the sound file.

    Args:
        action: The Action object to modify
        new_desc: New description text for the unlocked state
        new_sound: Optional new sound file path. If None, keeps existing sound.
    """
    action.description_text_unlocked = new_desc
    if new_sound:
        action.description_sound_unlocked = new_sound
    print(f"Action '{action.name}' (ID: {action.id}) unlocked description changed to: {new_desc}")


def PlayTextCutScene(yaml_path):
    """Play a Text based slide-show cutscene during gameplay"""
    import os
    from gamestate_manager import GameStateManager

    try:
        # Validate file exists
        if not os.path.exists(yaml_path):
            print(f"Cutscene file not found: {yaml_path}")
            return

        # Get GameStateManager instance and enqueue cutscene
        manager = GameStateManager.get_instance()
        success = manager.enqueue_cutscene(yaml_path)

        if success:
            print(f"Cutscene queued successfully: {yaml_path}")
        else:
            print(f"Failed to queue cutscene: {yaml_path}")

    except Exception as e:
        print(f"Error queueing cutscene {yaml_path}: {e}")