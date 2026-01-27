"""Dialog action functions that can be triggered from YAML dialog files."""

from actionfuncs import TakeItem, AllowDestroy, DestroyItem


def ResetAnswerBox(answerbox):
    """Reset the answer box to its initial state."""
    answerbox.state = None
    answerbox.answers = {}
    print("Answerbox reset")


def ExitDialog(new_active_dialog, room, npc, inventory, answerbox):
    """Exit the current dialog and set a new active dialog state."""
    print(f"Exiting dialog: {npc.name}")
    npc.active_dialog = new_active_dialog
    answerbox.answers = {}
    answerbox.state = None
    print("Dialog exited")


def ChangeDialog(npc_string, new_dialog, room, npc, inventory, answerbox):
    """Change the NPC's dialog to a new state and continue talking."""
    if npc.name == npc_string:
        npc.active_dialog = new_dialog
        answerbox.state = npc.active_dialog
        npc.talk(room, inventory, answerbox)
        print(f"Dialog changed to: {new_dialog}")
    else:
        print(f"NPC '{npc_string}' not found")


def TakeItemString(item_string, failure_dialog, success_dialog, room, npc, inventory, answerbox):
    """Take an item from the player's inventory by name."""
    for item in inventory.items.values():
        if item.name == item_string:
            TakeItem(item, inventory)
            AllowDestroy(item)
            DestroyItem(item, inventory)
            print(f"Item '{item.name}' (ID: {item.id}) removed from inventory")
            ChangeDialog(npc.name, success_dialog, room, npc, inventory, answerbox)
            return
    print(f"Item '{item_string}' not found in inventory")
    ChangeDialog(npc.name, failure_dialog, room, npc, inventory, answerbox)


def UnlockNPC(npc_string, room, npc, inventory, answerbox):
    """Unlock an NPC by name."""
    for room_npc in room.npcs.values():
        if room_npc.name == npc_string:
            room_npc.unlock(room_npc.key, inventory)
            print(f"NPC unlocked: {room_npc.name}")
            return
    print(f"NPC '{npc_string}' not found")
