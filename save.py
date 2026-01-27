import yaml

from room import Room
from inventory import Inventory
from item import Item


def SaveState(active_room, inventory, filename):
    """Save the current game state to a YAML file."""
    savedata = {
        "rooms": {},
        "inventory": {},
        "active_room": active_room.name
    }

    # Save room states
    for room in Room.rooms.values():
        room_data = {
            "doors": {},
            "actions": {},
            "items": {},
            "npcs": {}
        }

        for door in room.doors.values():
            room_data["doors"][door.name] = {"locked": door.locked}

        for item in room.items.values():
            room_data["items"][item.name] = {
                "stashed": item.stashed,
                "allow_destroy": item.allow_destroy
            }

        for action in room.actions.values():
            room_data["actions"][action.name] = {
                "locked": action.locked,
                "state": action.state,
                "imagepath": action.imagepath
            }

        for npc in room.npcs.values():
            room_data["npcs"][npc.name] = {
                "active_dialog": npc.active_dialog,
                "locked": npc.locked
            }

        savedata["rooms"][room.name] = room_data

    # Save inventory
    for item in inventory.items.values():
        savedata["inventory"][item.name] = {
            "stashed": item.stashed,
            "allow_destroy": item.allow_destroy,
            "self_destruct": item.self_destruct,
            "left": item.rect.left,
            "top": item.rect.top,
            "width": item.rect.width,
            "height": item.rect.height,
            "imagepath": item.imagepath
        }

    try:
        yaml_output = yaml.dump(savedata, sort_keys=False)
        with open(filename, 'w') as f:
            f.write(yaml_output)
        print(f"Game saved to {filename} successfully")
    except IOError as e:
        print(f"Error saving game: {e}")
    except yaml.YAMLError as e:
        print(f"Error serializing game state: {e}")


def LoadState(filename):
    """Load a game state from a YAML file."""
    try:
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Save file not found: {filename}")
        return None, None
    except yaml.YAMLError as e:
        print(f"Error parsing save file: {e}")
        return None, None
    except IOError as e:
        print(f"Error reading save file: {e}")
        return None, None

    if not data:
        print("Save file is empty or invalid")
        return None, None

    # Restore room states
    for room_name, room_data in data.get("rooms", {}).items():
        if room_name not in Room.rooms:
            continue

        room = Room.rooms[room_name]

        # Restore door states
        for door_name, door_data in room_data.get("doors", {}).items():
            if door_name in room.doors:
                room.doors[door_name].locked = door_data["locked"]

        # Remove items that aren't in the save
        items_to_delete = [
            item_name for item_name in room.items
            if item_name not in room_data.get("items", {})
        ]
        for item_name in items_to_delete:
            del room.items[item_name]

        # Restore action states
        for action_name, action_data in room_data.get("actions", {}).items():
            if action_name in room.actions:
                action = room.actions[action_name]
                action.locked = action_data["locked"]
                action.state = action_data["state"]
                action.imagepath = action_data["imagepath"]

        # Restore NPC states
        for npc_name, npc_data in room_data.get("npcs", {}).items():
            if npc_name in room.npcs:
                npc = room.npcs[npc_name]
                npc.active_dialog = npc_data["active_dialog"]
                npc.locked = npc_data["locked"]

    # Restore inventory
    inventory = Inventory()
    inventory.items = {}

    for item_name, item_data in data.get("inventory", {}).items():
        # Support both old 'selfdestruct' and new 'self_destruct' keys
        self_destruct = item_data.get("self_destruct", item_data.get("selfdestruct", False))

        item = Item(
            item_data["left"],
            item_data["top"],
            item_data["width"],
            item_data["height"],
            item_data["imagepath"],
            item_name,
            self_destruct
        )
        inventory.items[item_name] = item

        # Remove from any rooms
        for room in Room.rooms.values():
            if item_name in room.items:
                del room.items[item_name]

        item.stash(inventory, None)
        item.allow_destroy = item_data["allow_destroy"]

    # Restore active room
    active_room_name = data.get("active_room")
    active_room = Room.rooms.get(active_room_name)

    if active_room:
        print(f"Loaded from {filename} successfully")
        print(f"Active room: {active_room.name}")
        print(f"Inventory: {list(inventory.items.keys())}")
    else:
        print(f"Warning: Active room '{active_room_name}' not found")

    return active_room, inventory
