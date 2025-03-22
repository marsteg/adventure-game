from action import *
from door import *
from item import *
from rectshape import *
from room import *
from inventory import *
from npc import *

def SaveState(active_room, inventory,  filename):
    savedata = {}
    savedata["rooms"] = {}
    for room in Room.rooms.values():
        savedata["rooms"][room.name] = {}
        savedata["rooms"][room.name]['doors'] = {}
        savedata["rooms"][room.name]['actions'] = {}
        savedata["rooms"][room.name]['items'] = {}
        savedata["rooms"][room.name]['npcs'] = {}
        for door in room.doors.values():
            savedata["rooms"][room.name]['doors'][door.name] = {"locked": door.locked}
        for item in room.items.values():
            savedata["rooms"][room.name]['items'][item.name] = {"stashed": item.stashed, "allow_destroy": item.allow_destroy}
        for action in room.actions.values():
            savedata["rooms"][room.name]['actions'][action.name] = {"locked": action.locked, "state": action.state, "imagepath": action.imagepath}
        for npc in room.npcs.values():
            savedata["rooms"][room.name]['npcs'][npc.name] = {"active_dialog": npc.active_dialog, "locked": npc.locked}
    
    savedata['inventory'] = {}   
    for item in inventory.items.values():
            savedata['inventory'][item.name] = {"stashed": item.stashed, "allow_destroy": item.allow_destroy, "selfdestruct": item.selfdestruct, "left": item.rect.left, "top": item.rect.top, "width": item.rect.width, "height": item.rect.height, "imagepath": item.imagepath}
        
    savedata['active_room'] = active_room.name

    yaml_output = yaml.dump(savedata, sort_keys=False)

    with open(filename, 'w') as f:
        f.write(yaml_output)
    print('Written to file successfully')


def LoadState(filename):
    with open(filename, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

        for room_name, room_data in data["rooms"].items():
            if room_name in Room.rooms:
                room = Room.rooms[room_name]
                for door_name, door_data in room_data["doors"].items():
                    if door_name in room.doors:
                        room.doors[door_name].locked = door_data["locked"]
                items_to_delete = []
                for item_name, item_data in room.items.items():
                    if not item_name in room_data["items"]:
                        items_to_delete.append(item_name)
                for item_name in items_to_delete:
                    del room.items[item_name]

                for action_name, action_data in room_data["actions"].items():
                    if action_name in room.actions:
                        room.actions[action_name].locked = action_data["locked"]
                        room.actions[action_name].state = action_data["state"]
                        room.actions[action_name].imagepath = action_data["imagepath"]
                print('room_data["npcs"]:', room_data["npcs"])
                for npc_name, npc_data in room_data["npcs"].items():
                    if npc_name in room.npcs:
                        room.npcs[npc_name].active_dialog = npc_data['active_dialog']
                        room.npcs[npc_name].locked = npc_data["locked"]

        inventory = Inventory()
        inventory.items = {}
        for item_name, item_data in data["inventory"].items():
            item = Item(
                item_data["left"],
                item_data["top"],
                item_data["width"],
                item_data["height"],
                item_data["imagepath"],
                item_name,
                item_data["selfdestruct"]
            )
            inventory.items[item_name] = item
            found_room = None
            for room in Room.rooms.values():
                if item_name in room.items:
                    del room.items[item_name]
            item.stash(inventory, found_room)
            item.allow_destroy = item_data["allow_destroy"]
        
        active_room = None
        active_room_name = data["active_room"]
        if active_room_name in Room.rooms:
            active_room = Room.rooms[active_room_name]
        print('Loaded from file successfully')
        print('Active room:', active_room.name)
        print('Inventory:', inventory.items)
        return active_room, inventory
    

# collect the gamestate from
# - main
#     - active_room
# - inventory
# - every door
#    
# - every npc (excluding npc.dialog if possible)
#     - self.active_dialog
# - every action
#     - action.locked
# - every room
#     room.doors = {}
#        - door.locked
#     room.items = {}
#       - item.stashed
#       - item.stashed
#       - item.allow_destroy
#     room.actions = {}
#     room.npcs = {}
# - answerbox.state
# - dialogbox.state
    


